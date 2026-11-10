# Teaching-Learning-Based Optimization (TLBO)

> Pendiente de revisión. Por ahora solo contiene lo verificado en el código de MEALPY 3.0.3.

## 1. Identificación
- **Método básico:** TLBO.
- **Clase usada en MEALPY:** `OriginalTLO` (módulo `mealpy/human_based/TLO.py`). En MEALPY se llama TLO, no TLBO.
- **Referencia que cita el código:** Rao, R.V., Savsani, V.J. y Vakharia, D.P. (2011). *Teaching–learning-based optimization: a novel method for constrained mechanical design optimization problems.* Computer-Aided Design, 43(3), 303–315.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalTLO` | Versión básica (Rao et al., 2011) | Sí |
| `DevTLO` | Versión desarrollada por los autores de MEALPY | No (solo se documenta) |
| `ImprovedTLO` | Versión mejorada | No: en MEALPY 3.0.3 no se puede crear con sus valores por defecto (`n_teachers`) |

## 4. Qué implementa (según el código) — por revisar
Dos fases por época, para cada estudiante:
1. **Fase del maestro:** se mueve hacia el mejor global, alejándose de la media de la clase multiplicada por un factor de enseñanza TF ∈ {1, 2}.
2. **Fase del estudiante:** se compara con un compañero al azar y se acerca a él si es mejor, o se aleja si es peor.

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size` (50).
- Evaluaciones por época: 2 · `pop_size` = 100 (una por fase).

## 7. Observaciones preliminares
- En el cribado del catálogo, `OriginalTLO` mostró señales de sesgo hacia el centro del espacio (error mucho menor en la esfera centrada en el origen que en la desplazada). Por confirmar.

## 9. Resultados de la prueba reducida

## 10. Dudas pendientes
