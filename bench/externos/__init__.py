"""Algoritmos externos: métodos que no existen en MEALPY.

Se declaran en el YAML con el prefijo "externo:", por ejemplo "externo:RandomSearch".
Cada clase recibe la función objetivo ya envuelta por el Tracker, de modo que corre
con el mismo contador de evaluaciones y el mismo presupuesto que los de MEALPY.
"""
from .random_search import RandomSearch

EXTERNOS = {"RandomSearch": RandomSearch}
