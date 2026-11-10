CREATE DATABASE IF NOT EXISTS datamart;

USE datamart;

CREATE TABLE IF NOT EXISTS resumen_ingresos (
    categoria VARCHAR(80) NOT NULL,
    mes CHAR(7) NOT NULL,
    ingreso_total DECIMAL(20,2) NOT NULL,
    PRIMARY KEY (categoria, mes)
);
