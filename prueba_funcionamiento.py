"""Prueba de funcionamiento del catálogo completo de MEALPY.

Corre cada optimizador del catálogo dos veces con la misma semilla, con el mismo
ejecutor y el mismo control de presupuesto que los experimentos, y lo clasifica:

  utilizable          corre, consume el presupuesto, respeta los límites y es reproducible
  no_se_puede_crear   falla al crearse o al correr con sus parámetros por defecto
  fuera_de_limites    evalúa puntos fuera de los límites del dominio
  excede_presupuesto  una sola época no cabe en el presupuesto
  no_evoluciona       deja de evaluar después de inicializar
  consumo_variable    evoluciona, pero sus evaluaciones por época varían y termina antes
                      del presupuesto calibrado (requiere decidir cómo tratarlo)
  no_reproducible     dos corridas con la misma semilla dan resultados distintos
  excede_tiempo       no termina dentro del tiempo máximo

Uso:
  python prueba_funcionamiento.py                  # catálogo completo
  python prueba_funcionamiento.py --solo OriginalPSO OriginalDE
  python prueba_funcionamiento.py --procesos 4 --timeout 180

Salida: resultados/prueba_funcionamiento/catalogo.csv y resumen.md
"""
import argparse, csv, json, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SALIDA = Path("resultados/prueba_funcionamiento")
FUNCION, DIM, FE_POR_DIM, POP = "builtin:esfera_desplazada", 10, 1000, 50

TRABAJADOR = r"""
import json, sys, tempfile, warnings
warnings.filterwarnings("ignore")
from bench.config import Tarea
from bench.runner import ejecutar_tarea
nombre, funcion, dim, fe, pop = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
regs = []
for rep in range(2):
    with tempfile.TemporaryDirectory() as d:
        cfg = {"fe_por_dim": fe, "pop_size": pop, "semilla_base": 1000, "modo": "single",
               "parametros": {}, "salida": d}
        t = Tarea("prueba_funcionamiento", nombre, funcion, dim, 0)
        ejecutar_tarea(cfg, t, forzar=True)
        regs.append(json.load(open(f"{d}/runs/{t.clave}.json")))
print("@@" + json.dumps([{k: r.get(k) for k in ("estado", "error", "error_final", "nfe_real",
                        "max_fe", "fuera_limites", "no_finitos", "eval_inicializacion", "eval_por_epoca")} for r in regs]))
"""


def clasificar(regs):
    a, b = regs
    if a["estado"] == "error":
        return "no_se_puede_crear", a.get("error", "")
    if a.get("fuera_limites", 0) > 0:
        return "fuera_de_limites", f"{a['fuera_limites']} evaluaciones fuera de límites"
    if (a.get("eval_por_epoca") or 0) + (a.get("eval_inicializacion") or 0) > a["max_fe"]:
        return "excede_presupuesto", f"una época usa {a['eval_por_epoca']:.0f} evaluaciones de {a['max_fe']}"
    if a["estado"] == "subconsumo":
        if a["nfe_real"] <= (a.get("eval_inicializacion") or 0) + (a.get("eval_por_epoca") or 0):
            return "no_evoluciona", f"usa {a['nfe_real']} de {a['max_fe']} evaluaciones"
        return "consumo_variable", (f"usa {a['nfe_real']} de {a['max_fe']} evaluaciones: "
                                    "sus evaluaciones por época varían y termina antes del presupuesto")
    if a["error_final"] != b["error_final"]:
        return "no_reproducible", f"{a['error_final']:.6g} vs {b['error_final']:.6g}"
    return "utilizable", ""


def probar(nombre, timeout):
    t0 = time.perf_counter()
    try:
        p = subprocess.run([sys.executable, "-c", TRABAJADOR, nombre, FUNCION, str(DIM),
                            str(FE_POR_DIM), str(POP)],
                           capture_output=True, text=True, timeout=timeout)
        linea = next((l for l in p.stdout.splitlines() if l.startswith("@@")), None)
        if linea is None:
            cat, det = "no_se_puede_crear", (p.stderr.strip().splitlines() or ["sin salida"])[-1]
        else:
            cat, det = clasificar(json.loads(linea[2:]))
    except subprocess.TimeoutExpired:
        cat, det = "excede_tiempo", f"más de {timeout} s"
    return {"algoritmo": nombre, "categoria": cat, "detalle": det[:300],
            "tiempo_s": round(time.perf_counter() - t0, 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--solo", nargs="+")
    ap.add_argument("--procesos", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()

    from bench.runner import catalogo
    import mealpy
    nombres = sorted(a.solo or catalogo().keys())
    print(f"MEALPY {mealpy.__version__}: {len(nombres)} optimizadores")
    filas = []
    with ThreadPoolExecutor(a.procesos) as ex:
        for i, fila in enumerate(ex.map(lambda n: probar(n, a.timeout), nombres), 1):
            filas.append(fila)
            print(f"[{i:3d}/{len(nombres)}] {fila['algoritmo']:<28} {fila['categoria']}", flush=True)

    SALIDA.mkdir(parents=True, exist_ok=True)
    with open(SALIDA / "catalogo.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0]))
        w.writeheader(); w.writerows(filas)

    from collections import Counter
    c = Counter(f["categoria"] for f in filas)
    lineas = [f"# Prueba de funcionamiento del catálogo de MEALPY {mealpy.__version__}", "",
              f"Función {FUNCION}, D = {DIM}, {FE_POR_DIM}·D evaluaciones, población {POP}, "
              "dos corridas con la misma semilla.", "",
              "| Categoría | Número |", "|:--|--:|"]
    lineas += [f"| {k} | {v} |" for k, v in c.most_common()]
    lineas += [f"| **Total** | **{len(filas)}** |", "", "## Excluidos", "",
               "| Algoritmo | Categoría | Detalle |", "|:--|:--|:--|"]
    lineas += [f"| {f['algoritmo']} | {f['categoria']} | {f['detalle'].replace('|', '/')} |"
               for f in filas if f["categoria"] != "utilizable"]
    (SALIDA / "resumen.md").write_text("\n".join(lineas) + "\n")
    print("\n".join(lineas[4:4 + len(c) + 3]))


if __name__ == "__main__":
    main()
