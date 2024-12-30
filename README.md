# Manual de Usuario: ETL Limpieza y Procesamiento de Datos para Inserción en MySQL

## Introducción
Este documento describe los pasos realizados para limpiar, procesar y preparar los datos provenientes de archivos CSV antes de su inserción en una base de datos MySQL. Se detalla cómo se han manejado los valores nulos, los datos duplicados y las transformaciones necesarias para normalizar los datos en un esquema relacional.

---

## Proceso de Limpieza de Datos

### 1. Descarga de Archivos
- **Archivos involucrados**:
  - `global_calificacion.csv`: Contiene datos de casos globales reportados.
  - `municipio.csv`: Proporciona información local sobre municipios.
- **Validación previa**:
  - Verificamos si los archivos ya existen localmente para evitar descargas innecesarias.
  - Si no existen, los archivos se descargan desde la URL proporcionada utilizando `requests`.

### 2. Filtrado Inicial de Datos
- **Archivo `global_calificacion.csv`**:
  - Seleccionamos exclusivamente registros correspondientes a Guatemala usando la columna `Country`.
  - Los registros duplicados se eliminan para evitar redundancia.
  - Se manejan valores nulos reemplazándolos con `0` en las columnas:
    - `New_cases`
    - `Cumulative_cases`
    - `New_deaths`
    - `Cumulative_deaths`

- **Archivo `municipio.csv`**:
  - Reformateamos los datos de "ancho" a "largo" para tener una columna `Fecha` y otra `Casos`.
  - Convertimos las columnas numéricas (`Codigo_departamento`, `Codigo_municipio`, `Poblacion`, `Casos`) a enteros, rellenando valores faltantes con `0`.

### 3. Combinación de Datos
- Unimos los dos DataFrames (`global_calificacion` y `municipio`) usando la columna `Fecha` como referencia.
- **Manejo de datos no válidos**:
  - Se eliminan registros donde `Codigo_departamento` o `Codigo_municipio` son nulos.
  - Registros con valores "No disponible" en las columnas `Departamento` o `Municipio` también son eliminados.

---

## Inserción en MySQL

### 1. Conexión a la Base de Datos
- Configuramos la conexión usando las credenciales proporcionadas (usuario, contraseña, nombre de la base de datos, etc.).
- Se desactivan las verificaciones de claves foráneas temporalmente para evitar conflictos durante la inserción masiva.

### 2. Inserción en Tablas Normalizadas
#### Esquema original

![img](/images/1.png)

- **Tablas involucradas**:
  1. **`regiones`**:
      - Insertamos las regiones únicas provenientes de `WHO_region`.
  2. **`departamentos`**:
      - Insertamos los departamentos únicos con su nombre y código.
  3. **`municipios`**:
      - Insertamos los municipios junto con su código, el ID del departamento relacionado y su población.
  4. **`casos`**:
      - Insertamos los datos de casos, vinculando las regiones y municipios mediante subconsultas.

#### Esquema Modificado

El esquema organiza la información en tablas relacionadas para gestionar datos de departamentos, municipios, eventos y reportes nacionales. La tabla departamento almacena un identificador único y el nombre de cada departamento, mientras que municipio relaciona cada municipio con su departamento, junto con su población. La tabla evento_municipal registra eventos específicos en cada municipio, con fechas y cantidades. Por otro lado, reporte_nacional almacena datos agregados a nivel nacional, incluyendo nuevos casos, casos acumulados, nuevas muertes y muertes acumuladas por fecha. Finalmente, la tabla evento vincula eventos locales con los datos de reportes nacionales, permitiendo relacionar información detallada a nivel municipal con métricas más amplias. Este diseño facilita consultas y análisis cruzados entre los niveles regional y nacional.

```sql
CREATE TABLE departamento (
    codigo_departamento INT PRIMARY KEY,
    departamento VARCHAR(50) NOT NULL
);


CREATE TABLE municipio (
    codigo_municipio INT PRIMARY KEY,
    municipio VARCHAR(100) NOT NULL,
    codigo_departamento INT NOT NULL,
    poblacion INT UNSIGNED NOT NULL,
    FOREIGN KEY (codigo_departamento) REFERENCES departamento(codigo_departamento)
);


CREATE TABLE evento_municipal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_municipio INT NOT NULL,
    fecha DATE NOT NULL,
    eventos INT NOT NULL,
    FOREIGN KEY (codigo_municipio) REFERENCES municipio(codigo_municipio)
);


CREATE TABLE reporte_nacional (
    Date_reported DATE PRIMARY KEY,
    New_cases INT UNSIGNED NOT NULL,
    Cumulative_cases INT UNSIGNED NOT NULL,
    New_deaths INT UNSIGNED NOT NULL,
    Cumulative_deaths INT UNSIGNED NOT NULL
);

CREATE TABLE evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_municipio INT NOT NULL,
    fecha DATE NOT NULL,
    Date_reported DATE NOT NULL,
    FOREIGN KEY (codigo_municipio) REFERENCES municipio(codigo_municipio),
    FOREIGN KEY (Date_reported) REFERENCES reporte_nacional(Date_reported)
);


```
El nuevo esquema es superior al antiguo porque ofrece una estructura más modular, normalizada y escalable, que facilita análisis detallados a nivel municipal, departamental y nacional. Al separar eventos municipales y reportes nacionales en tablas específicas, se eliminan redundancias y se mejora la flexibilidad para realizar consultas cruzadas. Además, las relaciones más claras entre entidades permiten un control granular de los datos locales y globales, mientras que la capacidad de manejar múltiples eventos asociados a fechas específicas incrementa la escalabilidad. En general, el nuevo esquema es más adecuado para proyectos que requieren análisis complejos y expansión futura sin comprometer la consistencia de los datos.

---

1. **Entorno de Trabajo**:
- Tener instalado Python 3.x.
- Instalar las bibliotecas requeridas: `pandas`, `matplotlib`, `seaborn`, `numpy`.
- Opcional: Uso de Jupyter Notebook o Google Colab para el desarrollo del análisis.

2. **Base de Datos**:
- Acceso a la base de datos SQL con los datos procesados previamente mediante un proceso ETL.
- Herramienta para conectar Python a la base de datos: `mysql-connector-python` o `SQLAlchemy`.

3. **Conocimientos Previos**:
- Manejo básico de SQL.
- Análisis exploratorio de datos (EDA).
- Generación de gráficos estadísticos.
Pasos para el Análisis
### 1. Conexión a la Base de Datos
1. Configura la conexión a la base de datos SQL desde Python:

```python
import mysql.connector as mysql

db = mysql.connect(
    host="localhost",
    user="tu_usuario",
    password="tu_contraseña",
    database="nombre_base_datos"
)

cursor = db.cursor()
```
2. Extrae los datos relevantes con consultas SQL:

```python
query = "SELECT * FROM tabla_datos"
cursor.execute(query)
datos = cursor.fetchall()
```

### 2. Análisis Univariable
#### a. Datos Cuantitativos
Realiza análisis de variables como cantidad de nuevas muertes (`new_cases`), acumuladas (`cumulative_cases`) y población (`poblacion`).

#### Estadísticos a Calcular
```python
import pandas as pd
df = pd.DataFrame(datos, columns=["municipio", "new_cases", "cumulative_cases", "poblacion"])
print(df.describe())
```

#### b. Gráficos
```python
import matplotlib.pyplot as plt
df["new_cases"].hist()
plt.show()
```

### 3. Identificación de Outliers
```python
q1, q3 = df["new_cases"].quantile(0.25), df["new_cases"].quantile(0.75)
outliers = df[(df["new_cases"] < (q1 - 1.5 * (q3-q1))) | (df["new_cases"] > (q3 + 1.5 * (q3-q1)))]
print(outliers)
```


