"""Catálogo de funciones objetivo.

Especificación por texto en la configuración:
  "builtin:esfera_desplazada"     funciones propias (desplazamiento fijo, reproducible)
  "cec2017:F5"                    cualquier función de opfunu por suite y número
Toda función se devuelve como (f, lb, ub, f_opt, etiqueta).
"""
import numpy as np

_SHIFT_SEED = 2026


def _shift(dim, lb, ub):
    rng = np.random.default_rng(_SHIFT_SEED + dim)
    return rng.uniform(0.8 * lb, 0.8 * ub, dim)


class _Builtin:
    def __init__(self, dim, lb, ub):
        self.dim, self.lb, self.ub = dim, lb, ub
        self.o = _shift(dim, lb, ub)


class EsferaDesplazada(_Builtin):
    def __call__(self, x):
        z = np.asarray(x) - self.o
        return float(z @ z)


class RastriginDesplazada(_Builtin):
    def __call__(self, x):
        z = np.asarray(x) - self.o
        return float(10 * z.size + np.sum(z * z - 10 * np.cos(2 * np.pi * z)))


class Esfera(_Builtin):
    """Óptimo en el origen: solo para diagnosticar sesgo al centro, no para comparar."""
    def __call__(self, x):
        x = np.asarray(x)
        return float(x @ x)


BUILTIN = {
    "esfera_desplazada": (EsferaDesplazada, -100.0, 100.0),
    "rastrigin_desplazada": (RastriginDesplazada, -5.12, 5.12),
    "esfera_origen": (Esfera, -100.0, 100.0),
}


def build_function(spec: str, dim: int):
    fuente, nombre = spec.split(":", 1)
    if fuente == "builtin":
        cls, lb, ub = BUILTIN[nombre]
        return cls(dim, lb, ub), lb, ub, 0.0, spec
    # opfunu: "cec2017:F5" -> clase "F52017"
    import opfunu
    anio = fuente.replace("cec", "")
    clase = f"{nombre}{anio}"
    encontrados = opfunu.get_functions_by_classname(clase)
    if not encontrados:
        raise ValueError(f"opfunu no tiene la función {clase} ({spec})")
    prob = encontrados[0](ndim=dim)          # lanza error si la dimensión no es válida
    lb, ub = float(prob.bounds[0, 0]), float(prob.bounds[0, 1])
    return prob.evaluate, lb, ub, float(prob.f_global), spec


def validate(spec: str, dim: int):
    """Falla temprano (antes de lanzar el experimento) si la combinación no existe."""
    build_function(spec, dim)
