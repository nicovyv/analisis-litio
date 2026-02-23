import pandas as pd
from sqlalchemy import create_engine
import urllib

SERVER_NAME = 'DESKTOP-SHHQA4R\\SQLEXPRESS'
DATABASE_NAME = 'LitioDB'

params = urllib.parse.quote_plus(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};'
    f'Trusted_Connection=yes;TrustServerCertificate=yes;'
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
print("Iniciando proceso de carga...")


print("Preparando tabla de precios...")
df_precios = pd.DataFrame({
    'anio': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'precio_usd_ton': [6000, 9000, 12000, 14000, 10000, 10100, 14200, 71100, 41300, 14000]
}) 

print("Preparando tabla países")
df_paises = pd.DataFrame({
    'nombre_pais': ['Argentina', 'Chile', 'Bolivia', 'Australia', 'China', 'United States', 'Brazil', 'Canada', 'Zimbabwe', 'Portugal'],
    'metodo_id':   [1,           1,       1,         2,           3,       1,               2,        2,        2,          2],
    'reservas_ton': [4000000,     9300000, 0,         7000000,     3000000, 1800000,         390000,   1200000,  480000,     60000],
    'recursos_ton': [23000000,   11000000, 23000000,  8900000,     6800000, 19000000,        1300000,  5700000,  860000,     270000]
})

print("Leyendo CSV producción")
df_prod = pd.read_csv(r'C:\Users\Usuario\Documents\Proyecto_Litio\data\raw\lithium-production.csv')

lista_paises_validos = df_paises['nombre_pais'].tolist()
df_prod = df_prod[df_prod['Entity'].isin(lista_paises_validos)].copy()

df_prod = df_prod[['Entity', 'Year', 'Lithium production - kt']]
df_prod.columns = ['nombre_pais', 'anio', 'toneladas_producidas']

df_prod = df_prod[df_prod['anio'].between(2015,2025)]

try:
    print("Insertando en SQL Server...")

    df_precios.to_sql('dim_precios', con=engine, if_exists='append', index=False)
    print("Precios cargados.")

    df_paises.to_sql('dim_pais_detalles', con=engine, if_exists='append', index=False)
    print("Países cargados.")
    
    df_prod.to_sql('fact_produccion', con=engine, if_exists='append', index=False)
    print("Producción cargada.")

    print('\n Proceso terminado. Base de datos cargada')

except Exception as e:
    print(f'\n ocurrió un error: {e}')