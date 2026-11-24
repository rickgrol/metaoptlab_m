# Grey Wolf Optimizer (GWO)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalGWO` · **Revisado:** 17 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Grey Wolf Optimizer (GWO).
- **Clase usada en MEALPY:** `OriginalGWO` (módulo `mealpy/swarm_based/GWO.py`).
- **Referencia que cita el código de MEALPY:** Mirjalili, S., Mirjalili, S. M. y Lewis, A. (2014). *Grey wolf optimizer.* Advances in Engineering Software, 69, 46–61.
- **Referencia original del método:** la misma.

## 2. Idea del método
Inspirado en la jerarquía y la caza de los lobos grises. Los tres mejores individuos (alfa, beta y delta) guían a la manada: cada lobo calcula una posición hacia cada uno de los tres y se mueve al promedio. Un coeficiente `a`, que decrece de 2 a 0, controla la transición de exploración (rodear a la presa desde lejos) a explotación (atacar).

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalGWO` | Versión básica (Mirjalili et al., 2014) | Sí |
| `RW_GWO`, `GWO_WOA`, `IGWO`, `ChaoticGWO`, `FuzzyGWO`, `IncrementalGWO`, `ExGWO`, `DS_GWO` y otras | Variantes e hibridaciones | No (solo se documentan). `DS_GWO` además no evoluciona en 3.0.3 |

## 4. Qué implementa (según el código)
En cada época, con `a = 2 − 2 · época / total`:
1. Identifica alfa, beta y delta (los tres mejores de la población).
2. Para cada lobo y cada líder L: `A = a · (2·r − 1)`, `C = 2·r`, `X_L = L − A · |C · L − x|`, con r uniforme por dimensión.
3. Nueva posición: `x_nueva = (X_alfa + X_beta + X_delta) / 3`.
4. **Selección voraz:** el lobo solo se mueve si mejora.

## 5. Parámetros
No tiene parámetros propios además de `pop_size`; el coeficiente `a` sigue el programa lineal de 2 a 0.

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `pop_size`.

## 7. Diferencias y observaciones del código
1. **Selección voraz añadida.** En Mirjalili et al. (2014) cada lobo se mueve siempre a su nueva posición; en MEALPY solo si mejora. Es una variante elitista.
2. **Programa dependiente del total de épocas.** El coeficiente `a` depende de `época / total`, por lo que el número de épocas debe corresponder al presupuesto (MetaOptLab-M lo calibra).
3. **Sesgo hacia el centro del espacio.** La regla `|C · L − x|` multiplica la posición del líder por un factor aleatorio; en la literatura se ha señalado que GWO tiende a converger hacia el origen y por eso obtiene resultados excelentes en funciones con el óptimo en el centro (Kudela, 2022, *Nature Machine Intelligence*; Camacho-Villalón, Dorigo y Stützle, 2023). En la prueba de funcionamiento del catálogo, GWO quedó entre los algoritmos con sospecha de este sesgo. Por eso solo deben usarse funciones desplazadas para evaluarlo.

## 8. Relación con otros métodos (operadores)
Como PSO, se guía por los mejores individuos, pero usa tres líderes en lugar del mejor global y no tiene velocidad ni memoria personal. Comparte con SCA y ASO un coeficiente que decrece con el avance de las épocas para pasar de explorar a explotar. Las críticas a GWO lo describen como una variante de PSO con una metáfora nueva, lo que lo hace un buen caso para la discusión sobre metáforas en el paper.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, parámetros por defecto. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 1.931e+00 | 9.675e+05 | 1.044e+02 |

Empatado en el lugar 5 de 16 en el ranking de Friedman (rango promedio 6.3, igual que ABC). Las funciones de la prueba están desplazadas, por lo que el resultado no se beneficia del sesgo hacia el centro.

## 10. Dudas pendientes
- Confirmar el sesgo hacia el centro comparando la esfera centrada y la desplazada con más corridas.
