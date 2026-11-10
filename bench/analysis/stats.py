"""Estadística no paramétrica para comparar metaheurísticas.

Esquema estándar (Derrac, García, Molina y Herrera, 2011, Swarm Evol. Comput.):
  • Por problema (función × dimensión), sobre las 30 corridas:
      Kruskal-Wallis + Mann-Whitney por pares con corrección de Holm → +/≈/− vs. referencia.
  • Sobre el conjunto de problemas (bloques), con la mediana de cada algoritmo:
      Friedman (+ Iman-Davenport), rangos promedio, diferencia crítica de Nemenyi
      y Wilcoxon de rangos con signo por pares con Holm.
"""
import itertools
import numpy as np
import pandas as pd
from scipy import stats


def holm(pvals):
    p = np.asarray(pvals, float)
    orden = np.argsort(p)
    m = len(p)
    ajust = np.empty(m)
    acum = 0.0
    for i, idx in enumerate(orden):
        acum = max(acum, min(1.0, (m - i) * p[idx]))
        ajust[idx] = acum
    return ajust


def por_problema(df, referencia=None, alpha=0.05):
    ok = df[df["estado"] == "ok"]
    algs = sorted(ok["algoritmo"].unique())
    if len(algs) < 2:
        return pd.DataFrame(), pd.DataFrame()
    pares, resumen = [], []
    for (f, d), g in ok.groupby(["funcion", "dim"]):
        muestras = {a: g.loc[g["algoritmo"] == a, "error_final"].values for a in algs}
        if any(len(v) < 2 for v in muestras.values()):
            continue
        kw = stats.kruskal(*muestras.values()) if len(algs) > 2 else None
        filas = []
        for a, b in itertools.combinations(algs, 2):
            try:
                p = stats.mannwhitneyu(muestras[a], muestras[b], alternative="two-sided").pvalue
            except ValueError:                       # muestras idénticas
                p = 1.0
            filas.append({"funcion": f, "dim": d, "A": a, "B": b, "p": p,
                          "mediana_A": np.median(muestras[a]), "mediana_B": np.median(muestras[b])})
        p_adj = holm([x["p"] for x in filas])
        for x, pa in zip(filas, p_adj):
            x["p_holm"] = pa
            x["resultado"] = ("≈" if pa >= alpha else
                              ("A mejor" if x["mediana_A"] < x["mediana_B"] else "B mejor"))
        pares += filas
        resumen.append({"funcion": f, "dim": d,
                        "kruskal_p": kw.pvalue if kw else np.nan})
    pares = pd.DataFrame(pares)

    # +/≈/− de cada algoritmo frente a la referencia (por defecto, el mejor rango de Friedman)
    if referencia is None:
        referencia = friedman(df)["rangos"].index[0] if len(algs) > 2 else algs[0]
    wtl = []
    for a in algs:
        if a == referencia:
            continue
        sub = pares[((pares.A == a) & (pares.B == referencia)) | ((pares.A == referencia) & (pares.B == a))]
        mas = ((sub.A == a) & (sub.resultado == "A mejor")).sum() + ((sub.B == a) & (sub.resultado == "B mejor")).sum()
        menos = ((sub.A == a) & (sub.resultado == "B mejor")).sum() + ((sub.B == a) & (sub.resultado == "A mejor")).sum()
        wtl.append({"algoritmo": a, "vs": referencia, "+ (mejor)": int(mas),
                    "≈": int(len(sub) - mas - menos), "− (peor)": int(menos)})
    return pares, pd.DataFrame(wtl)


def matriz_bloques(df, estadistico="median"):
    ok = df[df["estado"] == "ok"]
    return ok.groupby(["funcion", "dim", "algoritmo"])["error_final"].agg(estadistico).unstack("algoritmo")


def friedman(df, alpha=0.05):
    M = matriz_bloques(df).dropna()
    N, k = M.shape
    rangos = M.rank(axis=1, method="average")
    R = rangos.mean().sort_values()
    out = {"bloques": N, "k": k, "rangos": R}
    if k >= 3 and N >= 2:
        chi2, p = stats.friedmanchisquare(*[M[c].values for c in M.columns])
        ff = (N - 1) * chi2 / (N * (k - 1) - chi2) if N * (k - 1) != chi2 else np.inf
        p_id = stats.f.sf(ff, k - 1, (k - 1) * (N - 1))
        q = stats.studentized_range.ppf(1 - alpha, k, np.inf) / np.sqrt(2)
        out.update({"chi2": chi2, "p": p, "iman_davenport_F": ff, "p_iman_davenport": p_id,
                    "nemenyi_CD": q * np.sqrt(k * (k + 1) / (6 * N))})
    return out


def wilcoxon_holm(df):
    M = matriz_bloques(df).dropna()
    filas = []
    for a, b in itertools.combinations(M.columns, 2):
        d = M[a] - M[b]
        if (d == 0).all() or len(d) < 2:
            p = 1.0
        else:
            p = stats.wilcoxon(M[a], M[b], zero_method="zsplit").pvalue
        filas.append({"A": a, "B": b, "p": p, "bloques_A_mejor": int((d < 0).sum()),
                      "bloques_B_mejor": int((d > 0).sum())})
    t = pd.DataFrame(filas)
    if len(t):
        t["p_holm"] = holm(t["p"])
    return t
