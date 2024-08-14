import psycopg2


try:
    connection = psycopg2.connect(
        host='localhost',
        user='postgres',
        password='202010039',
        database='postgres'
    )

    print("Conexion exitosa.")
    cursor = connection.cursor()
    cursor.execute("SELECT version()")
    row = cursor.fetchone()
    cursor.execute("SELECT * from T202010039")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

finally:
    connection.close()  # Se cerró la conexión a la BD.
    print("La conexion ha finalizado.")