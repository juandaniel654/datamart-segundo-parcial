import csv
import os
import sys
from decimal import Decimal
import pymysql

archivo = sys.argv[1]
registros = []

with open(archivo, encoding="utf-8") as f:
    lector = csv.reader(f, delimiter="\t")

    for fila in lector:
        if len(fila) != 3:
            raise ValueError(f"Fila incorrecta: {fila}")

        categoria, mes, ingreso = fila

        registros.append((
            categoria,
            mes,
            Decimal(ingreso)
        ))

conexion = pymysql.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    database=os.environ["DB_NAME"]
)

try:
    with conexion.cursor() as cursor:
        for categoria, mes, ingreso in registros:
            cursor.execute("""
                INSERT INTO resumen_ingresos
                (categoria, mes, ingreso_total)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                ingreso_total = %s
            """, (categoria, mes, ingreso, ingreso))

    conexion.commit()

    print("Carga realizada correctamente")
    print("Registros procesados:", len(registros))

finally:
    conexion.close()
