# Estimation of Distribution Algorithm (EDA)

> **Implementación propia:** `bench/externos/eda.py` (variante UMDA_c) · **Revisado:** 17 de noviembre de 2026 · **Estado:** implementación propia; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Estimation of Distribution Algorithm (EDA), algoritmo de estimación de distribuciones.
- **Clase en MEALPY:** no existe en MEALPY 3.0.3.
- **Implementación:** propia, en `bench/externos/eda.py`; se declara en el YAML como `externo:EDA`. Corre con el mismo contador de evaluaciones que los algoritmos de MEALPY.
- **Variante implementada:** UMDA_c (Univariate Marginal Distribution Algorithm, versión continua), la forma más simple de EDA para variables continuas.
- **Referencias:** Larrañaga, P. y Lozano, J. A. (Eds.) (2002). *Estimation of Distribution Algorithms: A New Tool for Evolutionary Computation.* Kluwer Academic Publishers. Larrañaga, P., Etxeberria, R., Lozano, J. A. y Peña, J. M. (2000). *Optimization in continuous domains by learning and simulation of Gaussian networks.* GECCO 2000 Workshop. El UMDA original para variables discretas es de Mühlenbein y Paaß (1996).

## 2. Idea del método
En lugar de cruzar y mutar soluciones, un EDA **aprende un modelo probabilístico** de las mejores soluciones y genera la siguiente población muestreando de ese modelo. Es el representante del paradigma probabilístico de la lista.

## 3. Variantes y cuál se toma
| Variante | Qué es | ¿Se usa? |
|:--|:--|:--|
| UMDA_c | Una normal independiente por dimensión | Sí (implementación propia) |
| EMNA, EGNA | Normal multivariada o red gaussiana: modelan dependencias entre variables | No |

Se eligió UMDA_c por ser la versión básica: es al EDA lo que la versión original es a los demás métodos de la lista.

## 4. Qué implementa
1. Genera N soluciones uniformes en el dominio y las evalúa.
2. Selecciona por truncamiento las k = 50 % mejores.
3. Estima, para cada dimensión, la media y la desviación estándar de las seleccionadas.
4. Muestrea N soluciones nuevas de esas normales independientes; las coordenadas fuera del dominio se recortan al límite.
5. Repite desde el paso 2 hasta agotar el presupuesto.

## 5. Parámetros
| Parámetro | Valor usado | Comentario |
|:--|:--|:--|
| `pop_size` (N) | el de la configuración (50) | Tamaño de la población |
| `seleccion` | 0.5 | Fracción seleccionada por truncamiento |

## 6. Costo por generación
- Evaluaciones en la inicialización: N.
- Evaluaciones por generación: N.

## 7. Decisiones de implementación y limitaciones
1. **Modelo univariado.** Ignora las dependencias entre variables, por lo que se espera que funcione peor en funciones rotadas (como las de CEC2017) que en funciones separables.
2. **Sin elitismo ni mínimo de varianza.** Siguiendo la forma básica, la población se reemplaza completa y la desviación estándar puede reducirse hasta colapsar, lo que causa convergencia prematura. Las variantes posteriores agregan elitismo o un mínimo de varianza.
3. **Manejo de límites por recorte** al borde del dominio; es una decisión propia, no del método.

## 8. Relación con otros métodos (operadores)
Pertenece, con CMA-ES y ACO_R, a los métodos que muestrean de un modelo probabilístico. UMDA_c usa una normal sin correlaciones; CMA-ES usa una normal multivariada que aprende la covarianza y adapta el tamaño de paso; ACO_R usa una mezcla de normales centradas en las soluciones del archivo.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, parámetros por defecto. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 8.224e−08 | 1.327e+08 | 4.995e+00 |

Lugar 4 de 16 en el ranking de Friedman (rango promedio 4.3). Obtuvo el mejor resultado de los 16 métodos en cec2017:F4 y quedó muy por detrás en cec2017:F1, una función rotada y mal condicionada; es lo esperable de un modelo univariado (punto 7.1).

## 10. Dudas pendientes
- Confirmar que UMDA_c es la variante que se espera como EDA básico en el estudio.
