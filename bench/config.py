"""Configuración declarativa (YAML) → lista de tareas independientes.

Una tarea = (algoritmo, función, dimensión, corrida). Es la unidad que el
orquestador (Snakemake) o el ejecutor secuencial reparten.
"""
from dataclasses import dataclass, asdict
from pathlib import Path
import itertools, yaml

DEFAULTS = {
    "fe_por_dim": 10000,       # presupuesto CEC: 10 000 · D
    "pop_size": 50,
    "corridas": 30,
    "semilla_base": 1000,
    "modo": "single",          # paralelizar entre corridas, no dentro del algoritmo
    "tolerancia_exito": 1e-8,
    "parametros": {},          # {"OriginalDE": {"wf": 0.8, "cr": 0.9}, ...}
}


@dataclass(frozen=True)
class Tarea:
    experimento: str
    algoritmo: str
    funcion: str
    dim: int
    corrida: int

    @property
    def clave(self):
        f = self.funcion.replace(":", "-")
        return f"{self.algoritmo}/{f}/D{self.dim}/r{self.corrida:02d}"

    @property
    def bloque(self):
        """Algoritmo × función × D: las 30 corridas de un bloque van en un mismo job,
        para no pagar 30 veces el arranque de Python + MEALPY."""
        return self.clave.rsplit("/", 1)[0]

    def semilla(self, base):
        # Misma semilla para todos los algoritmos en la corrida r (números aleatorios
        # comunes) y distinta entre corridas: varianza real entre réplicas.
        return base + self.corrida

    def dict(self):
        return asdict(self)


def cargar(ruta, **override):
    cfg = dict(DEFAULTS)
    cfg.update(yaml.safe_load(Path(ruta).read_text()))
    cfg.update({k: v for k, v in override.items() if v is not None})
    for req in ("experimento", "algoritmos", "funciones", "dimensiones"):
        if req not in cfg:
            raise ValueError(f"Falta '{req}' en {ruta}")
    cfg.setdefault("salida", f"resultados/{cfg['experimento']}")
    return cfg


def tareas(cfg):
    return [Tarea(cfg["experimento"], a, f, int(d), r)
            for a, f, d, r in itertools.product(cfg["algoritmos"], cfg["funciones"],
                                                cfg["dimensiones"], range(cfg["corridas"]))]


def validar(cfg):
    """Antes de lanzar nada: ¿existen los algoritmos y las combinaciones función × dimensión?"""
    from .functions import validate
    from .runner import catalogo
    cat = catalogo()
    faltan = [a for a in cfg["algoritmos"] if a not in cat]
    if faltan:
        raise ValueError(f"Algoritmos que no existen en este MEALPY: {faltan}")
    for f, d in itertools.product(cfg["funciones"], cfg["dimensiones"]):
        validate(f, int(d))
