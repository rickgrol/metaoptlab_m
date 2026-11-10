# SA (Simulated Annealing)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalSA` · **Revisado:** 10 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** SA (Simulated Annealing).
- **Clase usada en MEALPY:** `OriginalSA` (módulo `mealpy/physics_based/SA.py`).
- **Referencia que cita el código de MEALPY:** Kirkpatrick, S., Gelatt, C. D. y Vecchi, M. P. (1983). *Optimization by simulated annealing.* Science, 220(4598), 671–680.
- **Referencia original del método:** la misma (Kirkpatrick et al., 1983); también Černý (1985).

## 2. Idea del método
Búsqueda de trayectoria con una sola solución. En cada paso genera un vecino; si mejora, lo acepta; si empeora, lo acepta con probabilidad exp(−Δ/T). La temperatura T disminuye con el tiempo: al inicio acepta muchos empeoramientos (explora) y al final casi ninguno (intensifica, como un Hill Climbing).

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalSA` | Versión básica de trayectoria | Sí |
| `GaussianSA` | Variante de los autores de MEALPY con enfriamiento geométrico y paso gaussiano | No (solo se documenta) |
| `SwarmSA` | Variante poblacional de los autores de MEALPY | No (solo se documenta) |

## 4. Qué implementa (según el código)
1. Parte de la mejor solución de la población inicial.
2. En cada época genera un vecino: `vecino = actual + normal(0, 1) · step_size`.
3. Si el vecino mejora a la solución actual, se acepta.
4. Si no, se acepta con probabilidad `exp(−|Δf| / T)`, con `T = temp_init / época`.
5. Se conserva siempre la mejor solución encontrada.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Comentario |
|:--|:--|:--|
| `temp_init` | 100 | Temperatura inicial fija, sin calibrar a la escala de la función |
| `step_size` | 0.1 | Desviación del paso, en unidades absolutas del dominio |
| `pop_size` | 2 | Solo define cuántas soluciones aleatorias se evalúan al inicio |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: 1. Con 10 000 evaluaciones hay unas 9 950 épocas.

## 7. Diferencias y observaciones del código
1. **El paso no se escala al dominio.** Con σ = 0.1 en un dominio [−100, 100], cada paso cubre 0.05 % del rango: la búsqueda es casi un paseo local y no puede explorar.
2. **La temperatura inicial no se calibra.** Con T₀ = 100 fijo, el método se comporta distinto según la escala de la función: en funciones con valores del orden de 10⁹ (cec2017:F1) la probabilidad de aceptar empeoramientos es prácticamente cero y SA se reduce a un Hill Climbing; en funciones con valores pequeños acepta casi todo.
3. **El enfriamiento es T₀ / época** (descenso hiperbólico), no el geométrico T_{k+1} = α·T_k más usado en la literatura.
4. **Restricción del validador:** MEALPY limita `epoch` a 100 000; como SA evalúa una vez por época, no podría usar el presupuesto CEC (10 000·D) en D ≥ 20. MetaOptLab-M asigna las épocas después de construir el modelo para evitarlo.
5. **Candidato a implementación propia.** Por los puntos 1 y 2, se justifica usar como alternativa el SA de MetaOptLab (T₀ calibrada por función según Ben-Ameur, 2004, y paso vinculado a la temperatura).

## 8. Relación con otros métodos (operadores)
Comparte con Hill Climbing la trayectoria de una sola solución y la perturbación aleatoria; difiere en el criterio de aceptación probabilístico, controlado por la temperatura.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 1.384e−02 | 1.428e+04 | 1.821e+03 |

## 10. Dudas pendientes
- ¿Se incluye en el estudio el SA de MEALPY, el propio, o ambos?
