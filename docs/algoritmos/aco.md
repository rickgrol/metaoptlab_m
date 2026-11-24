# Optimización por Colonia de Hormigas para dominios continuos (ACO_R)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalACOR` · **Revisado:** 16 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Ant Colony Optimization (ACO). El ACO original (Dorigo, 1992) es para problemas combinatorios; la versión para variables continuas es ACO_R.
- **Clase usada en MEALPY:** `OriginalACOR` (módulo `mealpy/swarm_based/ACOR.py`).
- **Referencia que cita el código de MEALPY:** Socha, K. y Dorigo, M. (2008). *Ant colony optimization for continuous domains.* European Journal of Operational Research, 185(3), 1155–1173.
- **Referencia original del método:** la misma (ACO_R); para el ACO combinatorio, Dorigo, M., Maniezzo, V. y Colorni, A. (1996). *Ant system: optimization by a colony of cooperating agents.* IEEE Transactions on Systems, Man, and Cybernetics, Part B, 26(1), 29–41.

## 2. Idea del método
En lugar de feromona sobre aristas, ACO_R mantiene un **archivo** con las k mejores soluciones. Cada solución del archivo define una gaussiana centrada en ella; el conjunto forma una mezcla de gaussianas que hace el papel de la feromona. Las hormigas generan soluciones nuevas muestreando esa mezcla, eligiendo con mayor probabilidad las gaussianas de las mejores soluciones. Las soluciones nuevas se agregan al archivo y se conservan las k mejores.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalACOR` | Única versión en MEALPY (ACO_R) | Sí |

MEALPY no incluye el ACO combinatorio original; para optimización continua, ACO_R es la versión de referencia.

## 4. Qué implementa (según el código)
En cada época:
1. **Pesos por rango:** con el archivo ordenado, el peso de la solución de rango l es `w_l = exp(−(l−1)² / (2 q² k²)) / (q k √(2π))`; se normalizan para obtener probabilidades. Un q pequeño concentra la elección en las mejores soluciones (intensificación).
2. **Desviaciones:** para cada solución l y dimensión j, `σ_lj = ξ · Σ_e |x_ej − x_lj| / (k − 1)`, es decir, ξ veces la distancia media a las demás soluciones del archivo en esa dimensión.
3. **Muestreo:** se generan `sample_count` soluciones nuevas; para cada dimensión se elige una solución del archivo por ruleta y se muestrea `x_j = x_lj + normal(0, 1) · σ_lj`.
4. **Actualización del archivo:** se unen archivo y soluciones nuevas, se ordenan y se conservan las k mejores.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Valor en Socha y Dorigo (2008) |
|:--|:--|:--|
| `pop_size` (k, tamaño del archivo) | 100 | 50 |
| `sample_count` (m, hormigas por iteración) | 25 | 2 |
| `intent_factor` (q) | 0.5 | 10⁻⁴ en la mayoría de los experimentos |
| `zeta` (ξ) | 1.0 | 0.85 |

Los valores del paper deben verificarse en la tabla de parámetros del artículo.

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `sample_count` (25 por defecto).

## 7. Diferencias y observaciones del código
1. **La gaussiana se elige por dimensión, no por solución.** En Socha y Dorigo (2008), cada hormiga elige **una** gaussiana (una solución del archivo) y muestrea **todas** las dimensiones alrededor de ella. En MEALPY la ruleta se aplica en cada dimensión, de modo que una solución nueva combina coordenadas de soluciones distintas del archivo. Es un operador de recombinación que el original no tiene.
2. **Parámetros por defecto muy distintos.** Con q = 0.5 la selección de soluciones es casi uniforme sobre el archivo (exploratoria); el paper usa q ≈ 10⁻⁴, que concentra la búsqueda en la mejor solución. Con m = 25 en lugar de 2, cada época cuesta 12 veces más evaluaciones.
3. **La desviación incluye la propia solución en la suma** (con distancia cero) y divide entre k − 1, lo que coincide con la fórmula del paper.
4. **Elitismo completo:** el archivo conserva siempre las k mejores soluciones encontradas, como en el original.

## 8. Relación con otros métodos (operadores)
Comparte con CMA-ES la idea de **muestrear de un modelo probabilístico** que se ajusta a las buenas soluciones (aquí, una mezcla de gaussianas; en CMA-ES, una sola gaussiana multivariada). La selección por rango con pesos es análoga a la recombinación ponderada de CMA-ES. Con la ruleta por dimensión de MEALPY, el operador también se parece al cruce uniforme del GA.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, parámetros por defecto. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 6.258e−03 | 2.949e+05 | 4.888e+01 |

Lugar 3 de 16 en el ranking de Friedman (rango promedio 3.7), detrás de TLBO y PSO.

## 10. Dudas pendientes
- ¿Usamos los parámetros por defecto de MEALPY o los del paper (k = 50, m = 2, q = 10⁻⁴, ξ = 0.85)?
- La ruleta por dimensión cambia el operador; ¿se corrige para que sea fiel al original?
