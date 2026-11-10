#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "===== EXAMEN SEGUNDO PARCIAL ====="

echo "1. CONTENEDORES"
docker compose ps

echo "2. ARCHIVO CSV"
test -f data/ventas.csv
LINEAS=$(wc -l < data/ventas.csv)
echo "Lineas: $LINEAS"
test "$LINEAS" -eq 5000001
du -h data/ventas.csv

echo "3. HADOOP MAPREDUCE"
test -f resultados/hadoop_completo/_SUCCESS
TOTAL=$(wc -l < resultados/hadoop_completo/part-00000)
echo "Resultados: $TOTAL"
test "$TOTAL" -eq 60

echo "4. MYSQL"
DB_TOTAL=$(docker compose exec -T db sh -c \
'MYSQL_PWD="$MYSQL_PASSWORD" mysql -h 127.0.0.1 \
-u "$MYSQL_USER" "$MYSQL_DATABASE" \
-N -B -e "SELECT COUNT(*) FROM resumen_ingresos;"')

echo "Registros MySQL: $DB_TOTAL"
test "$DB_TOTAL" -eq 60

echo "5. API FLASK"
curl -fsS http://127.0.0.1:8082/salud

echo
echo "6. CONSULTA DE INGRESOS"
curl -fsS \
'http://127.0.0.1:8082/ingresos?categoria=Alimentos&mes=2025-01' \
| python3 -c '
import json
import sys

datos = json.load(sys.stdin)

assert datos["total"] == 1
assert datos["resultados"][0]["ingreso_total"] == "469172005.54"

print("Consulta correcta")
'

echo "===== VERIFICACIONES COMPLETADAS ====="
