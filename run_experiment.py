"""Ejecutor de experimentos (no interactivo).

  python run_experiment.py configs/e3_tres_algoritmos.yaml            # todo, secuencial, reanudable
  python run_experiment.py configs/e3_tres_algoritmos.yaml --listar   # muestra las tareas
  python run_experiment.py CFG --bloque "OriginalDE/cec2017-F4/D10"      # 30 corridas de un bloque (Snakemake)
  python run_experiment.py CFG --tarea "OriginalDE/cec2017-F4/D10/r03"   # una sola corrida
  python run_experiment.py CFG --corridas 5 --dimensiones 10            # versión reducida para probar
"""
import argparse, sys, time, json
from pathlib import Path
from bench import config as C
from bench.runner import ejecutar_tarea


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cfg")
    ap.add_argument("--listar", action="store_true")
    ap.add_argument("--tarea")
    ap.add_argument("--bloque")
    ap.add_argument("--corridas", type=int)
    ap.add_argument("--dimensiones", type=int, nargs="+")
    ap.add_argument("--fe_por_dim", type=int)
    ap.add_argument("--salida")
    a = ap.parse_args()

    cfg = C.cargar(a.cfg, corridas=a.corridas, dimensiones=a.dimensiones,
                   fe_por_dim=a.fe_por_dim, salida=a.salida)
    C.validar(cfg)
    tareas = C.tareas(cfg)
    if a.listar:
        print("\n".join(t.clave for t in tareas)); return
    if a.bloque:
        tareas = [t for t in tareas if t.bloque == a.bloque]
        if not tareas:
            sys.exit(f"Bloque desconocido: {a.bloque}")
    if a.tarea:
        tareas = [t for t in tareas if t.clave == a.tarea]
        if not tareas:
            sys.exit(f"Tarea desconocida: {a.tarea}")

    Path(cfg["salida"]).mkdir(parents=True, exist_ok=True)
    (Path(cfg["salida"]) / "config_efectiva.json").write_text(json.dumps(cfg, indent=2))
    t0, n = time.time(), len(tareas)
    for i, t in enumerate(tareas, 1):
        estado = ejecutar_tarea(cfg, t)
        if estado != "omitida":
            print(f"[{i}/{n}] {t.clave:<45} {estado:<10} {time.time()-t0:7.1f}s", flush=True)
    print(f"Listo: {n} tareas en {time.time()-t0:.1f}s → {cfg['salida']}")


if __name__ == "__main__":
    main()
