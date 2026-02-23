USE master
GO

CREATE DATABASE LitioDB
GO

USE LitioDB

GO

CREATE TABLE dim_metodo_extraccion (
    metodo_id INT IDENTITY (1,1),
    nombre_metodo VARCHAR (100) NOT NULL,
    litros_agua_ton INT,
    CONSTRAINT PK_dim_metodo_extraccion PRIMARY KEY (metodo_id)
)

GO

CREATE TABLE dim_precios (
    anio INT,
    precio_usd_ton DECIMAL (10,2),
    CONSTRAINT PK_dim_precios PRIMARY KEY (anio)
)
GO

CREATE TABLE dim_pais_detalles (
    nombre_pais VARCHAR (100) NOT NULL, -- LO MEJOR ES USAR EL NOMBRE DE PAIS (Entity) como ID para que reconozca el csv
    metodo_id INT,
    reservas_ton BIGINT,
	recursos_ton BIGINT,
    CONSTRAINT PK_dim_pais_detalles PRIMARY KEY (nombre_pais),
    CONSTRAINT FK_dim_pais_detalles_dim_metodo_extraccion FOREIGN KEY (metodo_id) REFERENCES dim_metodo_extraccion (metodo_id)
)

GO

CREATE TABLE fact_produccion (
    prod_id INT IDENTITY(1,1),
    nombre_pais VARCHAR (100) NOT NULL,
    anio INT,
    toneladas_producidas DECIMAL(12,2),
    CONSTRAINT PK_fact_produccion PRIMARY KEY (prod_id),
    CONSTRAINT FK_fact_produccion_dim_pais_detalles FOREIGN KEY (nombre_pais) REFERENCES dim_pais_detalles(nombre_pais),
    CONSTRAINT FK_fact_produccion_Anio FOREIGN KEY (anio) REFERENCES dim_precios(anio)
);
GO

INSERT INTO dim_metodo_extraccion (nombre_metodo, litros_agua_ton) 
VALUES ('Salmuera', 20000), ('Roca', 140000), ('Mixto China (70s/30r)', 104000);

GO