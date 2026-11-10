# Optimización por Enjambre de Partículas (PSO)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalPSO` · **Revisado:** 10 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Particle Swarm Optimization (PSO).
- **Clase usada en MEALPY:** `OriginalPSO` (módulo `mealpy/swarm_based/PSO.py`).
- **Referencia que cita el código de MEALPY:** Kennedy, J. y Eberhart, R. (1995). *Particle swarm optimization.* Proceedings of ICNN'95, vol. 4, 1942–1948.
- **Referencia del peso de inercia:** Shi, Y. y Eberhart, R. (1998). *A modified particle swarm optimizer.* IEEE International Conference on Evolutionary Computation.

## 2. Idea del método
Una población de partículas se mueve por el espacio. Cada partícula tiene una velocidad que combina tres términos: su inercia, la atracción hacia su mejor posición personal y la atracción hacia la mejor posición del enjambre.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalPSO` | Versión básica con peso de inercia fijo | Sí |
| `AIW_PSO`, `LDW_PSO`, `P_PSO`, `HPSO_TVAC`, `C_PSO`, `CL_PSO` | Variantes con inercia adaptativa o decreciente, coeficientes variables, caos o aprendizaje integral | No (solo se documentan) |

## 4. Qué implementa (según el código)
Para cada partícula, en cada época:
1. `v = w·v + c1·r1·(p_mejor − x) + c2·r2·(g_mejor − x)`, con r1 y r2 uniformes por dimensión.
2. `x_nueva = x + v`; las coordenadas fuera de límites se reemplazan por un valor aleatorio dentro del dominio.
3. Se evalúa x_nueva. **La partícula solo se mueve si x_nueva mejora su posición actual**; la mejor posición personal se actualiza aparte.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Valor en la literatura |
|:--|:--|:--|
| `c1`, `c2` | 2.05 | 2.0 en Kennedy y Eberhart (1995) |
| `w` | 0.4 fijo | No existe en 1995; en Shi y Eberhart (1998) suele decrecer de 0.9 a 0.4 |
| `pop_size` | 100 | 20–50 es lo habitual |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `pop_size`.

## 7. Diferencias y observaciones del código
1. **Movimiento voraz.** En el PSO canónico la partícula siempre se mueve a su nueva posición y la memoria del mejor personal guarda lo bueno. En MEALPY la partícula solo se mueve si mejora: es una variante elitista que reduce la exploración.
2. **"Original" mezcla dos versiones.** El peso de inercia no existe en el PSO de 1995; lo introdujeron Shi y Eberhart en 1998, y suele ser decreciente, no fijo.
3. **Sin límite de velocidad.** El código calcula `v_max = 0.5·(ub − lb)` pero solo lo usa para inicializar las velocidades; durante la búsqueda la velocidad no se acota.
4. **Manejo de límites por reinicio aleatorio** de la coordenada que sale del dominio.

## 8. Relación con otros métodos (operadores)
Comparte con DE el uso de diferencias entre posiciones para moverse; difiere en que PSO tiene memoria (mejor personal y velocidad) y DE no. La selección voraz de esta implementación lo acerca a un esquema elitista como el de DE.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 7.007e−16 | 2.876e+03 | 5.671e+01 |

## 10. Dudas pendientes
- ¿Usamos `OriginalPSO` tal cual o fijamos parámetros del PSO estándar (por ejemplo, el SPSO 2011)?
