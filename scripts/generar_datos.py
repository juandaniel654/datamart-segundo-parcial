import csv
import random
import argparse
from datetime import date, timedelta
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--filas", type=int, default=1000)
parser.add_argument("--semilla", type=int, required=True)
parser.add_argument("--salida", default="data/ventas.csv")
args = parser.parse_args()

random.seed(args.semilla)

productos = {
    "Electronica": ["Laptop", "Monitor", "Teclado"],
    "Ropa": ["Camisa", "Pantalon", "Sudadera"],
    "Hogar": ["Mesa", "Lampara", "Silla"],
    "Deportes": ["Balon", "Raqueta", "Mochila"],
    "Alimentos": ["Arroz", "Leche", "Cafe"]
}

categorias = list(productos)
sucursales = ["Norte", "Sur", "Centro", "Este", "Oeste"]
metodos = ["Efectivo", "Tarjeta", "Transferencia"]

salida = Path(args.salida)
salida.parent.mkdir(parents=True, exist_ok=True)

inicio = date(2025, 1, 1)

with salida.open("w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow([
        "id_venta",
        "fecha",
        "categoria",
        "producto",
        "cantidad",
        "precio_unitario",
        "sucursal",
        "metodo_pago",
        "cliente_id"
    ])

    for i in range(1, args.filas + 1):
        categoria = random.choice(categorias)
        producto = random.choice(productos[categoria])
        fecha = inicio + timedelta(days=random.randrange(365))
        cantidad = random.randint(1, 10)
        precio = random.randint(1000, 200000) / 100

        escritor.writerow([
            i,
            fecha.isoformat(),
            categoria,
            producto,
            cantidad,
            f"{precio:.2f}",
            random.choice(sucursales),
            random.choice(metodos),
            random.randint(100000, 999999)
        ])

print(f"Archivo generado: {salida}")
print(f"Registros generados: {args.filas}")
