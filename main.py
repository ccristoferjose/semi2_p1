import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from db_utils import insert_data

# --- Carga y limpieza del dataset nacional (df_guatemala_cleaned) ---

# URL pública del archivo
file_url = "https://mi-bucket-datos.s3.us-east-2.amazonaws.com/global_calificacion.csv"

# Cargar el archivo directamente en un DataFrame
try:
    print("Cargando el archivo global_calificacion.csv directamente desde el bucket...")
    df = pd.read_csv(file_url)
    print("Archivo cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el archivo en el DataFrame: {e}")
    exit(1)

# Filtrar los datos para Country = Guatemala
try:
    print("\nFiltrando datos para 'Country = Guatemala'...")
    if "Country" in df.columns:
        df_guatemala = df[df["Country"].str.strip().str.lower() == "guatemala"]
        print(f"Registros encontrados para Guatemala: {len(df_guatemala)}")
    else:
        print("Columna 'Country' no encontrada en los datos.")
        exit(1)
except Exception as e:
    print(f"Error al filtrar los datos: {e}")
    exit(1)

# Limpieza de los datos
try:
    # Eliminar columnas no necesarias
    df_guatemala_cleaned = df_guatemala.drop(columns=["Country_code", "Country", "WHO_region"])
    
    # Convertir columnas numéricas a formato adecuado
    df_guatemala_cleaned["New_cases"] = pd.to_numeric(df_guatemala_cleaned["New_cases"], errors="coerce").fillna(0).astype(int)
    df_guatemala_cleaned["New_deaths"] = pd.to_numeric(df_guatemala_cleaned["New_deaths"], errors="coerce").fillna(0).astype(int)
    df_guatemala_cleaned["Cumulative_cases"] = pd.to_numeric(df_guatemala_cleaned["Cumulative_cases"], errors="coerce").fillna(0).astype(int)
    df_guatemala_cleaned["Cumulative_deaths"] = pd.to_numeric(df_guatemala_cleaned["Cumulative_deaths"], errors="coerce").fillna(0).astype(int)
    
    # Convertir la columna de fechas a formato datetime
    df_guatemala_cleaned["Date_reported"] = pd.to_datetime(df_guatemala_cleaned["Date_reported"], errors="coerce")
    
    # Filtrar solo datos del año 2020
    df_guatemala_2020 = df_guatemala_cleaned[df_guatemala_cleaned["Date_reported"].dt.year == 2020]
    print(f"Registros filtrados para el año 2020: {len(df_guatemala_2020)}")
    
    # Eliminar filas donde todas las columnas de casos son 0
    df_guatemala_2020_nonzero = df_guatemala_2020[
        ~((df_guatemala_2020["New_cases"] == 0) &
          (df_guatemala_2020["Cumulative_cases"] == 0) &
          (df_guatemala_2020["New_deaths"] == 0) &
          (df_guatemala_2020["Cumulative_deaths"] == 0))
    ]
    print(f"Registros después de eliminar filas con valores 0: {len(df_guatemala_2020_nonzero)}")
    
except Exception as e:
    print(f"Error durante la limpieza de datos nacionales: {e}")
    exit(1)

# --- Carga y limpieza del dataset municipal ---
# Lista de departamentos válidos en Guatemala
departamentos_validos = [
    "GUATEMALA", "SACATEPEQUEZ", "CHIMALTENANGO", "ESCUINTLA", "SANTA ROSA", 
    "SOLOLA", "TOTONICAPAN", "QUETZALTENANGO", "SUCHITEPEQUEZ", "RETALHULEU",
    "SAN MARCOS", "HUEHUETENANGO", "QUICHE", "BAJA VERAPAZ", "ALTA VERAPAZ",
    "EL PROGRESO", "ZACAPA", "CHIQUIMULA", "JALAPA", "JUTIAPA", "PETEN",
    "IZABAL"
]

# --- Carga y limpieza del dataset municipal ---

# Ruta del archivo local municipio.csv
local_municipio_file = "municipio.csv"

# Verificar si el archivo existe localmente
if not os.path.exists(local_municipio_file):
    print(f"Archivo {local_municipio_file} no encontrado. Verifica la ruta.")
    exit(1)

# Cargar el archivo en un DataFrame
try:
    print("\nCargando el archivo municipio.csv desde la ubicación local...")
    df_municipio = pd.read_csv(local_municipio_file)
except Exception as e:
    print(f"Error inesperado al cargar el archivo municipio.csv: {e}")
    exit(1)

# Limpieza y transformación de datos
try:
    print("\nRealizando limpieza, transformación y corrección de datos...")

    # 1. Eliminar registros con departamentos no válidos
    df_municipio = df_municipio[df_municipio["departamento"].str.upper().isin(departamentos_validos)]

    # 2. Eliminar registros con códigos inválidos
    df_municipio = df_municipio[
        (df_municipio["codigo_departamento"] > 0) &
        (df_municipio["codigo_departamento"] != 9999) &
        (df_municipio["codigo_municipio"] > 0)
    ]

    # 3. Eliminar registros con población <= 0
    df_municipio = df_municipio[df_municipio["poblacion"] > 0]

    # 4. Eliminar columnas que no sean del año 2020
    columnas_a_conservar = ["departamento", "codigo_departamento", "municipio", "codigo_municipio", "poblacion"]
    columnas_2020 = [col for col in df_municipio.columns if "2020" in col]
    columnas_finales = columnas_a_conservar + columnas_2020
    df_municipio = df_municipio[columnas_finales]

    # 5. Convertir las fechas (columnas) a filas usando melt
    print("\nTransformando fechas a filas y eliminando días sin eventos...")
    df_municipio_melted = pd.melt(
        df_municipio,
        id_vars=columnas_a_conservar,
        var_name="fecha",
        value_name="eventos"
    )

    # 6. Eliminar filas donde "eventos" es 0
    df_municipio_final = df_municipio_melted[df_municipio_melted["eventos"] != 0]

    # Mostrar las primeras filas del DataFrame final
    # print("\nDatos finales después de transformación y limpieza:")
    # print(df_municipio_final.head())

except Exception as e:
    print(f"Error inesperado durante la limpieza y transformación de datos: {e}")
    exit(1)


df_guatemala_2020_nonzero["Date_reported"] = pd.to_datetime(df_guatemala_2020_nonzero["Date_reported"], errors="coerce")
df_municipio_final["fecha"] = pd.to_datetime(df_municipio_final["fecha"], errors="coerce")


# Realizar la unión
print("\nUniendo datasets por fecha...")
df_combinado = pd.merge(
    df_municipio_final,
    df_guatemala_2020_nonzero,
    left_on="fecha",
    right_on="Date_reported",
    how="inner"
)


# Departamentos únicos
departamentos = df_combinado[["codigo_departamento", "departamento"]].drop_duplicates()

# Municipios únicos
municipios = df_combinado[["codigo_municipio", "municipio", "codigo_departamento", "poblacion"]].drop_duplicates()

# Convertir Date_reported al tipo datetime y luego a date
df_combinado["Date_reported"] = pd.to_datetime(df_combinado["Date_reported"], errors="coerce").dt.date

# Extraer reportes nacionales únicos con Date_reported en formato correcto
reporte_nacional = df_combinado[[
    "Date_reported", "New_cases", "Cumulative_cases", "New_deaths", "Cumulative_deaths"
]].drop_duplicates()

# Validar que los datos sean correctos antes de la inserción
# print(reporte_nacional.head())

# Convertir las columnas de fecha al formato datetime.date
df_combinado["fecha"] = pd.to_datetime(df_combinado["fecha"], errors="coerce").dt.date

df_combinado["Date_reported"] = pd.to_datetime(df_combinado["Date_reported"], errors="coerce").dt.date

# Extraer eventos municipales únicos
evento_municipal = df_combinado[["codigo_municipio", "fecha", "eventos"]].drop_duplicates()

# Extraer eventos combinados únicos
evento = df_combinado[["codigo_municipio", "fecha", "Date_reported"]].drop_duplicates()


# Convertir DataFrame a listas de tuplas para cada tabla
departamentos_data = departamentos.to_records(index=False).tolist()
municipios_data = municipios.to_records(index=False).tolist()
reporte_nacional_data = reporte_nacional.to_records(index=False).tolist()
evento_municipal_data = evento_municipal.to_records(index=False).tolist()
evento_data = evento.to_records(index=False).tolist()



# Consultas de inserción
query_departamentos = "INSERT INTO departamento (codigo_departamento, departamento) VALUES (%s, %s)"
query_municipios = """INSERT INTO municipio (codigo_municipio, municipio, codigo_departamento, poblacion)
                      VALUES (%s, %s, %s, %s)"""
query_reporte_nacional = """INSERT INTO reporte_nacional (Date_reported, New_cases, Cumulative_cases, New_deaths, Cumulative_deaths)
                            VALUES (%s, %s, %s, %s, %s)"""
query_evento_municipal = """INSERT INTO evento_municipal (codigo_municipio, fecha, eventos)
                            VALUES (%s, %s, %s)"""
query_evento = """INSERT INTO evento (codigo_municipio, fecha, Date_reported)
                  VALUES (%s, %s, %s)"""


# Insertar datos
insert_data("departamento", departamentos_data, query_departamentos)
insert_data("municipio", municipios_data, query_municipios)
insert_data("reporte_nacional", reporte_nacional_data, query_reporte_nacional)

# Insertar datos de `evento_municipal` en lotes de 50 registros
insert_data("evento_municipal", evento_municipal_data, query_evento_municipal, batch_size=50)

# Insertar datos de `evento` en lotes de 50 registros
insert_data("evento", evento_data, query_evento, batch_size=50)

