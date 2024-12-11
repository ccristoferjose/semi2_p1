import requests
import os
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Configuración de la base de datos
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "admin123",
    "database": "guatemala_casos"  # Cambia esto al nombre de tu base de datos
}

# URL pública del archivo
file_url = "https://mi-bucket-datos.s3.us-east-2.amazonaws.com/global_calificacion.csv"
local_file_name = "global_calificacion.csv"

# Verificar si el archivo ya existe localmente
if not os.path.exists(local_file_name):
    try:
        print("Descargando archivo global_calificacion.csv...")
        response = requests.get(file_url)
        response.raise_for_status()
        with open(local_file_name, 'wb') as file:
            file.write(response.content)
        print("Archivo descargado con éxito.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
        exit(1)
else:
    print("Archivo global_calificacion.csv ya existe localmente.")

# Cargar el archivo en un DataFrame de pandas
try:
    print("Cargando el archivo global_calificacion.csv en un DataFrame...")
    df = pd.read_csv(local_file_name)
    print("Archivo cargado con éxito.")
except Exception as e:
    print(f"Error al cargar el archivo en el DataFrame: {e}")
    exit(1)

# Filtrar los datos de Guatemala
try:
    print("Filtrando datos para Guatemala...")
    if "Country" in df.columns:
        df_guatemala = df[df["Country"].str.strip().str.lower() == "guatemala"]
        print(f"Datos de Guatemala filtrados: {len(df_guatemala)} registros.")
    else:
        print("Columna 'Country' no encontrada en los datos.")
        exit(1)
except Exception as e:
    print(f"Error al filtrar los datos: {e}")
    exit(1)

# Limpieza de datos sobre Guatemala
try:
    print("Realizando limpieza de datos...")
    df_guatemala = df_guatemala.drop_duplicates()
    df_guatemala.fillna({
        "New_cases": 0,
        "Cumulative_cases": 0,
        "New_deaths": 0,
        "Cumulative_deaths": 0
    }, inplace=True)
    for col in ["New_cases", "Cumulative_cases", "New_deaths", "Cumulative_deaths"]:
        df_guatemala[col] = pd.to_numeric(df_guatemala[col], errors="coerce").fillna(0).astype(int)
    df_guatemala.drop(columns=["Country_code", "Country"], inplace=True)
    print("Limpieza de datos completada.")
except Exception as e:
    print(f"Error durante la limpieza de datos: {e}")
    exit(1)

# Preparar los datos del archivo 'municipio.csv'
local_municipio_file = "municipio.csv"
try:
    if not os.path.exists(local_municipio_file):
        print("Archivo municipio.csv no encontrado.")
        exit(1)

    print("Cargando archivo municipio.csv...")
    df_municipio = pd.read_csv(local_municipio_file)
    columnas_fijas = ["departamento", "codigo_departamento", "municipio", "codigo_municipio", "poblacion"]
    columnas_fechas = [col for col in df_municipio.columns if col not in columnas_fijas]
    print("Reformateando datos del archivo municipio.csv...")
    df_municipio_largo = pd.melt(
        df_municipio,
        id_vars=columnas_fijas,
        value_vars=columnas_fechas,
        var_name="Fecha",
        value_name="Casos"
    )
    df_municipio_largo.rename(columns={
        "departamento": "Departamento",
        "codigo_departamento": "Codigo_departamento",
        "municipio": "Municipio",
        "codigo_municipio": "Codigo_municipio",
        "poblacion": "Poblacion"
    }, inplace=True)
    df_municipio_largo["Fecha"] = pd.to_datetime(df_municipio_largo["Fecha"], format="%m/%d/%Y", errors="coerce")
    for col in ["Codigo_departamento", "Codigo_municipio", "Poblacion", "Casos"]:
        df_municipio_largo[col] = pd.to_numeric(df_municipio_largo[col], errors="coerce").fillna(0).astype(int)
    print("Datos del archivo municipio.csv preparados.")
except Exception as e:
    print(f"Error al reformatear los datos del archivo 'municipio.csv': {e}")
    exit(1)

# Combinar los datos globales con los municipales
try:
    print("Combinando datos de global_calificacion.csv y municipio.csv...")
    df_guatemala["Fecha"] = pd.to_datetime(df_guatemala["Date_reported"], format="%m/%d/%Y", errors="coerce")
    df_combinado = pd.merge(
        df_guatemala,
        df_municipio_largo,
        on="Fecha",
        how="outer"
    )

    # Manejar valores nulos y eliminar registros con valores inválidos
    df_combinado = df_combinado.dropna(subset=["Codigo_departamento", "Codigo_municipio"])
    df_combinado = df_combinado[(df_combinado["Departamento"] != "No disponible") & (df_combinado["Municipio"] != "No disponible")]

    print("Datos combinados preparados y registros no válidos eliminados.")
except Exception as e:
    print(f"Error al combinar y manejar los datos: {e}")
    exit(1)

# Función para insertar datos en el esquema normalizado
def insertar_datos(df_combinado):
    try:
        # Conectar a la base de datos
        print("Conectando a la base de datos...")
        conexion = mysql.connector.connect(**db_config)
        if conexion.is_connected():
            cursor = conexion.cursor()

            # Desactivar verificación de claves foráneas
            print("Desactivando verificación de claves foráneas...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            # 1. Insertar regiones
            print("Insertando datos en la tabla regiones...")
            regiones = df_combinado["WHO_region"].unique()
            for region in regiones:
                query_region = "INSERT IGNORE INTO regiones (nombre) VALUES (%s)"
                cursor.execute(query_region, (region,))
            conexion.commit()

            # 2. Insertar departamentos
            print("Insertando datos en la tabla departamentos...")
            departamentos = df_combinado[["Departamento", "Codigo_departamento"]].drop_duplicates()
            for _, row in departamentos.iterrows():
                query_departamento = """
                INSERT IGNORE INTO departamentos (nombre, codigo)
                VALUES (%s, %s)
                """
                cursor.execute(query_departamento, (row["Departamento"], int(row["Codigo_departamento"])))
            conexion.commit()

            # 3. Insertar municipios
            print("Insertando datos en la tabla municipios...")
            municipios = df_combinado[["Municipio", "Codigo_municipio", "Codigo_departamento", "Poblacion"]].drop_duplicates()
            for _, row in municipios.iterrows():
                query_municipio = """
                INSERT IGNORE INTO municipios (nombre, codigo, departamento_id, poblacion)
                VALUES (%s, %s, 
                (SELECT id FROM departamentos WHERE codigo = %s LIMIT 1), %s)
                """
                cursor.execute(query_municipio, (
                    row["Municipio"], int(row["Codigo_municipio"]), int(row["Codigo_departamento"]), int(row["Poblacion"])
                ))
            conexion.commit()

            # 4. Insertar casos
            print("Insertando datos en la tabla casos...")
            casos = df_combinado[[
                "Date_reported", "WHO_region", "New_cases", "Cumulative_cases", 
                "New_deaths", "Cumulative_deaths", "Casos", "Codigo_municipio"
            ]]
            for _, row in casos.iterrows():
                region_id_query = "SELECT id FROM regiones WHERE nombre = %s LIMIT 1"
                cursor.execute(region_id_query, (row["WHO_region"],))
                region_id = cursor.fetchone()

                municipio_id_query = "SELECT id FROM municipios WHERE codigo = %s LIMIT 1"
                cursor.execute(municipio_id_query, (row["Codigo_municipio"],))
                municipio_id = cursor.fetchone()

                if not region_id:
                    print(f"Error: Región no encontrada para {row['WHO_region']}.")
                    continue

                municipio_id = municipio_id[0] if municipio_id else None

                query_caso = """
                INSERT INTO casos (
                    date_reported, region_id, municipio_id, new_cases, cumulative_cases, 
                    new_deaths, cumulative_deaths, casos_municipales
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query_caso, (
                    row["Date_reported"], region_id[0], municipio_id,
                    int(row["New_cases"]), int(row["Cumulative_cases"]),
                    int(row["New_deaths"]), int(row["Cumulative_deaths"]),
                    int(row["Casos"])
                ))
            conexion.commit()

            # Reactivar verificación de claves foráneas
            print("Reactivando verificación de claves foráneas...")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

            print("Datos insertados con éxito.")

    except Error as e:
        print(f"Error al insertar datos: {e}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada.")

# Llamada a la función insertar_datos
insertar_datos(df_combinado)
