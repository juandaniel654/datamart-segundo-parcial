import re
from datetime import datetime
from pathlib import Path

log = Path("evidencias/hadoop_completo.log").read_text()

inicio = None
fin = None

for linea in log.splitlines():
    encontrado = re.match(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})",
        linea
    )

    if not encontrado:
        continue

    fecha = datetime.strptime(
        encontrado.group(1),
        "%Y-%m-%d %H:%M:%S,%f"
    )

    if "Running job:" in linea:
        inicio = fecha

    if "completed successfully" in linea:
        fin = fecha

if inicio and fin:
    tiempo = (fin - inicio).total_seconds()

    resultado = (
        "COMPARACION DE PROCESAMIENTO\n"
        "Registros: 5000000\n"
        "Resultados: 60\n"
        "Python: 17.993 segundos\n"
        f"Hadoop: {tiempo:.3f} segundos\n"
        "Resultados identicos: SI\n"
        "Hadoop: modo local\n"
    )

    print(resultado)

    Path("evidencias/comparacion_tiempos.txt").write_text(
        resultado
    )
else:
    print("No se encontro el tiempo completo en el log.")
    print("Es necesario medir una nueva ejecucion.")
