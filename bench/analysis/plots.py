"""Figuras: convergencia (mediana e IQR vs. evaluaciones), boxplots y diagrama de diferencia crítica."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PISO = 1e-16   # para escala logarítmica cuando el error llega a 0


def convergencia(curvas, carpeta):
    rutas = []
    for (f, d), g in curvas.groupby(["funcion", "dim"]):
        fig, ax = plt.subplots(figsize=(6.4, 4.2))
        for a, ga in g.groupby("algoritmo"):
            q = ga.groupby("fe")["error"].quantile([0.25, 0.5, 0.75]).unstack().clip(lower=PISO)
            ax.plot(q.index, q[0.5], label=a, lw=1.6)
            ax.fill_between(q.index, q[0.25], q[0.75], alpha=0.2)
        ax.set_yscale("log"); ax.set_xscale("log")
        ax.set_xlabel("Evaluaciones de la función"); ax.set_ylabel("Error  f(x) − f*")
        ax.set_title(f"{f}  ·  D = {d}   (mediana e IQR, {g['corrida'].nunique()} corridas)", fontsize=10)
        ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=8)
        ruta = Path(carpeta) / f"conv_{f.replace(':', '-')}_D{d}.png"
        fig.tight_layout(); fig.savefig(ruta, dpi=300); plt.close(fig); rutas.append(ruta)
    return rutas


def boxplots(df, carpeta):
    rutas = []
    ok = df[df["estado"] == "ok"]
    for (f, d), g in ok.groupby(["funcion", "dim"]):
        algs = sorted(g["algoritmo"].unique())
        datos = [np.clip(g.loc[g.algoritmo == a, "error_final"], PISO, None) for a in algs]
        fig, ax = plt.subplots(figsize=(max(4, 1.2 * len(algs) + 2), 4))
        ax.boxplot(datos, tick_labels=algs, showfliers=True)
        ax.set_yscale("log"); ax.set_ylabel("Error final")
        ax.set_title(f"{f} · D = {d}", fontsize=10); ax.grid(alpha=0.3, axis="y")
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        ruta = Path(carpeta) / f"box_{f.replace(':', '-')}_D{d}.png"
        fig.tight_layout(); fig.savefig(ruta, dpi=300); plt.close(fig); rutas.append(ruta)
    return rutas


def diferencia_critica(rangos, cd, carpeta, titulo=""):
    k = len(rangos)
    fig, ax = plt.subplots(figsize=(7, 1.2 + 0.35 * k))
    lo, hi = 1, k
    ax.hlines(0, lo, hi, color="k"); ax.set_xlim(lo - 0.3, hi + 0.3)
    for i in range(lo, hi + 1):
        ax.vlines(i, -0.05, 0.05, color="k"); ax.text(i, 0.12, str(i), ha="center", fontsize=8)
    for j, (a, r) in enumerate(rangos.items()):
        y = -0.3 - 0.25 * j
        ax.plot([r, r], [0, y], color="0.4", lw=0.8)
        ax.text(r + 0.05, y, f"{a} ({r:.2f})", va="center", fontsize=8)
    ax.plot([lo, lo + cd], [0.35, 0.35], color="C3", lw=3)
    ax.text(lo + cd / 2, 0.45, f"CD = {cd:.2f}", ha="center", fontsize=8, color="C3")
    ax.axis("off"); ax.set_title(titulo, fontsize=9)
    ruta = Path(carpeta) / "diferencia_critica.png"
    fig.tight_layout(); fig.savefig(ruta, dpi=300); plt.close(fig)
    return ruta
