"""Random Search (búsqueda aleatoria pura).

Referencia de exploración pura: cada evaluación es un punto uniforme en todo el
dominio, sin usar información previa. No es una metaheurística; sirve como base
de comparación (cualquier método debería superarla).
"""
import numpy as np


class RandomSearch:
    def __init__(self, **params):
        self.params = params                     # no tiene parámetros

    def solve(self, f, lb, ub, dim, semilla):
        rng = np.random.default_rng(semilla)
        while True:                              # el Tracker corta en max_fe
            f(rng.uniform(lb, ub, dim))
