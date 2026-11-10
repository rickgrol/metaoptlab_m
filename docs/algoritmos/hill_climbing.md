# Hill Climbing (HC)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalHC` · **Revisado:** 10 de noviembre de 2026

## 1. Identificación
- **Método básico:** Hill Climbing (búsqueda local por ascenso de colina).
- **Clase usada en MEALPY:** `OriginalHC` (módulo `mealpy/math_based/HC.py`, MEALPY 3.0.3).
- **Referencia que cita el código de MEALPY:** Mitchell, M., Holland, J. y Forrest, S. (1993). *When will a genetic algorithm outperform hill climbing.* Advances in Neural Information Processing Systems, 6.
- **Referencia original del método:** por definir. HC es un método clásico sin un único paper fundacional; conviene acordar con el Dr. Marrero qué referencia usar.

## 2. Idea del método
Parte de una solución y, en cada paso, prueba soluciones cercanas ("vecinos"). Si alguna es mejor, se mueve a ella; si ninguna mejora, se queda donde está. Solo acepta mejoras, por eso es un método voraz: encuentra rápido un óptimo local, pero no tiene mecanismo para escapar de él.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalHC` | Versión básica: una solución, muchos vecinos por paso | Sí |
| `SwarmHC` | Variante propia de los autores de MEALPY: varios escaladores en paralelo | No (solo se documenta) |

## 4. Qué implementa (según el código)
En cada época:
1. Calcula el tamaño de paso: `paso = exp(−2 · época / total_de_épocas)`. Empieza en 1 y baja hasta e⁻² ≈ 0.135.
2. Genera `neighbour_size` vecinos (50 por defecto) alrededor del **mejor global**:
   `vecino = mejor_global + uniforme(lb, ub) · paso`
3. Corrige los vecinos que salen de los límites.
4. Evalúa los vecinos; el mejor global se actualiza si alguno lo mejora.

Es un *hill climbing de ascenso más empinado estocástico*: no recorre todos los vecinos posibles, sino una muestra aleatoria, y se queda con el mejor.

## 5. Parámetros
| Parámetro        | Valor por defecto en MEALPY          | Valor en el paper original                                                                                           |
| :--------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| `neighbour_size` | 50                                   | por revisar                                                                                                          |
| `pop_size`       | 2                                    | no aplica: solo determina cuántas soluciones aleatorias se evalúan al inicio; la búsqueda parte de la mejor de ellas |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size` (50 en nuestra configuración).
- Evaluaciones por época: `neighbour_size` = 50.
- Con un presupuesto de 10 000 evaluaciones caben unas 200 épocas.

## 7. Diferencias y observaciones del código
1. **La referencia citada no describe este algoritmo.** Mitchell, Holland y Forrest (1993) estudian un hill climbing de mutación aleatoria sobre cadenas binarias; `OriginalHC` es una versión continua distinta.
2. **La perturbación se sortea en el intervalo del dominio, no en un intervalo centrado en cero.**
   El código genera cada vecino como `mejor_global + uniforme(lb, ub) · paso`. La distribución es uniforme, pero el intervalo de sorteo es el dominio del problema `[lb, ub]`.
   - Con un dominio simétrico, como [−100, 100], los valores sorteados son mitad negativos y mitad positivos, de modo que el vecino puede quedar a cualquier lado del punto actual. Las funciones de nuestras pruebas tienen dominios simétricos, así que no se vieron afectadas.
   - Con un dominio no centrado en cero, como [0, 10], todos los valores sorteados son positivos y cada vecino queda siempre "a la derecha" del punto actual. El algoritmo solo puede aumentar las coordenadas. Por ejemplo, si el óptimo está en x = 2 y la búsqueda arranca en x = 7, nunca podrá llegar a él.
   - Lo esperable es sortear en un intervalo centrado en cero, por ejemplo `uniforme(−1, 1) · (ub − lb)`, para que la perturbación sea simétrica sin importar dónde esté el dominio.
1. **El paso mínimo es grande.** Al final de la búsqueda el factor de paso es e⁻² ≈ 0.135; en [−100, 100] eso permite saltos de hasta ±13.5, por lo que el método no puede afinar cerca del óptimo. Esto explica los errores altos aun en la esfera.
2. **La reducción del paso no es parte del HC clásico.** En el HC original el vecindario tiene un radio fijo; la reducción exponencial `exp(−2 · época / total_de_épocas)` es una decisión de diseño de MEALPY. Como depende del total de épocas, el número de épocas debe corresponder al presupuesto (MetaOptLab-M lo calibra automáticamente).

## 8. Relación con otros métodos (operadores)
Comparado con Recocido Simulado (SA): ambos trabajan con una sola solución y generan candidatos con perturbación aleatoria. La diferencia esencial es el **criterio de aceptación**: HC solo acepta mejoras; SA también acepta empeoramientos con probabilidad exp(−Δ/T), y esa probabilidad disminuye conforme baja la temperatura T, lo que le permite escapar de óptimos locales al inicio e intensificar al final.

## 9. Resultados de la prueba reducida

| Función | Mediana del error |
|:--|:--|
| Esfera desplazada | 1.614e+02 |
| cec2017:F1 | 1.936e+08 |
| cec2017:F4 | 3.127e+02 |

Prueba reducida: 5 corridas, D = 10, 1 000·D evaluaciones.

## 10. Dudas pendientes
- ¿Qué referencia usar como original de HC?
- ¿Tiene sentido incluir `SwarmHC` en el estudio masivo, siendo una variante no publicada?
