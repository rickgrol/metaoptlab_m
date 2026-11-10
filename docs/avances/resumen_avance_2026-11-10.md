---
title: "Resumen de avance — MetaOptLab-M"
author: "Ricardo H Guerrero Lara"
date: "10 de noviembre de 2026"
---

# Resumen de avance — MetaOptLab-M

**Ricardo H Guerrero Lara** · 10 de noviembre de 2026

## 1. Avance desde la sesión del 20 de octubre
- **Revisión de MEALPY.** Confirmamos en el código fuente (versión 3.0.3) y en el artículo de sus autores (*Journal of Systems Architecture*, 2023) que la biblioteca no incluye pruebas estadísticas; el artículo reporta solo media y desviación estándar.
- **Prueba de funcionamiento del catálogo completo de MEALPY.** De 234 optimizadores, 215 corren sin problemas y 19 quedan documentados con su motivo de exclusión: 8 no se pueden crear con sus parámetros por defecto, 7 evalúan puntos fuera de los límites, 2 no evolucionan (`OriginalGA` y `DS_GWO`), 1 excede el presupuesto de evaluaciones y 1 no es reproducible con semilla fija.
- **Flujo de experimentación sobre MEALPY (MetaOptLab-M).** Configuración por archivo, ejecución no interactiva, un resultado por corrida con reanudación, presupuesto exacto por evaluaciones y número de épocas calibrado al presupuesto. La ejecución y el análisis están separados, y admite algoritmos externos que no existen en MEALPY con el mismo control de presupuesto. Corre en Colab, y verificamos que los resultados se reproducen igual en máquinas distintas.
- **Hallazgos en opfunu.** La numeración de CEC2017 está recorrida respecto a la oficial (su F5 no es Rastrigin) y su F9 da valores por debajo de su óptimo declarado. Antes del experimento masivo hay que validar las funciones contra el código oficial de CEC.
- **Módulo de algoritmos: 8 métodos sumados, corridos y documentados** (un archivo por método con variante usada, operadores, parámetros y diferencias con el original): Random Search (implementación propia, como referencia), Hill Climbing, SA, TLBO, PSO, DE, GA y ABC. Principales diferencias encontradas en MEALPY:
  - Hill Climbing: la reducción exponencial del paso es propia de MEALPY, y la perturbación falla en dominios no centrados en cero.
  - SA: paso fijo de 0.1 sin escalar al dominio y temperatura inicial sin calibrar.
  - PSO: la partícula solo se mueve si mejora, y el peso de inercia es fijo (0.4).
  - DE: F = 0.1 por defecto, la estrategia por defecto está mal etiquetada y el cruce no garantiza la componente del mutante.
  - ABC: perturba todas las dimensiones, mientras que el original modifica solo una.
  - GA: `OriginalGA` no funciona porque no implementa el método de evolución (corre sin error, pero la población nunca cambia); se usa `BaseGA`, con codificación real.
  - En la prueba reducida, Random Search quedó en el último lugar del ranking de Friedman, como se espera de la referencia de azar.
- **Repositorio en GitHub** con el código, las configuraciones, la documentación de cada método y el plan de trabajo, compartido con usted.

## 2. Trabajo de esta semana
- Sumar y documentar ACO y CMA-ES, para avanzar en completar los 15 métodos.
- Contrastar la documentación de cada método con su paper original.
- Completar el repositorio en GitHub hasta donde vamos.

## 3. Decisiones por tomar
- Referencia original de Hill Climbing a utilizar, La referencia que cita MEALPY de Mitchell, Holland y Forrest (1993) describen un HC sobre cadenas binarias, no la versión continua que implementa `OriginalHC`. Podemos citar a Talbi (2009) y Brownlee (2012).
- Decidir si utilizamos los parámetros por defecto de MEALPY o utilizamos los de los papers originales para las metaheurísticas que apliqu. En DE, por ejemplo, MEALPY utiliza F = 0.1 frente a F = 0.5.
- Implementaciones de MEALPY que se alejan del original (ABC, SA): usarlas tal cual o sustituirlas por una implementación fiel.
