from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db import db_config

# String de conexión para SQLAlchemy
string_connection = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# Creación del motor SQL
engine = create_engine(string_connection)

# Query para obtener datos necesarios
query = """
SELECT 
    municipio.poblacion, 
    reporte_nacional.New_deaths AS nuevas_muertes, 
    reporte_nacional.Cumulative_deaths AS muertes_acumuladas
FROM municipio
LEFT JOIN evento ON municipio.codigo_municipio = evento.codigo_municipio
LEFT JOIN reporte_nacional ON evento.Date_reported = reporte_nacional.Date_reported;
"""

# Cargar los datos en un DataFrame
data = pd.read_sql(query, engine)

# Eliminar filas con valores nulos
data = data.dropna()

# Estadísticos descriptivos
descriptive_stats = data.describe(include='all')
print(descriptive_stats)


# Crear histogramas
variables = ['poblacion', 'nuevas_muertes', 'muertes_acumuladas']
for var in variables:
    plt.figure(figsize=(8, 5))
    sns.histplot(data[var], kde=True, bins=30)
    plt.title(f"Histograma de {var}")
    plt.xlabel(var)
    plt.ylabel("Frecuencia")
    plt.show()

# Crear diagramas de caja
for var in variables:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=data[var])
    plt.title(f"Diagrama de caja de {var}")
    plt.xlabel(var)
    plt.show()



# Query para obtener datos necesarios
query = """
SELECT 
    municipio.municipio, 
    municipio.poblacion
FROM municipio;
"""

# Cargar los datos en un DataFrame
data = pd.read_sql(query, engine)

# Eliminar filas con valores nulos
data = data.dropna()

# Estadísticos descriptivos
descriptive_stats = data['poblacion'].describe()
print(descriptive_stats)

# Crear histograma
plt.figure(figsize=(8, 5))
sns.histplot(data['poblacion'], kde=True, bins=30)
plt.title("Histograma de la población de los municipios")
plt.xlabel("Población")
plt.ylabel("Frecuencia")
plt.show()

# Crear diagrama de caja
plt.figure(figsize=(8, 5))
sns.boxplot(x=data['poblacion'])
plt.title("Diagrama de caja de la población de los municipios")
plt.xlabel("Población")
plt.show()


# Agregar nombres de municipios en vertical
plt.figure(figsize=(10, 8))
plt.barh(data['municipio'], data['poblacion'], color='skyblue')
plt.title("Población por municipio")
plt.xlabel("Población")
plt.ylabel("Municipio")
plt.yticks(fontsize=0.01)  # Reducir el tamaño de los nombres de los municipios
plt.tight_layout()
plt.show()


