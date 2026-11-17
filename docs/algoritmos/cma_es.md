# Estrategia Evolutiva con Adaptación de la Matriz de Covarianza (CMA-ES)

> **Versión revisada:** MEALPY 3.0.3, clase `CMA_ES` · **Revisado:** 16 de noviembre de 2026 · **Estado:** revisado contra el código; implementación con defectos graves

## 1. Identificación
- **Método básico:** Covariance Matrix Adaptation Evolution Strategy (CMA-ES).
- **Clase usada en MEALPY:** `CMA_ES` (módulo `mealpy/evolutionary_based/ES.py`).
- **Referencia que cita el código de MEALPY:** Hansen, N. y Ostermeier, A. (2001). *Completely derandomized self-adaptation in evolution strategies.* Evolutionary Computation, 9(2), 159–195.
- **Referencia de la versión estándar:** Hansen, N. (2016). *The CMA Evolution Strategy: A Tutorial.* arXiv:1604.00772.

## 2. Idea del método
Muestrea cada generación de una gaussiana multivariada N(m, σ²C). Con los mejores individuos actualiza tres cosas: la media m (hacia donde están las buenas soluciones), el tamaño de paso σ (con una trayectoria acumulada) y la matriz de covarianza C (que aprende la forma y orientación del paisaje). Así se adapta a funciones rotadas y mal condicionadas, que es justo donde fallan los métodos que trabajan coordenada por coordenada.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `CMA_ES` | Versión completa (media, σ y C) | Sí |
| `Simple_CMA_ES` | Versión simplificada de los autores de MEALPY | No (solo se documenta) |
| `OriginalES`, `LevyES` | Estrategias evolutivas sin adaptación de covarianza | No (solo se documentan) |

## 4. Qué implementa (según el código)
En cada época:
1. Genera λ = `pop_size` hijos: `x_i = m + σ · paso_i`, con `paso_i ~ N(0, C)`; corrige los que salen de los límites.
2. Ordena los hijos por calidad (no hay elitismo: la población anterior se descarta).
3. Actualiza la media con la suma ponderada de los pasos de los μ = λ/2 mejores.
4. Actualiza σ con la trayectoria de evolución p_σ, y C con la trayectoria p_c (rango 1) y los pasos de los μ mejores (rango μ).

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Valor estándar (Hansen, 2016) |
|:--|:--|:--|
| `pop_size` (λ) | 100 | 4 + ⌊3 ln D⌋ (10 en D = 10) |
| σ₀ | 0.1·(ub − lb) | ≈ 0.3·(ub − lb) |
| μ | λ/2 | λ/2 |

Los demás coeficientes (c_σ, d_σ, c_c, c_1, c_μ) se calculan internamente con las fórmulas del tutorial, salvo las diferencias señaladas abajo.

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: `pop_size`.

## 7. Diferencias y observaciones del código
1. **Defecto grave: la media no se mueve hacia las buenas soluciones.** Hay dos errores que se combinan:
   - Al crear cada hijo, `generate_empty_agent` le asigna un **paso aleatorio nuevo**, distinto del que se usó para generarlo.
   - Antes de actualizar la media, `update_step__` **vuelve a sobrescribir** todos los pasos con muestras nuevas.

   Así, la "suma ponderada de los pasos de los mejores" es en realidad una suma de vectores aleatorios que no tienen relación con los hijos seleccionados. La media hace un paseo aleatorio y la selección no influye en la búsqueda. En una prueba de diagnóstico (esfera desplazada, D = 10, 10 000 evaluaciones, 3 semillas), la media terminó **más lejos** del óptimo que al inicio, y el error final fue del orden de 10³. Corrigiendo solo estos dos puntos (que cada hijo conserve su paso y remuestrear al final de la época), el mismo caso llega a errores del orden de 10⁻¹⁴.
2. **d_σ mal calculado.** El código usa `np.max(valor, 0)`, que en NumPy no es el máximo entre el valor y 0 sino el valor mismo (el 0 se interpreta como eje). Cuando el valor es negativo, d_σ queda menor que el estándar.
3. **Actualización de σ modificada:** se eleva el factor a la potencia 0.3, que no aparece en la formulación estándar.
4. **Pesos de recombinación sobre λ, no sobre μ.** Los pesos se calculan para los λ hijos y se normalizan sobre λ, pero solo se usan los μ primeros; por eso suman menos de 1, y μ_eff también se calcula sobre λ.
5. **Reparación de C incorrecta.** Cuando C pierde la definición positiva, el código hace `V * E / V` elemento a elemento, lo que produce valores NaN; la reparación correcta es `V · diag(E) · Vᵀ`.

## 8. Relación con otros métodos (operadores)
Es el representante de los métodos que **aprenden un modelo de distribución**: muestrea, selecciona y ajusta la distribución. Comparte esa lógica con ACO_R (mezcla de gaussianas sobre un archivo) y, en menor medida, con la búsqueda de un único punto de SA y HC, que usan una distribución fija. A diferencia de PSO, DE y GA, no combina soluciones de la población entre sí.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, implementación de MEALPY sin modificar. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 3.210e+03 | 8.432e+09 | 8.569e+03 |

Último lugar del ranking de Friedman entre los diez métodos (rango promedio 9.67), **por debajo de Random Search**, lo que es coherente con el defecto del punto 7.1.

## 10. Dudas pendientes
- `CMA_ES` de MEALPY no puede usarse tal cual en el estudio. Opciones: (a) corregirla y documentar la corrección; (b) sustituirla por una implementación de referencia (la biblioteca `cma` de Hansen) como algoritmo externo; (c) reportar el defecto a los autores de MEALPY.
