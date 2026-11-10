# Optimización Basada en Enseñanza-Aprendizaje (TLBO)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalTLO` · **Revisado:** 10 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Teaching-Learning-Based Optimization (TLBO). En MEALPY se llama TLO.
- **Clase usada en MEALPY:** `OriginalTLO` (módulo `mealpy/human_based/TLO.py`).
- **Referencia que cita el código de MEALPY:** Rao, R. V., Savsani, V. J. y Vakharia, D. P. (2011). *Teaching–learning-based optimization: a novel method for constrained mechanical design optimization problems.* Computer-Aided Design, 43(3), 303–315.
- **Referencia original del método:** la misma.
- **Crítica relevante:** Črepinšek, M., Liu, S.-H. y Mernik, L. (2012). *A note on teaching–learning-based optimization algorithm.* Information Sciences, 212, 79–93.

## 2. Idea del método
La población es un grupo de estudiantes. En la fase del maestro, cada estudiante se acerca al mejor (el maestro) y se aleja de la media del grupo. En la fase del estudiante, cada uno aprende de un compañero al azar: se acerca a él si es mejor, o se aleja si es peor.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalTLO` | Versión básica (Rao et al., 2011) | Sí |
| `DevTLO` | Versión desarrollada por los autores de MEALPY | No (solo se documenta) |
| `ImprovedTLO` | Versión mejorada | No: en MEALPY 3.0.3 no se puede crear con sus valores por defecto |

## 4. Qué implementa (según el código)
Para cada estudiante x_i, en cada época:
1. **Fase del maestro:** `x_nueva = x_i + r·(maestro − T_F·media)`, con r uniforme por dimensión y T_F ∈ {1, 2} al azar; reemplazo voraz.
2. **Fase del estudiante:** elige un compañero x_j; si x_i es mejor, `x_nueva = x_i + r·(x_i − x_j)`; si no, `x_nueva = x_i + r·(x_j − x_i)`; reemplazo voraz.

## 5. Parámetros
No tiene parámetros propios además de `pop_size` (por eso se presenta como "libre de parámetros"; Črepinšek et al. discuten esa afirmación).

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: 2·`pop_size` (una por fase). Al comparar con otros métodos debe usarse el número de evaluaciones, no de épocas: una época de TLBO cuesta el doble que una de PSO.

## 7. Diferencias y observaciones del código
1. **Fases intercaladas por estudiante.** En el original, la fase del maestro se aplica a todo el grupo y después la del estudiante; aquí cada estudiante pasa por ambas fases antes del siguiente, y la media se recalcula con los cambios.
2. **Sin eliminación de duplicados**, que sí aparece en algunas descripciones del método original.
3. **Posible sesgo hacia el centro del espacio:** en la prueba de funcionamiento del catálogo obtuvo errores mucho menores en la esfera centrada en el origen que en la desplazada. Está por confirmar con más corridas.

## 8. Relación con otros métodos (operadores)
La fase del maestro es una atracción hacia el mejor, como el término social de PSO; la fase del estudiante es un movimiento por diferencia entre dos soluciones, como en DE y ABC.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 1.354e−06 | 8.036e+02 | 3.209e+01 |

## 10. Dudas pendientes
- Confirmar el sesgo hacia el centro con funciones desplazadas y rotadas.
