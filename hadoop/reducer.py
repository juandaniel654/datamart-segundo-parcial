import sys

clave_actual = None
total = 0

def mostrar_resultado(clave, centavos):
    categoria, mes = clave.split("|", 1)
    ingreso = f"{centavos // 100}.{centavos % 100:02d}"
    print(f"{categoria}\t{mes}\t{ingreso}")

for linea in sys.stdin:
    clave, valor = linea.strip().split("\t", 1)
    ingreso = int(valor)

    if clave_actual == clave:
        total += ingreso
    else:
        if clave_actual is not None:
            mostrar_resultado(clave_actual, total)

        clave_actual = clave
        total = ingreso

if clave_actual is not None:
    mostrar_resultado(clave_actual, total)
