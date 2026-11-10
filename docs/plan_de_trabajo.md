# Plan de trabajo — MetaOptLab-M

**Actualizado:** 10 de noviembre de 2026

Este plan ordena el trabajo según las indicaciones del Dr. Marrero en las sesiones del 22 de septiembre, 20 de octubre y 3 de noviembre de 2026.

## Principios

- **Prioridad:** el módulo de algoritmos va primero. Las medidas estadísticas de desempeño vienen después; por ahora basta con media y desviación estándar.
- **Un método a la vez:** se suma, se revisa y se documenta antes de pasar al siguiente.
- **Implementaciones de MEALPY:** de cada método se usa su versión básica. Una implementación externa solo se usa cuando el método no existe en MEALPY o cuando la de MEALPY tiene problemas serios, y en ambos casos se justifica.
- **Conocer la variante:** de cada método hay que saber qué variante se toma y qué implementa.

## Fase 1. Módulo de algoritmos (en curso)

### Procedimiento por método

1. Declararlo en un YAML de `configs/`, con su versión básica de MEALPY.
2. Correrlo en prueba reducida: 5 corridas, D = 10, 1 000·D evaluaciones.
3. Revisar su código en MEALPY contra el paper original.
4. Documentarlo en `docs/algoritmos/<método>.md`.

### Seguimiento

La lista de los 15 métodos se confirma contra la que envió el Dr. Marrero; la tabla incluye los identificados en la sesión del 22 de septiembre.

| # | Método | Familia | Clase en MEALPY | Estado | Documento |
|:-:|:--|:--|:--|:--|:--|
| 1 | Random Search | Referencia (no es metaheurística) | Implementación propia (`externo:RandomSearch`) | Sumado y documentado | `random_search.md` |
| 2 | Hill Climbing | Trayectoria | `OriginalHC` | Sumado y documentado | `hill_climbing.md` |
| 3 | SA (Simulated Annealing) | Trayectoria | `OriginalSA` | Sumado y documentado | `simulated_annealing.md` |
| 4 | TLBO | Social / humano | `OriginalTLO` | Sumado y documentado | `tlbo.md` |
| 5 | PSO | Enjambre | `OriginalPSO` | Sumado y documentado | `pso.md` |
| 6 | DE | Evolutivo | `OriginalDE` | Sumado y documentado | `differential_evolution.md` |
| 7 | GA | Evolutivo | `BaseGA` (`OriginalGA` no evoluciona en 3.0.3) | Sumado y documentado | `genetic_algorithm.md` |
| 8 | ABC | Enjambre | `OriginalABC` | Sumado y documentado | `abc.md` |
| 9 | ACO (continuo) | Enjambre | `OriginalACOR` | Pendiente | |
| 10 | CMA-ES | Evolutivo | `CMA_ES` | Pendiente | |
| 11–15 | Por completar según la lista acordada | | | | |

"Documentado" significa revisado contra el código de MEALPY 3.0.3; el contraste detallado con cada paper original queda como revisión pendiente.

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
