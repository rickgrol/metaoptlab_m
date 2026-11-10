# Colonia Artificial de Abejas (ABC)

> **Versión revisada:** MEALPY 3.0.3, clase `OriginalABC` · **Revisado:** 10 de noviembre de 2026 · **Estado:** revisado contra el código; pendiente contraste detallado con el paper original

## 1. Identificación
- **Método básico:** Artificial Bee Colony (ABC).
- **Clase usada en MEALPY:** `OriginalABC` (módulo `mealpy/swarm_based/ABC.py`).
- **Referencia que cita el código de MEALPY:** Basturk, B. y Karaboga, D. (2006). *An artificial bee colony (ABC) algorithm for numeric function optimization.* IEEE Swarm Intelligence Symposium.
- **Referencia original del método:** Karaboga, D. (2005). *An idea based on honey bee swarm for numerical optimization.* Reporte técnico TR06, Universidad de Erciyes; y Karaboga, D. y Basturk, B. (2007), Journal of Global Optimization, 39, 459–471.

## 2. Idea del método
Cada solución es una fuente de alimento. Las abejas empleadas exploran alrededor de su fuente; las observadoras eligen fuentes según su calidad y las explotan; las exploradoras abandonan las fuentes que no mejoran tras cierto número de intentos y buscan nuevas al azar.

## 3. Variantes en MEALPY y cuál se toma
| Clase | Qué es | ¿Se usa? |
|:--|:--|:--|
| `OriginalABC` | Única versión en MEALPY | Sí |

## 4. Qué implementa (según el código)
En cada época:
1. **Empleadas:** para cada fuente x_i, `v = x_i + φ·(x_i − x_k)`, con φ uniforme en [−1, 1] y k al azar; reemplazo voraz y conteo de intentos fallidos.
2. **Observadoras:** eligen fuentes por ruleta según su calidad y aplican la misma regla.
3. **Exploradoras:** toda fuente con `n_limits` intentos fallidos o más se reemplaza por una solución aleatoria.

## 5. Parámetros
| Parámetro | Valor por defecto en MEALPY | Valor en Karaboga y Basturk (2007) |
|:--|:--|:--|
| `n_limits` | 25 | límite = SN·D (fuentes × dimensiones) |
| `pop_size` | 100 | número de fuentes SN = mitad de la colonia |

## 6. Costo por época
- Evaluaciones en la inicialización: `pop_size`.
- Evaluaciones por época: 2·`pop_size` (empleadas y observadoras), más una por cada fuente abandonada.

## 7. Diferencias y observaciones del código
1. **Perturba todas las dimensiones.** En el ABC original, cada abeja modifica **una sola** dimensión elegida al azar; aquí φ es un vector y cambian todas. Es un operador mucho más exploratorio.
2. **Límite de abandono fijo (25)** en lugar de SN·D; con D = 10 y 50 fuentes, el original usaría 500.
3. **Varias exploradoras por ciclo.** En el original, a lo más una fuente se abandona por ciclo; aquí se abandonan todas las que superan el límite.

## 8. Relación con otros métodos (operadores)
La regla de movimiento usa la diferencia entre dos soluciones, como DE, pero sin cruce; la fase de exploradoras es un reinicio parcial, ausente en PSO y DE.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 4.393e−02 | 1.453e+07 | 5.893e+01 |

## 10. Dudas pendientes
- Las tres diferencias del punto 7 cambian el algoritmo de forma importante. ¿Usamos `OriginalABC` o una implementación fiel al original?
