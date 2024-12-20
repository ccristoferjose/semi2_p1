import mysql.connector
from mysql.connector import Error
from db import db_config

def insert_data(table_name, data, query_template, batch_size=50):
    """
    Inserta datos en una tabla, con manejo de transacciones en lotes.
    Args:
        table_name (str): Nombre de la tabla.
        data (list of tuples): Datos a insertar.
        query_template (str): Plantilla de la consulta SQL.
        batch_size (int): Tamaño del lote para cada transacción.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print(f"Iniciando inserción en la tabla {table_name}...")

        # Procesar datos en lotes
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            cursor.executemany(query_template, batch)
            connection.commit()  # Commit por cada lote
            print(f"Lote {i // batch_size + 1} insertado con éxito ({len(batch)} registros).")

    except Error as e:
        print(f"Error al insertar datos en la tabla {table_name}: {e}")
        connection.rollback()
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print(f"Conexión a la base de datos cerrada.")