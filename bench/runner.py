"""Ejecución de una tarea: un algoritmo de MEALPY, una función, una corrida.

No es interactivo: escribe un JSON por corrida y nada más. Si el JSON ya
existe, la tarea se omite (reanudación sin repetir trabajo).
"""
import io, json, math, time, platform, contextlib, traceback
from pathlib import Path
import numpy as np

from .functions import build_function
from .tracker import Tracker, PresupuestoAgotado


def catalogo():
    import mealpy
    try:
        return mealpy.get_all_optimizers(verbose=False)
    except TypeError:                                    # MEALPY 3.0.1
        with contextlib.redirect_stdout(io.StringIO()):
            return mealpy.get_all_optimizers()


def medir_evaluaciones(cls, params, pop, lb, ub, dim, f, semilla):
    """Mide cuántas evaluaciones hace el algoritmo al inicializar y en cada época.

    Corre el algoritmo 1 y 3 épocas con un contador sin límite:
      por_epoca = (n3 − n1) / 2      inicializacion = n1 − por_epoca
    Así se puede fijar el número de épocas que cabe exactamente en el presupuesto.
    """
    from mealpy import FloatVar
    conteos = []
    for ep in (1, 3):
        c = Tracker(f, 0.0, lb, ub, max_fe=10**12)
        m = cls(epoch=ep, pop_size=pop, **params)
        prob = {"obj_func": c, "bounds": FloatVar(lb=[lb] * dim, ub=[ub] * dim),
                "minmax": "min", "log_to": None}
        c.reset()
        m.solve(prob, mode="single", seed=semilla)
        conteos.append(c.n)
    por_epoca = (conteos[1] - conteos[0]) / 2
    return max(0, conteos[0] - por_epoca), por_epoca


def ruta_resultado(cfg, tarea):
    return Path(cfg["salida"]) / "runs" / f"{tarea.clave}.json"


def ejecutar_tarea(cfg, tarea, forzar=False):
    destino = ruta_resultado(cfg, tarea)
    if destino.exists() and not forzar:
        return "omitida"
    import mealpy
    from mealpy import FloatVar

    f, lb, ub, f_opt, etiqueta = build_function(tarea.funcion, tarea.dim)
    max_fe = int(cfg["fe_por_dim"] * tarea.dim)
    tr = Tracker(f, f_opt, lb, ub, max_fe)
    params = dict(cfg["parametros"].get(tarea.algoritmo, {}))
    pop = int(params.pop("pop_size", cfg["pop_size"]))   # permite pop_size por algoritmo

    reg = {"tarea": tarea.dict(), "max_fe": max_fe, "pop_size": pop,
           "parametros": params, "semilla": tarea.semilla(cfg["semilla_base"]),
           "modo": cfg["modo"], "mealpy": mealpy.__version__,
           "python": platform.python_version()}
    t0 = time.perf_counter()
    try:
        cls = catalogo()[tarea.algoritmo]
        # Número de épocas calibrado al presupuesto. Muchos algoritmos ajustan sus
        # parámetros con epoch / self.epoch (por ejemplo, el tamaño de paso); si self.epoch
        # no corresponde a las épocas que realmente caben en max_fe, ese programa interno
        # se distorsiona. El validador de MEALPY limita epoch a 100 000: se construye dentro
        # del límite y luego se asigna el valor calibrado. El tracker corta en max_fe exacto.
        inic, por_epoca = medir_evaluaciones(cls, params, pop, lb, ub, tarea.dim, f, reg["semilla"])
        epocas = (int(math.ceil((max_fe - inic) / por_epoca)) if por_epoca > 0 else max_fe)
        epocas = max(1, epocas)
        reg.update({"eval_inicializacion": inic, "eval_por_epoca": por_epoca,
                    "epocas_planeadas": epocas})
        modelo = cls(epoch=min(epocas, 100000), pop_size=pop, **params)
        modelo.epoch = epocas
        problema = {"obj_func": tr, "bounds": FloatVar(lb=[lb] * tarea.dim, ub=[ub] * tarea.dim),
                    "minmax": "min", "log_to": None}
        tr.reset()                       # MEALPY puede evaluar una vez al construir el problema
        try:
            modelo.solve(problema, mode=cfg["modo"], seed=reg["semilla"])
        except PresupuestoAgotado:
            pass                                        # fin normal: presupuesto exacto
        reg.update(tr.resultado())
        reg["estado"] = "ok" if tr.n >= max_fe else "subconsumo"
    except Exception as e:
        reg.update({"estado": "error", "error": f"{type(e).__name__}: {e}",
                    "traceback": traceback.format_exc()[-2000:]})
    reg["tiempo_s"] = time.perf_counter() - t0

    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(".tmp")
    tmp.write_text(json.dumps(reg, default=float))
    tmp.replace(destino)                 # escritura atómica: nunca queda un JSON a medias
    return reg["estado"]
