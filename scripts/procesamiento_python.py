import csv
import time
from collections import defaultdict
from pathlib import Path

inicio = time.perf_counter()
totales = defaultdict(int)
registros = 0

with open("data/ventas.csv", encoding="utf-8", newline="") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        categoria = fila["categoria"]
        mes = fila["fecha"][:7]
        cantidad = int(fila["cantidad"])

        entero, decimal = fila["precio_unitario"].split(".")
        precio_centavos = int(entero) * 100 + int(decimal)

        totales[(categoria, mes)] += cantidad * precio_centavos
        registros += 1

salida = Path("resultados/python_completo.tsv")

with salida.open("w", encoding="utf-8") as archivo:
    for (categoria, mes), centavos in sorted(totales.items()):
        ingreso = f"{centavos // 100}.{centavos % 100:02d}"
        archivo.write(f"{categoria}\t{mes}\t{ingreso}\n")

duracion = time.perf_counter() - inicio

print("Registros procesados:", registros)
print("Resultados generados:", len(totales))
print(f"Tiempo Python: {duracion:.3f} segundos")
print("Archivo:", salida)
