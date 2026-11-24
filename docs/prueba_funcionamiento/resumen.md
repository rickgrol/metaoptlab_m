# Prueba de funcionamiento del catálogo de MEALPY 3.0.3

Función builtin:esfera_desplazada, D = 10, 1000·D evaluaciones, población 50, dos corridas con la misma semilla.

| Categoría | Número |
|:--|--:|
| utilizable | 204 |
| consumo_variable | 10 |
| fuera_de_limites | 7 |
| no_reproducible | 6 |
| no_se_puede_crear | 5 |
| no_evoluciona | 2 |
| **Total** | **234** |

## Excluidos

| Algoritmo | Categoría | Detalle |
|:--|:--|:--|
| AAO | no_reproducible | 8191.91 vs 8630.84 |
| DS_GWO | no_evoluciona | usa 50 de 10000 evaluaciones |
| DevCHIO | no_se_puede_crear | ValueError: 'max_age' is an integer and value should be in range: [1, 3]. |
| DevDMOA | consumo_variable | usa 9000 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| DevEPC | consumo_variable | usa 9553 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| DevFOA | fuera_de_limites | 44 evaluaciones fuera de límites |
| EnhancedTWO | fuera_de_limites | 40 evaluaciones fuera de límites |
| HI_WOA | no_se_puede_crear | ValueError: 'feedback_max' is an integer and value should be in range: [2, 7]. |
| JADE | no_reproducible | 8.26406e-08 vs 3.83362e-09 |
| L_SHADE | no_reproducible | 1.07855e-09 vs 8.6139e-11 |
| LevyTWO | fuera_de_limites | 180 evaluaciones fuera de límites |
| OCRO | no_se_puede_crear | ValueError: 'restart_count' is an integer and value should be in range: [2, 5]. |
| OppoTWO | fuera_de_limites | 2768 evaluaciones fuera de límites |
| OriginalArchOA | fuera_de_limites | 7551 evaluaciones fuera de límites |
| OriginalBCO | no_se_puede_crear | ValueError: 'n_chemotaxis' is an integer and value should be in range: (1, 5). |
| OriginalCHIO | no_se_puede_crear | ValueError: 'max_age' is an integer and value should be in range: [1, 3]. |
| OriginalEOA | consumo_variable | usa 9994 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| OriginalEVO | consumo_variable | usa 8814 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| OriginalFOA | fuera_de_limites | 44 evaluaciones fuera de límites |
| OriginalGA | no_evoluciona | usa 50 de 10000 evaluaciones |
| OriginalHHO | consumo_variable | usa 9326 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| OriginalIWO | consumo_variable | usa 8290 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| OriginalLSHADEcnEpSin | no_reproducible | 1.75183e-13 vs 3.73218e-14 |
| OriginalPSS | no_reproducible | 50.7673 vs 37.6341 |
| OriginalSFO | consumo_variable | usa 9775 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| OriginalSHADE | no_reproducible | 1.38079e-09 vs 5.77078e-10 |
| OriginalSHO | consumo_variable | usa 9507 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| OriginalWCA | consumo_variable | usa 9914 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| SAP_DE | consumo_variable | usa 5610 de 10000 evaluaciones: sus evaluaciones por época varían y termina antes del presupuesto |
| WhaleFOA | fuera_de_limites | 44 evaluaciones fuera de límites |
