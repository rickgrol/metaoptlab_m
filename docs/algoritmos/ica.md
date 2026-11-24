# Imperialist Competitive Algorithm (ICA)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalICA` · **Revisado:** 17 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Imperialist Competitive Algorithm (ICA), algoritmo competitivo imperialista.
- **Clase usada en MEALPY:** `OriginalICA` (módulo `mealpy/human_based/ICA.py`).
- **Referencia que cita el código de MEALPY:** Atashpaz-Gargari, E. y Lucas, C. (2007). *Imperialist competitive algorithm: an algorithm for optimization inspired by imperialistic competition.* IEEE Congress on Evolutionary Computation, 4661–4667.
- **Referencia original del método:** la misma.

## 2. Idea del método
Inspirado en el imperialismo. Las mejores soluciones son **imperialistas** y las demás se reparten entre ellos como **colonias**, en proporción al poder de cada imperio. Las colonias se mueven hacia su imperialista (asimilación), algunas cambian al azar (revolución) y, si una colonia supera a su imperialista, intercambian papeles. Los imperios compiten: el más débil pierde colonias frente a los demás y, al quedarse sin ellas, desaparece. Es el representante del paradigma social de la lista.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalICA` | Única versión en MEALPY | Sí |

## 4. Qué implementa (según el código)
En cada época:
1. **Asimilación:** `colonia = colonia + beta · U(0, 1) · (imperialista − colonia)`, con U por dimensión.
2. **Revolución:** el imperialista siempre, y cada colonia con probabilidad `revolution_prob`, reciben una perturbación gaussiana en una fracción `revolution_rate` de sus dimensiones.
3. **Competencia dentro del imperio:** si una colonia es mejor que su imperialista, intercambian lugar.
4. **Competencia entre imperios:** con el costo total de cada imperio (imperialista + `zeta` · media de colonias), se elige un imperio ganador y se le asigna la peor colonia del imperio más débil.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Comentario |
|:--|:--|:--|
| `empire_count` | 5 | Número de imperios |
| `assimilation_coeff` (β) | 1.5 | Coeficiente de asimilación |
| `revolution_prob` | 0.05 | Probabilidad de revolución de una colonia |
| `revolution_rate` | 0.1 | Fracción de dimensiones que cambian |
| `revolution_step_size` | 0.1 | Desviación del paso de revolución, en unidades absolutas |
| `zeta` (ξ) | 0.1 | Peso de las colonias en el costo total del imperio |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: número de colonias + número de imperialistas, **que crece con las épocas** (ver punto 7.1).

## 7. Diferencias y observaciones del código
1. **La población crece en cada época.** Al transferir la peor colonia del imperio más débil, el código la toma de una **copia ordenada** de la lista y la agrega al imperio ganador, pero nunca la elimina del imperio original. La colonia queda duplicada y la población aumenta en una por época. En una prueba de diagnóstico (población 50), las colonias pasaron de 45 a 145 en 100 épocas, y las evaluaciones por época de 53 a 153. Los imperios nunca desaparecen, de modo que la eliminación de imperios del método original no ocurre.
2. **La asimilación omite la desviación angular.** En el paper, la colonia avanza hacia el imperialista una distancia aleatoria y con una desviación de dirección θ; aquí se usa un factor uniforme por dimensión, sin θ.
3. **Normalización del poder diferente.** El código normaliza el costo restando (máximo + mínimo); verificar contra la normalización del paper.
4. **Paso de revolución sin escalar al dominio** (0.1 absoluto), como en SA y Tabu Search.
5. **Población reportada desactualizada.** Al final de la época, la población que MEALPY usa para su historial se arma con la lista de colonias inicial, no con las colonias actuales de los imperios.

## 8. Relación con otros métodos (operadores)
La asimilación es una atracción hacia un líder, como en PSO o GWO, pero cada colonia sigue a su propio imperialista y no al mejor global, lo que mantiene varias subpoblaciones. La revolución hace el papel de la mutación del GA.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones, parámetros por defecto. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 2.131e+00 | 1.925e+06 | 1.883e+02 |

Lugar 9 de 16 en el ranking de Friedman (rango promedio 7.7).

## 10. Dudas pendientes
- Con la población creciendo y sin eliminación de imperios (punto 7.1), `OriginalICA` no reproduce el método original. ¿Se corrige o se sustituye?
