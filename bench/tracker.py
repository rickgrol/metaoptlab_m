"""Contador externo de evaluaciones: la fuente de verdad del presupuesto.

El tracker corta la ejecución en la evaluación número max_fe lanzando
PresupuestoAgotado. Así el presupuesto es exacto para todos los algoritmos,
sin depender de cuántas evaluaciones hace cada uno por época, y se evita el
Termination(max_fe) de MEALPY, que se revisa solo al final de cada época y
recorre todo el historial en cada una (costo cuadrático con muchas épocas).
"""


class PresupuestoAgotado(Exception):
    """Señal de fin normal de la corrida (no es un error)."""
import numpy as np

# Fracciones de registro del protocolo CEC2017 (0.01, 0.02, 0.03, 0.05, 0.1 … 1.0)
CHECKPOINTS_CEC = [0.01, 0.02, 0.03, 0.05] + [round(0.1 * k, 1) for k in range(1, 11)]


class Tracker:
    def __init__(self, f, f_opt, lb, ub, max_fe, fracciones=CHECKPOINTS_CEC):
        self.f, self.f_opt, self.lb, self.ub, self.max_fe = f, f_opt, lb, ub, max_fe
        self.cp_fe = sorted({max(1, int(round(p * max_fe))) for p in fracciones})
        self.reset()

    def reset(self):
        self.n = 0
        self.best = np.inf
        self.curva = {}            # fe -> mejor error hasta ese fe
        self._i_cp = 0
        self.fuera_limites = 0
        self.no_finitos = 0

    def __call__(self, x):
        if self.n >= self.max_fe:
            raise PresupuestoAgotado()
        self.n += 1
        x = np.asarray(x, dtype=float)
        if np.any(x < self.lb - 1e-9) or np.any(x > self.ub + 1e-9):
            self.fuera_limites += 1
        v = float(self.f(x))
        if not np.isfinite(v):
            self.no_finitos += 1
        err = v - self.f_opt
        if err < self.best:
            self.best = err
        while self._i_cp < len(self.cp_fe) and self.n >= self.cp_fe[self._i_cp]:
            self.curva[self.cp_fe[self._i_cp]] = self.best
            self._i_cp += 1
        return v

    def resultado(self):
        return {
            "error_final": self.best,
            "nfe_real": self.n,
            "curva_fe": list(self.curva.keys()),
            "curva_error": list(self.curva.values()),
            "fuera_limites": self.fuera_limites,
            "no_finitos": self.no_finitos,
        }
