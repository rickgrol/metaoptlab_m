---
title: "Resumen de avance — MetaOptLab-M"
author: "Ricardo H Guerrero Lara"
date: "17 de noviembre de 2026"
---

# 1. Avance desde el resumen del 10 de noviembre

- **Módulo de algoritmos: los 15 métodos acordados están sumados, corridos y documentados**, más Random Search como baseline estocástico. Esta semana sumamos siete: ACO, CMA-ES, Tabu Search, ASO, GWO, ICA y SCA desde MEALPY, y EDA como implementación propia (variante UMDA_c), porque no existe en MEALPY. Cada método tiene su archivo de documentación con la variante usada, sus operadores, parámetros y diferencias con el original.
- **Principales hallazgos en las implementaciones de MEALPY:**
  - CMA-ES: defecto grave. Los pasos con los que se actualiza la media no son los que generaron a los mejores individuos, porque se vuelven a sortear antes de usarlos; la media se mueve al azar y la selección no influye en la búsqueda. Quedó empatado en el último lugar con Random Search. En una prueba de diagnóstico, corrigiendo solo ese punto, el error en la esfera desplazada pasa del orden de 10³ al orden de 10⁻¹⁴.
  - Tabu Search: la lista tabú compara soluciones exactas de números reales, por lo que en variables continuas prácticamente nunca descarta un vecino; además, el paso no se escala al dominio. En la práctica no tiene memoria efectiva.
  - ICA: al transferir colonias entre imperios, la colonia se duplica en lugar de moverse; la población crece en cada época y los imperios nunca desaparecen.
  - ASO: el centro de los mejores átomos se calcula como un escalar en lugar de un vector.
  - ACO: MEALPY implementa ACO_R (Socha y Dorigo, 2008), pero elige la solución guía por dimensión y no por hormiga, y sus parámetros por defecto difieren de los del artículo.
  - GWO y SCA: agregan selección voraz, que no está en los originales. GWO tiene un sesgo hacia el centro del espacio documentado en la literatura; por eso usamos solo funciones desplazadas.
- **Prueba reducida con los 16 métodos** (5 corridas, D = 10, 3 funciones): 240 corridas sin fallas. En el ranking de Friedman, los primeros lugares son TLBO, PSO, ACO_R y EDA, y los últimos, Tabu Search, CMA-ES y Random Search. Con 5 corridas y 3 funciones, la prueba sirve para verificar que los métodos corren, no para concluir.
- **Repositorio en GitHub actualizado** con los 15 métodos, y flujo completo verificado: editamos y documentamos en local, subimos a GitHub y ejecutamos desde Colab; los resultados se reproducen igual en máquinas distintas.

# 2. Trabajo de esta semana

- Contrastar la documentación de cada método con su paper original y completar las fichas.
- Preparar las correcciones o alternativas de las implementaciones con defectos, según lo que decidamos.

# 3. Decisiones por tomar

- Implementaciones de MEALPY con defectos que impiden que representen al método (CMA-ES, Tabu Search, ICA y ASO): corregirlas y documentar la corrección, sustituirlas por una implementación de referencia, o reportar los defectos a los autores de MEALPY.
- Implementaciones que se alejan del original sin ser defectos (ABC, SA, ACO_R): usarlas tal cual o sustituirlas por una implementación fiel.
- Parámetros por defecto de MEALPY o los de los papers originales (por ejemplo, F = 0.1 en DE, y los parámetros de ACO_R).
- Confirmar UMDA_c como variante básica de EDA.
