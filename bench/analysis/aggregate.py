"""Lee los JSON de corridas y produce tablas. No ejecuta nada."""
import json
from pathlib import Path
import numpy as np
import pandas as pd


def cargar_corridas(salida):
    filas, curvas = [], []
    for p in sorted(Path(salida, "runs").rglob("*.json")):
        r = json.loads(p.read_text())
        t = r["tarea"]
        base = {"algoritmo": t["algoritmo"], "funcion": t["funcion"], "dim": t["dim"],
                "corrida": t["corrida"], "estado": r.get("estado"), "semilla": r.get("semilla")}
        filas.append({**base, "error_final": r.get("error_final", np.nan),
                      "nfe_real": r.get("nfe_real"),
                      "max_fe": r.get("max_fe"), "tiempo_s": r.get("tiempo_s"),
                      "fuera_limites": r.get("fuera_limites"), "no_finitos": r.get("no_finitos"),
                      "eval_por_epoca": r.get("eval_por_epoca"), "epocas_planeadas": r.get("epocas_planeadas"),
                      "error": r.get("error")})
        for fe, e in zip(r.get("curva_fe", []), r.get("curva_error", [])):
            curvas.append({**base, "fe": fe, "fe_frac": fe / r["max_fe"], "error": e})
    return pd.DataFrame(filas), pd.DataFrame(curvas)


def descriptiva(df, tol=1e-8):
    ok = df[df["estado"] == "ok"]
    g = ok.groupby(["funcion", "dim", "algoritmo"])["error_final"]
    t = pd.DataFrame({
        "n": g.size(), "mejor": g.min(), "peor": g.max(), "mediana": g.median(),
        "media": g.mean(), "desv": g.std(ddof=1),
        "SR_%": g.apply(lambda s: 100 * ((s <= tol) & (s >= -tol)).mean()),
        "tiempo_med_s": ok.groupby(["funcion", "dim", "algoritmo"])["tiempo_s"].median(),
    }).reset_index()
    # Control de calidad: varianza cero entre réplicas = corridas no independientes
    t["varianza_cero"] = (t["n"] > 1) & (t["desv"] == 0) & (t["mejor"] > tol)
    # Control de calidad: error < 0 significa que f_opt declarado no es el mínimo real
    t["error_negativo"] = t["mejor"] < -tol
    return t


def tabla_checkpoints(curvas, fracciones=(0.01, 0.1, 0.5, 1.0)):
    c = curvas[curvas["fe_frac"].round(4).isin([round(f, 4) for f in fracciones])]
    return (c.groupby(["funcion", "dim", "algoritmo", "fe_frac"])["error"].median()
             .unstack("fe_frac").add_prefix("mediana@").reset_index())
