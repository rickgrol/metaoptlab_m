# Tabu Search (TS)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalTS` · **Revisado:** 17 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Tabu Search (búsqueda tabú).
- **Clase usada en MEALPY:** `OriginalTS` (módulo `mealpy/math_based/TS.py`).
- **Referencia que cita el código de MEALPY:** Hajji, O., Brisset, S. y Brochet, P. (2004). *A new tabu search method for optimization with continuous parameters.* IEEE Transactions on Magnetics, 40(2), 1184–1187.
- **Referencia original del método:** Glover, F. (1986). *Future paths for integer programming and links to artificial intelligence.* Computers & Operations Research, 13(5), 533–549; y Glover, F. (1989, 1990), *Tabu Search — Part I y Part II*, ORSA Journal on Computing.

## 2. Idea del método
Es una búsqueda local de trayectoria, como Hill Climbing, pero **con memoria**. En cada paso se mueve al mejor vecino aunque sea peor que la solución actual, y guarda en una **lista tabú** los movimientos o soluciones recientes para no regresar a ellos. Así puede salir de un óptimo local sin quedar atrapado en ciclos. Es el representante del patrón de memoria en la lista de métodos.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalTS` | Única versión en MEALPY | Sí |

## 4. Qué implementa (según el código)
En cada época:
1. Genera `neighbour_size` vecinos (10 por defecto) con perturbación gaussiana alrededor de la solución actual: `vecino = actual + normal(0, perturbation_scale)`.
2. Descarta los vecinos que coinciden exactamente con la solución actual o con alguno de la lista tabú.
3. Se mueve al **mejor vecino que queda, aunque sea peor** que la solución actual.
4. Agrega la nueva solución a la lista tabú; si la lista supera `tabu_size` (5), elimina la más antigua.

La mejor solución encontrada se conserva aparte.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Comentario |
|:--|:--|:--|
| `tabu_size` | 5 | Tamaño de la lista tabú |
| `neighbour_size` | 10 | Vecinos por iteración |
| `perturbation_scale` | 0.05 | Desviación del paso, en unidades absolutas del dominio |
| `pop_size` | 2 | No es parámetro del método; solo define cuántas soluciones aleatorias se evalúan al inicio |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `neighbour_size` = 10.

## 7. Diferencias y observaciones del código
1. **La lista tabú no tiene efecto en variables continuas.** La lista guarda las soluciones como tuplas exactas de números reales y descarta un vecino solo si es **idéntico** a una de ellas. Con perturbaciones gaussianas, esa coincidencia prácticamente nunca ocurre. En una prueba de diagnóstico (200 épocas), las 5 soluciones de la lista eran distintas y ningún vecino fue descartado. Las versiones continuas de Tabu Search definen la zona tabú como una vecindad alrededor de las soluciones visitadas, no como el punto exacto; esto debe verificarse en Hajji et al. (2004). En la práctica, `OriginalTS` se comporta como una búsqueda local que siempre se mueve al mejor vecino, sin memoria efectiva.
2. **El paso no se escala al dominio.** Con σ = 0.05 en un dominio [−100, 100], cada paso cubre 0.025 % del rango, por lo que el método casi no se aleja del punto inicial. Es el mismo problema que el SA de MEALPY. En la prueba de diagnóstico, el error en la esfera desplazada seguía en el orden de 10⁴ después de 2 000 evaluaciones.
3. **Se mueve al mejor vecino aunque sea peor.** Esto sí corresponde a Tabu Search y es lo que lo distingue de Hill Climbing; sin una lista tabú efectiva, sin embargo, ese movimiento no está protegido contra ciclos.

## 8. Relación con otros métodos (operadores)
Comparte con Hill Climbing y SA la trayectoria de una sola solución con perturbación aleatoria. Hill Climbing solo acepta mejoras; SA acepta empeoramientos con probabilidad; Tabu Search acepta siempre al mejor vecino y usa **memoria** para evitar regresar. Es el único método de la lista cuyo mecanismo central es la memoria explícita.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, parámetros por defecto. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 3.393e+03 | 4.194e+09 | 7.264e+03 |

Lugar 14 de 16 en el ranking de Friedman (rango promedio 14.3), solo por encima de CMA-ES y Random Search, lo que es coherente con los puntos 7.1 y 7.2.

## 10. Dudas pendientes
- Con la lista tabú sin efecto y el paso sin escalar, `OriginalTS` no representa el patrón de memoria. ¿Se corrige (zona tabú con radio y paso relativo al dominio) o se sustituye por una implementación fiel?
