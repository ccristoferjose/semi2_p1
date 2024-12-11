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
- **Tablas involucradas**:
  1. **`regiones`**:
      - Insertamos las regiones únicas provenientes de `WHO_region`.
  2. **`departamentos`**:
      - Insertamos los departamentos únicos con su nombre y código.
  3. **`municipios`**:
      - Insertamos los municipios junto con su código, el ID del departamento relacionado y su población.
  4. **`casos`**:
      - Insertamos los datos de casos, vinculando las regiones y municipios mediante subconsultas.

- **Manejo de Errores**:
  - Para cada inserción:
    - Si no se encuentra una región o municipio, se omite el registro con un mensaje de advertencia.
    - Las operaciones de inserción utilizan comandos como `INSERT IGNORE` para evitar duplicados.

- **Reactivación de Claves Foráneas**:
  - Una vez finalizadas todas las inserciones, se vuelven a activar las verificaciones de claves foráneas.

---

## Consideraciones Finales
- **Optimizaciones implementadas**:
  - Eliminación de datos no válidos antes de la inserción.
  - Uso de transacciones para asegurar la consistencia de los datos.

- **Posibles problemas y solución**:
  - Valores "NaN" o "No disponible": Se eliminan antes de la inserción.
  - Conflictos de claves foráneas: Se desactivan temporalmente para garantizar una inserción fluida.

---

## Ejecución del Código
Para ejecutar este script, asegúrese de:
1. Tener los archivos `global_calificacion.csv` y `municipio.csv` en el directorio local o accesibles mediante las URLs proporcionadas.
2. Configurar correctamente las credenciales de conexión a MySQL en `db_config`.
3. Instalar las librerías necesarias:
   ```bash
   pip install pandas mysql-connector-python requests

4. Ejecutar el script:
   ```bash
   python main.py