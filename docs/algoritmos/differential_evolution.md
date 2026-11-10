# Evolución Diferencial (DE)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalDE` · **Revisado:** 10 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Differential Evolution (DE).
- **Clase usada en MEALPY:** `OriginalDE` (módulo `mealpy/evolutionary_based/DE.py`).
- **Referencia que cita el código de MEALPY:** Mohamed, A. W., Hadi, A. A. y Jambi, K. M. (2019). *Novel mutation strategy for enhancing SHADE and LSHADE algorithms for global numerical optimization.* Swarm and Evolutionary Computation, 50, 100455.
- **Referencia original del método:** Storn, R. y Price, K. (1997). *Differential evolution – a simple and efficient heuristic for global optimization over continuous spaces.* Journal of Global Optimization, 11, 341–359.

## 2. Idea del método
Población de vectores. Para cada vector se crea un mutante sumando a otro vector la diferencia escalada de dos más; luego se cruza con el vector original y el resultado lo reemplaza solo si es mejor.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalDE` | Versión básica con seis estrategias de mutación (por defecto, la 0) | Sí |
| `JADE`, `SADE`, `SAP_DE` | Variantes adaptativas | No (solo se documentan) |
| `OriginalSHADE`, `L_SHADE` | Variantes adaptativas con historial; L-SHADE ganó CEC 2014 | Candidatos a algoritmos campeones |

## 4. Qué implementa (según el código), estrategia por defecto
Para cada vector x_i:
1. Mutación: `v = x_r1 + F·(x_r2 − x_r3)`, con r1, r2, r3 distintos entre sí y de i.
2. Cruce binomial: cada componente se toma de v con probabilidad CR y de x_i en otro caso.
3. Selección: el vector de prueba reemplaza a x_i **en ese mismo momento** si es mejor.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Valor en Storn y Price (1997) |
|:--|:--|:--|
| `wf` (F) | 0.1 | 0.5 como punto de partida; rango usual [0.4, 1.0] |
| `cr` (CR) | 0.9 | 0.1 a 1.0 según el problema; 0.9 es común |
| `strategy` | 0 | DE/rand/1/bin |
| `pop_size` | 100 | 5·D a 10·D |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `pop_size`.

## 7. Diferencias y observaciones del código
1. **F = 0.1 por defecto.** Es muy bajo: las mutaciones son tan pequeñas que la población converge prematuramente. Explica que DE quede por debajo de Hill Climbing en la prueba.
2. **La estrategia 0 está mal etiquetada.** La documentación de MEALPY dice "DE/current-to-rand/1/bin", pero el código implementa DE/rand/1/bin.
3. **Falta la componente garantizada del cruce.** En el DE original, al menos una componente (índice j_rand) se toma siempre del mutante; aquí, con probabilidad (1 − CR)^D el vector de prueba es idéntico al original y se desperdicia una evaluación.
4. **Reemplazo inmediato (asíncrono).** En el DE clásico, la nueva población se forma al final de la generación; aquí cada reemplazo afecta a los siguientes vectores de la misma generación.
5. **La referencia citada no es la del método original**, sino un trabajo de 2019 sobre variantes de SHADE.

## 8. Relación con otros métodos (operadores)
Tiene los mismos nombres de operadores que GA (mutación, cruce, selección) pero en orden inverso y con significado distinto: en DE la mutación es diferencial y va primero; en GA el cruce va primero y la mutación es una perturbación pequeña.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, parámetros por defecto. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 7.011e+02 | 1.350e+09 | 1.560e+03 |

## 10. Dudas pendientes
- ¿Usamos F = 0.1 (por defecto) o los valores de Storn y Price (F = 0.5, CR = 0.9)?
