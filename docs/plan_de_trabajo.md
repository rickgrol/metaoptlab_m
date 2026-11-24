# Plan de trabajo — MetaOptLab-M

**Actualizado:** 10 de noviembre de 2026

Este plan ordena el trabajo según las indicaciones del Dr. Marrero en las sesiones del 22 de septiembre, 20 de octubre y 3 de noviembre de 2026.

## Principios

- **Prioridad:** el módulo de algoritmos va primero. Las medidas estadísticas de desempeño vienen después; por ahora basta con media y desviación estándar.
- **Un método a la vez:** se suma, se revisa y se documenta antes de pasar al siguiente.
- **Implementaciones de MEALPY:** de cada método se usa su versión básica. Una implementación externa solo se usa cuando el método no existe en MEALPY o cuando la de MEALPY tiene problemas serios, y en ambos casos se justifica.
- **Conocer la variante:** de cada método hay que saber qué variante se toma y qué implementa.

## Fase 1. Módulo de algoritmos (15 métodos sumados; contraste con papers en curso)

### Procedimiento por método

1. Declararlo en un YAML de `configs/`, con su versión básica de MEALPY.
2. Correrlo en prueba reducida: 5 corridas, D = 10, 1 000·D evaluaciones.
3. Revisar su código en MEALPY contra el paper original.
4. Documentarlo en `docs/algoritmos/<método>.md`.

### Seguimiento

Lista de los 15 métodos acordada con el Dr. Marrero (sesión del 22 de septiembre de 2026), con su numeración, más Random Search como baseline estocástico.

| # | Método | Paradigma | Clase usada | Estado | Documento |
|:-:|:--|:--|:--|:--|:--|
| 1 | SA (Simulated Annealing) | Trayectoria | `OriginalSA` | Sumado y documentado | `simulated_annealing.md` |
| 2 | DE | Evolutivo | `OriginalDE` | Sumado y documentado | `differential_evolution.md` |
| 3 | PSO | Enjambre | `OriginalPSO` | Sumado y documentado | `pso.md` |
| 4 | TLBO | Social / humano | `OriginalTLO` | Sumado y documentado | `tlbo.md` |
| 5 | GA | Evolutivo | `BaseGA` (`OriginalGA` no evoluciona en 3.0.3) | Sumado y documentado | `genetic_algorithm.md` |
| 6 | Tabu Search | Trayectoria con memoria | `OriginalTS` | Sumado y documentado; lista tabú sin efecto en continuo | `tabu_search.md` |
| 7 | ACO | Constructivo (ACO_R para continuo) | `OriginalACOR` | Sumado y documentado | `aco.md` |
| 8 | ASO | Físico / químico | `OriginalASO` | Sumado y documentado; error en el centro de masa | `aso.md` |
| 9 | CMA-ES | Evolutivo (estrategia evolutiva) | `CMA_ES` | Sumado y documentado; implementación con defectos graves | `cma_es.md` |
| 10 | ABC | Enjambre | `OriginalABC` | Sumado y documentado | `abc.md` |
| 11 | GWO | Enjambre | `OriginalGWO` | Sumado y documentado | `gwo.md` |
| 12 | EDA | Probabilístico | Implementación propia, UMDA_c (`externo:EDA`) | Sumado y documentado | `eda.md` |
| 13 | Hill Climbing | Trayectoria local | `OriginalHC` | Sumado y documentado | `hill_climbing.md` |
| 14 | ICA | Social | `OriginalICA` | Sumado y documentado; la población crece cada época | `ica.md` |
| 15 | SCA | Matemático / oscilaciones | `OriginalSCA` | Sumado y documentado | `sca.md` |
| — | Random Search | Baseline estocástico (no es metaheurística; 100 % exploración) | Implementación propia (`externo:RandomSearch`) | Sumado y documentado | `random_search.md` |

"Documentado" significa revisado contra el código de MEALPY 3.0.3 (o contra la implementación propia); el contraste detallado con cada paper original queda como revisión pendiente.

**Algoritmos campeones de competencias CEC** (referencia positiva, después de los 15): MEALPY incluye `L_SHADE`, `OriginalLSHADEcnEpSin` e `OriginalIMODE`. Se revisarán con el mismo procedimiento.

## Fase 2. Medidas estadísticas de desempeño

Una vez que los métodos estén corriendo. El módulo ya existe en `bench/analysis/stats.py`: Friedman con Iman-Davenport, diferencia crítica de Nemenyi, y Wilcoxon y Mann-Whitney con corrección de Holm. Falta revisarlo y validarlo.

## Fase 3. Experimento comparativo masivo (paper 1)

Embudo acordado el 20 de octubre:

1. Todos los algoritmos de MEALPY que corran, en 8–10 funciones, con 30 corridas. Los que no corran se documentan con su motivo.
2. Los mejores, en una suite CEC completa.
3. Reducción y prueba en tres suites CEC.
4. Núcleo final de 20–30 algoritmos, elegidos por desempeño y diversidad.

Requiere las máquinas del laboratorio y el orquestador (Snakemake).

## Pendientes transversales

- **Referencia original de HC.** Candidatas de la bibliografía del curso del Dr. Marrero: Talbi (2009), *Metaheuristics: From Design to Implementation*, y Brownlee (2012), *Clever Algorithms*. Confirmar con él.
- **Validar las funciones de opfunu** contra el código oficial de CEC antes de la Fase 3. Hay errores conocidos: la numeración de CEC2017 está recorrida y la F9 es inválida.
- **SA propio como algoritmo externo**, si se decide (el punto de extensión ya existe: `bench/externos/`).

## Registro de avance

| Fecha | Avance |
|:--|:--|
| 3-nov | El Dr. Marrero fija la prioridad: módulo de algoritmos, uno por uno |
| 9-nov | Pipeline corriendo en Colab (prueba rápida: 45/45 corridas OK) |
| 10-nov | Calibración de épocas al presupuesto; punto de extensión para algoritmos externos; 8 métodos sumados, corridos (`configs/modulo_algoritmos.yaml`) y documentados; repositorio en GitHub compartido |
| 16-nov | ACO_R y CMA-ES sumados, corridos y documentados (10 métodos). Se detecta que `CMA_ES` de MEALPY no usa la selección para mover la media |
| 17-nov | Tabu Search, ASO, GWO, ICA y SCA (MEALPY) y EDA (implementación propia, UMDA_c) sumados, corridos y documentados: 15 métodos completos más Random Search |
