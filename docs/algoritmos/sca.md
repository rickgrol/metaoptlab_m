# Sine Cosine Algorithm (SCA)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalSCA` · **Revisado:** 17 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Sine Cosine Algorithm (SCA).
- **Clase usada en MEALPY:** `OriginalSCA` (módulo `mealpy/math_based/SCA.py`).
- **Referencia que cita el código de MEALPY:** Mirjalili, S. (2016). *SCA: a sine cosine algorithm for solving optimization problems.* Knowledge-Based Systems, 96, 120–133.
- **Referencia original del método:** la misma.

## 2. Idea del método
Cada solución oscila alrededor del mejor global con funciones seno y coseno. La amplitud de la oscilación disminuye con el tiempo: al inicio las soluciones se mueven lejos del mejor (exploración) y al final se acercan (explotación). Es el representante del paradigma matemático y de oscilaciones de la lista.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalSCA` | Versión básica (Mirjalili, 2016) | Sí |
| `DevSCA` | Versión de los autores de MEALPY | No (solo se documenta) |
| `QleSCA` | Variante con aprendizaje por refuerzo (Q-learning) | No (solo se documenta) |

## 4. Qué implementa (según el código)
Para cada solución y cada dimensión j, en cada época, con `r1 = 2 · (1 − época / total)`:
- `r2 = 2π·U(0, 1)`, `r3 = 2·U(0, 1)`, `r4 = U(0, 1)`;
- si `r4 < 0.5`: `x_j = x_j + r1 · sin(r2) · |r3 · mejor_j − x_j|`;
- si no: `x_j = x_j + r1 · cos(r2) · |r3 · mejor_j − x_j|`.

Las coordenadas fuera de límites se reemplazan por valores aleatorios y la solución solo se actualiza si mejora (selección voraz).

## 5. Parámetros
No tiene parámetros propios además de `pop_size`; la constante a = 2 del programa de r1 está fija en el código, como en el paper.

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `pop_size`.

## 7. Diferencias y observaciones del código
1. **Las ecuaciones de actualización coinciden con el paper** (ecuaciones 3.1–3.4 de Mirjalili, 2016).
2. **Selección voraz añadida.** En el paper, cada solución se mueve siempre a su nueva posición; en MEALPY solo si mejora.
3. **Manejo de límites por reinicio aleatorio** de la coordenada, en lugar del recorte al límite que usa la implementación en MATLAB del autor (verificar).
4. **Programa dependiente del total de épocas.** r1 depende de `época / total`; MetaOptLab-M calibra el número de épocas al presupuesto.
5. **Posible sesgo hacia el centro.** El término `|r3 · mejor − x|` multiplica la posición del mejor por un factor aleatorio, el mismo tipo de operador que en GWO; hay que verificar el sesgo con funciones desplazadas.

## 8. Relación con otros métodos (operadores)
Como GWO, mueve cada solución en función de su distancia a los mejores, con una amplitud que decrece linealmente; la diferencia es que SCA usa un solo líder (el mejor global) y modula el movimiento con seno y coseno. Comparte con PSO la atracción hacia el mejor global, pero sin velocidad ni memoria.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, parámetros por defecto. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 2.697e+01 | 7.411e+07 | 1.316e+02 |

Lugar 10 de 16 en el ranking de Friedman (rango promedio 9.0).

## 10. Dudas pendientes
- Confirmar el sesgo hacia el centro con más corridas.
