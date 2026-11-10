"""Módulo de análisis: lee una carpeta de resultados y genera tablas, pruebas y figuras.

  python analyze.py resultados/e3_tres_algoritmos
No ejecuta ninguna metaheurística; puede correrse cuantas veces se quiera.
"""
import argparse, json
from pathlib import Path
import pandas as pd
from bench.analysis import aggregate as A, stats as S, plots as P


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("salida")
    ap.add_argument("--referencia", default=None)
    a = ap.parse_args()
    raiz = Path(a.salida); dest = raiz / "analisis"; fig = dest / "figuras"
    fig.mkdir(parents=True, exist_ok=True)
    tol = json.loads((raiz / "config_efectiva.json").read_text()).get("tolerancia_exito", 1e-8) \
        if (raiz / "config_efectiva.json").exists() else 1e-8

    df, curvas = A.cargar_corridas(raiz)
    df.to_csv(dest / "corridas.csv", index=False)
    estados = df["estado"].value_counts().to_dict()
    desc = A.descriptiva(df, tol); desc.to_csv(dest / "descriptiva.csv", index=False)
    A.tabla_checkpoints(curvas).to_csv(dest / "checkpoints.csv", index=False)
    P.convergencia(curvas, fig); P.boxplots(df, fig)

    md = [f"# Análisis — {raiz.name}\n",
          f"Corridas: {len(df)} · estados: {estados}\n",
          "## Estadística descriptiva del error final\n", desc.to_markdown(index=False, floatfmt=".3e"), ""]
    if desc["varianza_cero"].any():
        md += ["> Advertencia: Hay combinaciones con varianza cero entre corridas: revisar semillas.\n"]
    if desc["error_negativo"].any():
        malas = sorted(desc.loc[desc["error_negativo"], "funcion"].unique())
        md += [f"> Advertencia: Errores negativos en {malas}: el óptimo declarado no es el mínimo real; "
               "esas funciones no son válidas para comparar.\n"]
    sub = df[df["estado"] != "ok"]
    if len(sub):
        md += [f"> Advertencia: {len(sub)} corridas no terminaron normalmente (ver columna 'estado' en corridas.csv).\n"]

    algs = df["algoritmo"].nunique()
    if algs >= 2:
        pares, wtl = S.por_problema(df, a.referencia)
        pares.to_csv(dest / "pares_por_problema.csv", index=False)
        wtl.to_csv(dest / "ganadas_empatadas_perdidas.csv", index=False)
        md += ["## Comparación por problema (Mann-Whitney + Holm)\n",
               wtl.to_markdown(index=False), ""]
        W = S.wilcoxon_holm(df); W.to_csv(dest / "wilcoxon_holm.csv", index=False)
        md += ["## Wilcoxon de rangos con signo sobre medianas por bloque (Holm)\n",
               W.to_markdown(index=False, floatfmt=".4f"), ""]
    if algs >= 3:
        fr = S.friedman(df)
        pd.DataFrame({"rango_promedio": fr["rangos"]}).to_csv(dest / "friedman_rangos.csv")
        md += ["## Friedman\n",
               f"Bloques (función × D): {fr['bloques']} · algoritmos: {fr['k']}\n",
               f"χ² = {fr.get('chi2', float('nan')):.3f}, p = {fr.get('p', float('nan')):.4g}; "
               f"Iman-Davenport F = {fr.get('iman_davenport_F', float('nan')):.3f}, "
               f"p = {fr.get('p_iman_davenport', float('nan')):.4g}; "
               f"CD de Nemenyi (α=0.05) = {fr.get('nemenyi_CD', float('nan')):.3f}\n",
               fr["rangos"].to_frame("rango promedio").to_markdown(floatfmt=".3f"), ""]
        if "nemenyi_CD" in fr:
            P.diferencia_critica(fr["rangos"], fr["nemenyi_CD"], fig,
                                 f"Friedman/Nemenyi · {fr['bloques']} bloques")
    (dest / "resumen.md").write_text("\n".join(md))
    print("\n".join(md))
    print(f"\nTablas y figuras en {dest}")


if __name__ == "__main__":
    main()
