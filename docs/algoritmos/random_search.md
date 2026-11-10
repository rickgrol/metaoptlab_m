# Búsqueda Aleatoria (Random Search)

> **Implementación propia:** `bench/externos/random_search.py` · **Revisado:** 10 de noviembre de 2026

## 1. Identificación
- **Método:** búsqueda aleatoria pura.
- **Clase en MEALPY:** no existe en MEALPY 3.0.3.
- **Implementación:** propia, en `bench/externos/random_search.py`; se declara en el YAML como `externo:RandomSearch`.
- **Papel en el estudio:** referencia de exploración pura. No es una metaheurística; cualquier método debería superarla.

## 2. Idea del método
En cada evaluación genera un punto uniforme en todo el dominio y conserva el mejor encontrado. No usa información de evaluaciones anteriores.

## 4. Qué implementa
Repite hasta agotar el presupuesto: `x = uniforme(lb, ub)` en las D dimensiones; evaluar f(x). El contador de evaluaciones es el mismo que usan los algoritmos de MEALPY, de modo que el presupuesto es idéntico.

## 5. Parámetros
Ninguno.

## 6. Costo
Una evaluación por iteración; no tiene inicialización aparte.

## 9. Resultados de la prueba reducida
5 corridas, D = 10, 1 000·D evaluaciones. Mediana del error final.

| Esfera desplazada | cec2017:F1 | cec2017:F4 |
|:--|:--|:--|
| 6.081e+03 | 6.048e+09 | 8.049e+03 |

Quedó en el último lugar del ranking de Friedman entre los ocho métodos (rango promedio 8.0), como se espera de una referencia de azar.
