# Algoritmo Genético (GA)

> **Versión revisada:** MEALPY 3.0.3, clase `BaseGA` · **Revisado:** 10 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Genetic Algorithm (GA), en codificación real.
- **Clase usada en MEALPY:** `BaseGA` (módulo `mealpy/evolutionary_based/GA.py`).
- **Referencia que cita el código de MEALPY:** Whitley, D. (1994). *A genetic algorithm tutorial.* Statistics and Computing, 4(2), 65–85.
- **Referencia original del método:** Holland, J. H. (1975). *Adaptation in Natural and Artificial Systems.* University of Michigan Press.

## 2. Idea del método
Población de soluciones que evoluciona por selección de padres, cruce y mutación; los hijos compiten con la población anterior para formar la siguiente generación.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `BaseGA` | Versión básica | Sí |
| `OriginalGA` | Clase nueva en 3.0.3 | No: no implementa el método de evolución (ver punto 7.4) |
| `SingleGA`, `MultiGA`, `EliteSingleGA`, `EliteMultiGA` | Variantes de los autores de MEALPY | No (solo se documentan) |

## 4. Qué implementa (según el código)
En cada época, se generan `pop_size` hijos por pares:
1. **Selección de padres:** torneo con el 20 % de la población.
2. **Cruce uniforme** con probabilidad `pc`: cada gen se toma de uno u otro padre al azar.
3. **Mutación:** cada gen se reemplaza por un valor aleatorio del dominio con probabilidad `pm`.
4. **Supervivencia:** cada hijo compite con el peor de un torneo del 10 % de la población anterior; pasa el mejor de los dos.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Comentario |
|:--|:--|:--|
| `pc` | 0.95 | Probabilidad de cruce |
| `pm` | 0.025 | Probabilidad de mutación por gen |
| selección | torneo, k = 20 % | También ruleta o aleatoria |
| cruce | uniforme | También un punto, dos puntos o aritmético |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `pop_size`.

## 7. Diferencias y observaciones del código
1. **Codificación real, no binaria.** El GA de Holland y el tutorial de Whitley trabajan con cadenas binarias; `BaseGA` aplica los operadores directamente sobre números reales.
2. **Mutación por reinicio aleatorio del gen** ("flip"), no una perturbación pequeña alrededor del valor actual. Es exploratoria pero no ayuda a afinar.
3. **Supervivencia con elitismo implícito:** los hijos reemplazan a individuos malos, no a toda la población, de modo que las buenas soluciones se conservan.
4. **`OriginalGA` no funciona en 3.0.3.** La clase solo define `__init__` y no implementa `evolve`, de modo que hereda el método vacío de la clase base `Optimizer`: el ciclo de épocas corre, pero la población nunca cambia y el resultado es la mejor solución aleatoria inicial. No genera ningún error. Por eso se usa `BaseGA`, la versión base que aparece en el artículo de MEALPY (2023).

## 8. Relación con otros métodos (operadores)
Ver Evolución Diferencial: mismos nombres de operadores, distinto orden y significado.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 5.888e+00 | 5.986e+06 | 8.536e+01 |

## 10. Dudas pendientes
- ¿Conviene una variante con cruce y mutación para codificación real (por ejemplo, SBX y mutación polinomial), más común en la literatura actual?
