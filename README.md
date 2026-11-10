# MetaOptLab-M · v0.1

Capa experimental sobre **MEALPY 3.0.3** (algoritmos) y **opfunu 1.0.1** (funciones CEC), para el proyecto doctoral RHGL (paper 1: caracterización masiva de metaheurísticas).

**Qué aporta cada pieza:**
- **MEALPY** aporta las metaheurísticas.
- **Este paquete** aporta lo que MEALPY no tiene: diseño experimental declarativo, presupuesto exacto por evaluaciones, un registro por corrida con reanudación, orquestación y análisis estadístico.

## Estructura

```
configs/            experimentos en YAML (qué correr)
bench/
  functions.py      catálogo de funciones (propias + opfunu)
  tracker.py        contador externo de evaluaciones; corta en max_fe exacto
  config.py         YAML → tareas (algoritmo, función, D, corrida)
  runner.py         ejecuta una tarea → un JSON (escritura atómica, reanudable)
  analysis/         aggregate · stats · plots  (solo lee JSON)
bench/externos/     algoritmos que no existen en MEALPY (por ejemplo, Random Search)
docs/algoritmos/    un archivo .md por método: qué implementa MEALPY, variantes, diferencias
docs/avances/       resúmenes de avance
docs/plan_de_trabajo.md   plan por fases y seguimiento de los métodos
run_experiment.py   módulo de ejecución (no interactivo)
analyze.py          módulo de análisis (no ejecuta algoritmos)
Snakefile           orquestación: un job por bloque algoritmo × función × D
```

## Uso

```bash
pip install -r requirements.txt
pip install --no-deps mealpy==3.0.3   # ver nota en requirements.txt

# 1. Verificar que todo funciona (~1–2 min)
python run_experiment.py configs/prueba_rapida.yaml
python analyze.py resultados/prueba_rapida

# 2. Experimentos E1–E3, secuencial
python run_experiment.py configs/e1_sa_esfera.yaml
python analyze.py resultados/e1_sa_esfera

# 3. Lo mismo con Snakemake, usando 8 núcleos
snakemake --cores 8 --config cfg=configs/e3_tres_algoritmos.yaml

# Versión reducida de cualquier experimento, para probar
python run_experiment.py configs/e3_tres_algoritmos.yaml --corridas 5 --dimensiones 10 --fe_por_dim 2000 --salida resultados/prueba_e3
```

**Salida de `analyze.py`** (en `resultados/<exp>/analisis/`):
- `corridas.csv` (una fila por corrida);
- `descriptiva.csv`: mejor, peor, mediana, media, desviación, tasa de éxito y tiempo;
- `checkpoints.csv`: error mediano al 1, 10, 50 y 100 % del presupuesto;
- comparaciones por problema (Mann-Whitney con Holm, ganadas/empatadas/perdidas), Wilcoxon con Holm y Friedman con Iman-Davenport y diferencia crítica de Nemenyi;
- figuras a 300 dpi: convergencia con mediana e IQR contra evaluaciones, boxplots y diagrama de diferencia crítica;
- `resumen.md`.

## Decisiones de diseño

- **Presupuesto exacto.** El tracker lanza `PresupuestoAgotado` en la evaluación `max_fe = fe_por_dim · D`. Así el presupuesto no depende de cuántas evaluaciones hace cada algoritmo por época. Además, evita el `Termination(max_fe)` de MEALPY, que solo revisa al final de cada época y recorre el historial completo en cada una, lo que vuelve muy lentos los algoritmos con muchas épocas.
- **Épocas calibradas.** Antes de cada corrida se mide cuántas evaluaciones hace el algoritmo al inicializar y por época, y se fija el número de épocas que cabe en el presupuesto. Muchos algoritmos ajustan sus parámetros con `época / total_de_épocas` (por ejemplo, el tamaño de paso de HC); si el total no corresponde al presupuesto real, ese programa interno se distorsiona.
- **Error.** Se reporta como f(x) − f\*, con registro en las fracciones del protocolo CEC2017 (0.01, 0.02, 0.03, 0.05, 0.1 … 1.0).
- **Semillas.** Se usa `semilla_base + corrida`: igual para todos los algoritmos en una corrida (números aleatorios comunes) y distinta entre corridas, para tener varianza real. Si una combinación sale con varianza cero, `analyze.py` lo marca.
- **Modo `single` y paralelismo.** Cada corrida usa el modo `single` de MEALPY. El paralelismo va entre corridas, a cargo de Snakemake. El propio paper de MEALPY (Tabla 15) muestra que el modo `process` es unas 120 veces más lento con funciones baratas.
- **Controles de calidad automáticos:** varianza cero, error negativo (óptimo declarado incorrecto), evaluaciones fuera de límites o no finitas, y subconsumo del presupuesto.

## Problemas encontrados al construir esta versión

1. **opfunu recorre la numeración de CEC2017.** Omite la F2 oficial, de modo que opfunu Fk corresponde a la oficial F(k+1) para k ≥ 2. Por ejemplo, `cec2017:F4` es la Rastrigin (F5 oficial).
2. **opfunu `cec2017:F9` (Schwefel) no es válida.** Con muestreo aleatorio se obtienen valores por debajo de `f_global` (−215 frente a 900), así que su `f_global` no es el mínimo real.
3. **La magnitud del error de `cec2017:F4` sugiere una implementación distinta a la oficial.** Antes de la Ronda 1 hay que validar cada función de opfunu contra el código oficial de CEC.
4. **`OriginalSA` de MEALPY tiene problemas serios:**
   - es de solución única, con una evaluación por época, y su validador limita `epoch` ≤ 100 000, lo que impide el presupuesto CEC en D ≥ 20 (aquí se resuelve fijando `epoch` después de construir el modelo);
   - el tamaño de paso es fijo (0.1) y no se escala al dominio;
   - el enfriamiento es T₀/época, sin calibración;
   - puede evaluar fuera de límites;
   - cada corrida en D = 30 tarda unos 3 minutos.
   
   Por estos problemas, se justifica considerar una implementación externa de SA.
5. **`OriginalDE` usa F = `wf` = 0.1 por defecto**, muy por debajo de los valores clásicos (0.5–0.9), y `OriginalPSO` usa inercia fija w = 0.4. Los parámetros por defecto deben reportarse o fijarse explícitamente en `parametros:`.
