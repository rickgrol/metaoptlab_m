# Atom Search Optimization (ASO)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalASO` · **Revisado:** 17 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Atom Search Optimization (ASO).
- **Clase usada en MEALPY:** `OriginalASO` (módulo `mealpy/physics_based/ASO.py`).
- **Referencia que cita el código de MEALPY:** Zhao, W., Wang, L. y Zhang, Z. (2019). *Atom search optimization and its application to solve a hydrogeologic parameter estimation problem.* Knowledge-Based Systems, 163, 283–304.
- **Referencia original del método:** la misma. El código de MEALPY también enlaza la implementación en MATLAB de los autores.

## 2. Idea del método
Inspirado en la dinámica molecular. Cada solución es un átomo con masa (mayor cuanto mejor es su valor). Los átomos interactúan con los K mejores mediante una fuerza derivada del potencial de Lennard-Jones (atracción a distancia, repulsión a corta distancia) y además están sujetos a una restricción que los atrae hacia el mejor átomo. La aceleración resultante, dividida entre la masa, actualiza la velocidad y la posición. Es el representante químico/físico de la lista.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalASO` | Única versión en MEALPY | Sí |

## 4. Qué implementa (según el código)
En cada época:
1. **Masa:** a partir del valor de cada átomo, normalizada para que sume 1.
2. **K mejores:** K disminuye de N a 2 con la raíz del avance (época / total de épocas).
3. **Aceleración:** para cada átomo, suma de las fuerzas de Lennard-Jones hacia los K mejores, ponderadas por un factor aleatorio por dimensión, más `beta · (mejor − átomo)`; se multiplica por `G = exp(−20 · época / total)` y se divide entre la masa.
4. **Velocidad y posición:** `v = rand · v + a`, `x = x + v`; las coordenadas fuera de límites se reemplazan por valores aleatorios.
5. **Selección voraz:** el átomo solo se mueve si mejora.
6. Si el mejor global no mejoró, se reinserta en una posición aleatoria de la población.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Comentario |
|:--|:--|:--|
| `alpha` | 10 | Peso de profundidad del potencial |
| `beta` | 0.2 | Peso de la atracción hacia el mejor |
| `pop_size` | 100 | Número de átomos |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `pop_size`.

## 7. Diferencias y observaciones del código
1. **El centro de los K mejores se calcula como un escalar.** La línea `mk_average = np.mean([agent.solution for agent in k_best_pop])` no indica el eje, así que promedia **todas las coordenadas de todos los átomos** y produce un solo número. La distancia media de cada átomo, que regula el potencial, se mide entonces contra el punto (m, m, …, m) y no contra el centro de los K mejores. Debería ser `np.mean(..., axis=0)`.
2. **Selección voraz y reinserción del mejor.** El átomo solo se mueve si mejora, y el mejor global se reinserta si la población no lo superó. Verificar contra el paper si estos dos mecanismos forman parte del ASO original.
3. **Programa interno dependiente del total de épocas.** K, G y el potencial dependen de `época / total`, por lo que el número de épocas debe corresponder al presupuesto (MetaOptLab-M lo calibra).

## 8. Relación con otros métodos (operadores)
Como PSO, usa velocidad e inercia y una atracción hacia el mejor global; a diferencia de PSO, la fuerza depende de la distancia (atracción o repulsión según el potencial) y de la masa, y no hay memoria del mejor personal. Comparte con GWO y SCA la reducción programada de la exploración con el avance de las épocas.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, parámetros por defecto. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 2.266e+03 | 2.529e+09 | 3.002e+03 |

Lugar 13 de 16 en el ranking de Friedman (rango promedio 13.0).

## 10. Dudas pendientes
- El error del centro de masa (punto 7.1) cambia el comportamiento del potencial. ¿Se corrige y documenta?
