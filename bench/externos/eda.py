"""EDA: Estimation of Distribution Algorithm, versión continua univariada (UMDA_c).

En cada generación se seleccionan los mejores individuos (truncamiento), se ajusta
una normal independiente por dimensión (media y desviación estándar) y se muestrea
la población siguiente de ese modelo. No usa cruce ni mutación: el modelo
probabilístico sustituye a los operadores de variación.

Referencias:
  Larrañaga, P. y Lozano, J. A. (Eds.) (2002). Estimation of Distribution Algorithms:
  A New Tool for Evolutionary Computation. Kluwer Academic Publishers.
  Larrañaga, P., Etxeberria, R., Lozano, J. A. y Peña, J. M. (2000). Optimization in
  continuous domains by learning and simulation of Gaussian networks. GECCO 2000 Workshop.
"""
import numpy as np


class EDA:
    def __init__(self, pop_size=50, seleccion=0.5, **params):
        self.pop_size = int(pop_size)          # N: tamaño de la población
        self.seleccion = float(seleccion)      # fracción seleccionada por truncamiento
        self.params = params

    def solve(self, f, lb, ub, dim, semilla):
        rng = np.random.default_rng(semilla)
        N = self.pop_size
        k = max(2, int(round(self.seleccion * N)))
        X = rng.uniform(lb, ub, (N, dim))
        F = np.array([f(x) for x in X])
        while True:                                       # el Tracker corta en max_fe
            S = X[np.argsort(F)[:k]]                      # selección por truncamiento
            media = S.mean(axis=0)
            desv = S.std(axis=0, ddof=1)
            X = np.clip(rng.normal(media, desv, (N, dim)), lb, ub)
            F = np.array([f(x) for x in X])
