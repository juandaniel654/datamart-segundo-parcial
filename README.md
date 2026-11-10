# Examen Segundo Parcial
## Pipeline de datos contenerizado

### Objetivo
Crear un pipeline de datos utilizando Docker, Hadoop MapReduce,
Python, MySQL y Flask.

### Pregunta de negocio
¿Cuál es el ingreso total por categoría y mes?

### Herramientas utilizadas
- Ubuntu Linux
- Docker y Docker Compose
- Hadoop 3.5.0
- Python 3
- MySQL 8.0
- Flask
- SSH

### Generación de datos
Se generaron 5,000,000 de registros de ventas utilizando Python.

Semilla: 125055088

Archivo: data/ventas.csv

Tamaño generado: 323 MiB aproximadamente.

### Procesamiento
Se utilizaron dos programas:

- mapper.py: obtiene la categoría, el mes y calcula el ingreso.
- reducer.py: suma los ingresos por categoría y mes.

Se obtuvieron 60 resultados.

### Comparación de tiempos
Python: 17.993 segundos.
Hadoop: 24.104 segundos.

Los resultados fueron idénticos.

Hadoop se ejecutó en modo local. Los tiempos corresponden a
ventanas de medición diferentes, por lo que son orientativos.

### Base de datos
MySQL almacena los resultados en la tabla resumen_ingresos.

El script cargar_resultados.py lee la salida de Hadoop
y la inserta en MySQL.

### API Flask
Puerto local: 8082

Endpoints:
- GET /resultados
- GET /resultados/<clave>
- POST /resultados

Se comprobó la consulta, el filtrado y la inserción
de registros mediante la API.

### Persistencia
Se ejecutaron docker compose down y docker compose up.

Los 61 registros existentes permanecieron almacenados,
incluido el registro creado mediante POST.

### Docker Compose
El proyecto utiliza tres servicios:
- hadoop
- db
- api

Comando de inicio:

docker compose up -d --build

Comando para comprobar los servicios:

docker compose ps

### SSH
Se configuró una conexión SSH mediante claves
entre Ubuntu y el contenedor Hadoop.

Puerto local: 2223.

### Evidencias
Los resultados de ejecución y las comprobaciones
se guardaron en la carpeta evidencias/.

### Nota
El archivo CSV se puede regenerar utilizando
scripts/generar_datos.py y la misma semilla.
Las contraseñas y las claves privadas no se publican.

### Preparar el proyecto en otra computadora

1. Tener Docker, Docker Compose, Python 3 y SSH instalados.

2. Preparar las credenciales y claves SSH:

   bash scripts/preparar_entorno.sh

3. Generar los datos originales:

   python3 scripts/generar_datos.py --filas 5000000 --semilla 125055088 --salida data/ventas.csv

4. Construir e iniciar los contenedores:

   docker compose up -d --build

El procesamiento de Hadoop y la carga en MySQL se
realizan mediante los scripts del proyecto.

No se incluyen contraseñas, claves privadas ni el
CSV original en GitHub.
