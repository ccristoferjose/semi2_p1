# Descripción del Proyecto: Visualización y Análisis de Datos en Power BI

## Introducción
Este manual documenta el desarrollo del proyecto enfocado en la creación de dashboards interactivos utilizando Power BI. Estos dashboards se basan en los datos recopilados por el Ministerio de Salud de Guatemala durante la pandemia de COVID-19 en 2020. La etapa previa del proyecto consistió en el análisis y procesamiento de datos para su carga en una base de datos SQL. Ahora, la visualización de datos permite extraer y comunicar información clave de manera efectiva.


## Dashboard 1: Fallecidos por Municipio

Este dashboard presenta la información de fallecimientos por municipio, permitiendo identificar tendencias locales y analizar correlaciones entre la población y las muertes.

![img](/images/dash1.png)

Las gráficas utilizadas en este dashboard fueron seleccionadas para maximizar la claridad y comprensión de los datos representados. El gráfico de barras permite visualizar fácilmente las diferencias en el número de muertes entre municipios, destacando las áreas más afectadas. El gráfico de líneas muestra de manera clara la evolución acumulada de muertes a lo largo del tiempo, permitiendo identificar tendencias. La dispersión facilita el análisis de correlación entre la población y las muertes, ayudando a evaluar la relación entre estos factores. El mapa interactivo ofrece una representación geográfica intuitiva que permite localizar rápidamente los municipios afectados. Finalmente, los indicadores clave brindan métricas resumidas como la tasa de mortalidad, días registrados y máximos fallecimientos diarios, proporcionando un resumen cuantitativo que complementa las visualizaciones detalladas. Esta combinación de elementos visuales asegura una comprensión integral y una navegación interactiva para los usuarios.

## Dashboard 2: Fallecidos por Departamento

Este dashboard amplía el análisis a nivel departamental, permitiendo comparar regiones con mayor y menor impacto.

![img](/images/dash2.png)

Las gráficas empleadas en este dashboard fueron seleccionadas para facilitar el análisis a nivel departamental, destacando patrones y tendencias clave. El gráfico de barras permite comparar rápidamente las muertes totales entre departamentos, mientras que el gráfico de líneas acumuladas muestra las tendencias de crecimiento en cada región a lo largo del tiempo. El gráfico de dispersión ayuda a analizar la distribución de los valores acumulados, destacando departamentos con características atípicas. El mapa interactivo proporciona una representación geográfica clara, visualizando el impacto regional con círculos proporcionales al número de muertes. Finalmente, los indicadores clave, como la tasa de mortalidad y el máximo de muertes, resumen información crítica, mientras que los filtros y segmentadores interactivos permiten una exploración detallada de datos específicos por departamento y fechas. Esta combinación asegura una interpretación integral y precisa de los datos departamentales.

## Objetivo del Dashboard 3: Datos Globales

El tercer dashboard del proyecto está diseñado para ofrecer una comparación entre los datos locales del Ministerio de Salud de Guatemala y datos globales relacionados con la pandemia de COVID-19. Este dashboard incluye indicadores clave que permiten a los usuarios explorar las diferencias entre los datos locales y globales, y visualizar tendencias que revelan patrones y anomalías en los datos.

![img](/images/dash2.png)

Las gráficas de este dashboard fueron seleccionadas para proporcionar una comparación clara y precisa entre los datos de Guatemala y las tendencias globales relacionadas con la pandemia. El gráfico de líneas que compara las muertes diarias locales y globales permite identificar patrones de variación y similitudes en el impacto de la pandemia. El gráfico de barras refleja visualmente la diferencia entre la tasa de mortalidad en Guatemala y el promedio global, destacando discrepancias importantes.

El gráfico de líneas acumuladas para muertes y el promedio global ofrece una perspectiva clara sobre el progreso acumulativo del impacto local frente al global, mientras que el gráfico combinado de líneas y barras para nuevos casos diarios y muertes acumuladas muestra simultáneamente tendencias específicas de nuevos contagios junto con las consecuencias acumulativas, lo que facilita un análisis completo.

Finalmente, los segmentadores de país y rango de fechas permiten una exploración interactiva, permitiendo al usuario ajustar el análisis a contextos y períodos específicos, lo que mejora la utilidad del dashboard para la toma de decisiones basada en datos.
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

La conexión de Power BI con la base de datos MySQL alojada en Amazon RDS se realizó configurando el endpoint de la instancia RDS, junto con las credenciales de acceso proporcionadas. En Power BI, se utilizó la opción "Obtener datos" seleccionando el conector MySQL y estableciendo la conexión segura con SSL para garantizar la protección de los datos. Las tablas adicionales en formato CSV se cargaron directamente en Power BI mediante el editor de consultas, donde se realizó la limpieza de datos y se relacionaron con las tablas de la base de datos para complementar los análisis y enriquecer los dashboards.


### 2. Inserción en Tablas Normalizadas
#### Esquema Final Adaptado

![img](/images/2.png)

#### Esquema Modificado

El esquema organiza la información en tablas relacionadas para gestionar datos locales y globales, ampliando la capacidad analítica más allá de los límites nacionales. A continuación, se describe la función de cada tabla en el nuevo esquema:

- **Tablas involucradas**:
  - **Tabla `departamento`:**  
  Almacena un identificador único y el nombre de cada departamento, siendo la base para agrupar datos a nivel departamental.

- **Tabla `municipio`:**  
  Relaciona cada municipio con su departamento, junto con información sobre su población. Esto permite realizar análisis detallados a nivel municipal.

- **Tabla `evento_municipal`:**  
  Registra eventos específicos en cada municipio, incluyendo fechas y cantidades, para un seguimiento granular de los impactos locales.

- **Tabla `reporte_nacional`:**  
  Contiene datos agregados a nivel nacional, como nuevos casos, casos acumulados, nuevas muertes y muertes acumuladas por fecha, permitiendo análisis enfocados en el contexto de Guatemala.

- **Tabla `evento`:**  
  Vincula eventos locales con los datos de reportes nacionales, facilitando la conexión entre información detallada a nivel municipal y métricas más amplias.

- **Tabla `world_population_2023`:**  
  Integra datos demográficos globales, esenciales para calcular tasas de mortalidad y realizar comparaciones entre Guatemala y otros países.

- **Tabla `reporte_global`:**  
  Almacena datos agregados de otros países, como nuevos casos y muertes acumuladas, permitiendo un análisis comparativo a nivel mundial.

- **Tabla `tabla_fechas`:**  
  Actúa como una tabla de soporte para relacionar fechas entre los reportes nacionales y globales, garantizando consistencia y eficiencia en las consultas cruzadas.

- **Tabla `indicadores_departamento`:**  
  Proporciona métricas clave como variación diaria de muertes y totales por departamento, generadas a partir de consultas SQL avanzadas, para análisis detallados en el contexto departamental.


#### **1. Tabla de Población Mundial 2023 (`world_population_2023`)**
- **Justificación:**  
  Los datos originales no contenían información demográfica global. Esta tabla fue esencial para calcular la tasa de mortalidad a nivel mundial y compararla con Guatemala, proporcionando un contexto más amplio y relevante para el análisis. Sin esta tabla, no hubiera sido posible analizar el impacto relativo de la pandemia en un marco global.

---

#### **2. Tabla de Reporte Global (`reporte_global`)**
- **Justificación:**  
  El esquema inicial estaba enfocado únicamente en los datos de Guatemala. Esta nueva tabla permitió integrar datos de otros países, lo cual fue indispensable para realizar comparaciones globales, analizar tendencias internacionales y entender el impacto relativo de la pandemia en Guatemala frente a otros contextos.

---

#### **3. Tabla de Fechas (`tabla_fechas`)**
- **Justificación:**  
  Esta tabla fue necesaria para vincular de manera eficiente los datos de `reporte_nacional` y `reporte_global`, ya que las fechas servían como punto común de referencia. Su inclusión optimizó el rendimiento al realizar consultas entre los dos conjuntos de datos, asegurando una estructura relacional clara y precisa.

---

#### **4. Tabla de Indicadores por Departamento (`indicadores_departamento`)**
- **Justificación:**  
  Esta tabla fue generada a partir de una consulta SQL avanzada para calcular indicadores clave como la variación diaria de muertes por departamento. Dado que estos datos no estaban presentes en el esquema original, esta tabla permitió desglosar y analizar el impacto a nivel departamental, proporcionando métricas más detalladas y específicas que mejoraron la granularidad del análisis.


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

### **Entorno de Trabajo con Power BI, Amazon RDS y React**

1. **Entorno de Trabajo**:
   - Tener instalada la herramienta Power BI Desktop.
   - Acceso a un entorno de desarrollo React configurado para crear una interfaz web interactiva.
   - Configuración de una base de datos MySQL en Amazon RDS.

2. **Base de Datos**:
   - Conexión de Power BI a Amazon RDS utilizando el endpoint de la instancia RDS, junto con las credenciales proporcionadas.
   - Carga y limpieza de datos adicionales en Power BI desde archivos CSV para integrarlos con las tablas de MySQL.

3. **Conocimientos Previos**:
   - Conocimientos básicos de SQL para explorar datos en Amazon RDS.
   - Habilidad en Power BI para transformar, limpiar y visualizar datos.
   - Familiaridad con React para crear una aplicación web que integre los dashboards de Power BI embebidos.

---

### **Pasos para la Conexión y Visualización**

#### 1. Conexión a la Base de Datos en Power BI:
1. Configura la conexión desde Power BI seleccionando **Obtener datos** > **MySQL**:
   - Introduce el endpoint de Amazon RDS, puerto, nombre de la base de datos, usuario y contraseña.
   - Habilita SSL para asegurar la transferencia de datos.
2. Una vez conectado, selecciona las tablas relevantes y cárgalas al modelo de datos en Power BI.

#### 2. Limpieza y Relación de Datos:
- Limpia y transforma las tablas en Power BI utilizando el editor de consultas.
- Relaciona las tablas importadas de MySQL con los datos cargados desde archivos CSV para enriquecer los análisis.

#### 3. Publicación de Dashboards en React:
1. Publica los dashboards creados en Power BI en el servicio Power BI Online.
2. Genera un enlace embebido o token de acceso para integrar los dashboards en React.
3. En React, utiliza el componente `iframe` o bibliotecas específicas como `powerbi-client-react` para mostrar los dashboards de Power BI en la aplicación web.

---

### **Resultado Final**
Los datos procesados en Amazon RDS y los gráficos creados en Power BI se presentan en una aplicación web React, ofreciendo una experiencia interactiva y accesible para los usuarios finales. La solución combina la potencia analítica de Power BI con la flexibilidad de React para una visualización dinámica y moderna.
