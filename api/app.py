import os
import re
import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

def conectar():
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "db"),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=10
    )

@app.get("/")
def inicio():
    return jsonify({
        "proyecto": "Examen Segundo Parcial",
        "estado": "API funcionando",
        "rutas": ["/salud", "/ingresos"]
    })

@app.get("/salud")
def salud():
    try:
        with conectar() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT 1")
        return jsonify({"mysql": "conectado"})
    except pymysql.MySQLError:
        return jsonify({"mysql": "no disponible"}), 503

@app.get("/ingresos")
def ingresos():
    categoria = request.args.get("categoria")
    mes = request.args.get("mes")

    if mes and not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", mes):
        return jsonify({"error": "Mes invalido"}), 400

    if categoria and len(categoria) > 80:
        return jsonify({"error": "Categoria invalida"}), 400

    consulta = """
        SELECT categoria, mes, ingreso_total
        FROM resumen_ingresos
        WHERE 1=1
    """
    valores = []

    if categoria:
        consulta += " AND categoria = %s"
        valores.append(categoria)

    if mes:
        consulta += " AND mes = %s"
        valores.append(mes)

    consulta += " ORDER BY categoria, mes"

    try:
        with conectar() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(consulta, valores)
                filas = cursor.fetchall()
    except pymysql.MySQLError:
        return jsonify({"error": "Base de datos no disponible"}), 503

    for fila in filas:
        fila["ingreso_total"] = str(fila["ingreso_total"])

    return jsonify({
        "total": len(filas),
        "resultados": filas
    })


from decimal import Decimal, InvalidOperation

@app.get("/resultados")
def obtener_resultados():
    return ingresos()


@app.get("/resultados/<clave>")
def obtener_por_clave(clave):
    try:
        with conectar() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT categoria, mes, ingreso_total
                    FROM resumen_ingresos
                    WHERE categoria = %s
                    ORDER BY mes
                """, (clave,))
                filas = cursor.fetchall()

    except pymysql.MySQLError:
        return jsonify({"error": "Error de MySQL"}), 503

    for fila in filas:
        fila["ingreso_total"] = str(fila["ingreso_total"])

    return jsonify({
        "clave": clave,
        "total": len(filas),
        "resultados": filas
    })


@app.post("/resultados")
def crear_resultado():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "JSON invalido"}), 400

    categoria = datos.get("categoria")
    mes = datos.get("mes")

    if not isinstance(categoria, str):
        return jsonify({"error": "Categoria invalida"}), 400

    categoria = categoria.strip()

    if not categoria or len(categoria) > 80:
        return jsonify({"error": "Categoria invalida"}), 400

    if not isinstance(mes, str) or not re.fullmatch(
        r"\d{4}-(0[1-9]|1[0-2])", mes
    ):
        return jsonify({"error": "Mes invalido"}), 400

    try:
        monto = Decimal(str(datos.get("ingreso_total")))

        if (
            not monto.is_finite()
            or monto < 0
            or monto > Decimal("999999999999999999.99")
            or monto != monto.quantize(Decimal("0.01"))
        ):
            return jsonify({"error": "Ingreso invalido"}), 400

    except (InvalidOperation, TypeError, ValueError):
        return jsonify({"error": "Ingreso invalido"}), 400

    try:
        with conectar() as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO resumen_ingresos
                    (categoria, mes, ingreso_total)
                    VALUES (%s, %s, %s)
                """, (categoria, mes, monto))

            conexion.commit()

    except pymysql.err.IntegrityError:
        return jsonify({"error": "Registro duplicado"}), 409

    except pymysql.MySQLError:
        return jsonify({"error": "Error de MySQL"}), 503

    return jsonify({
        "mensaje": "Registro creado correctamente",
        "categoria": categoria,
        "mes": mes,
        "ingreso_total": str(monto)
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
