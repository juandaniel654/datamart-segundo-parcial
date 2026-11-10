import sys
import csv
from decimal import Decimal

lector = csv.reader(sys.stdin)

for fila in lector:
    if not fila or fila[0] == "id_venta":
        continue

    fecha = fila[1]
    categoria = fila[2]
    cantidad = int(fila[4])
    precio = Decimal(fila[5])

    mes = fecha[:7]
    ingreso_centavos = int(precio * 100) * cantidad

    clave = f"{categoria}|{mes}"

    print(f"{clave}\t{ingreso_centavos}")
