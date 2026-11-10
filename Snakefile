# Orquestación con Snakemake.
#   snakemake --cores 8 --config cfg=configs/e3_tres_algoritmos.yaml
#   snakemake -n --config cfg=...      # simulación: muestra qué falta por correr
#
# Unidad de trabajo = bloque (algoritmo × función × D) con sus 30 corridas: un job por
# bloque evita pagar 30 veces el arranque de Python + MEALPY. Snakemake reparte los
# bloques entre los núcleos disponibles. Si algo se interrumpe, al relanzar se repiten
# solo los bloques incompletos, y dentro de ellos solo las corridas sin JSON.
import sys
sys.path.insert(0, ".")
from bench import config as C

CFG_PATH = config.get("cfg", "configs/e3_tres_algoritmos.yaml")
CFG = C.cargar(CFG_PATH)
SAL = CFG["salida"]
BLOQUES = sorted({t.bloque for t in C.tareas(CFG)})

rule todo:
    input: f"{SAL}/analisis/resumen.md"

rule bloque:
    output: touch(f"{SAL}/bloques/{{bloque}}.ok")
    shell: f"python run_experiment.py {CFG_PATH} --bloque {{wildcards.bloque}}"

rule analisis:
    input: expand(f"{SAL}/bloques/{{bloque}}.ok", bloque=BLOQUES)
    output: f"{SAL}/analisis/resumen.md"
    shell: f"python analyze.py {SAL}"
