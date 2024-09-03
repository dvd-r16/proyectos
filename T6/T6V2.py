import psycopg2
import re

# Función para conectarse a la base de datos PostgreSQL
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            host="localhost",
            port="5432",
            user="postgres",
            password="202010039"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return None

# Función para solicitar la fecha
def solicitar_fecha():
    while True:
        fecha = input('Ingrese la fecha (dd-mm-aaaa): ')
        if not re.match(r'^\d{2}-\d{2}-\d{4}$', fecha):
            print('Formato de fecha inválido. Debe ser dd-mm-aaaa.')
        else:
            return fecha

# Función para ingresar la hora con validación de formato
def ingresar_hora(mensaje):
    while True:
        hora = input(mensaje)
        if not re.match(r'^\d{4}$', hora):
            print('Formato de hora inválido. Debe ser HHMM.')
        else:
            return hora

# Función para calcular el monto a pagar
def calcular_monto(hora_entrada, hora_salida):
    # Convertir horas y minutos
    horas_entrada = int(hora_entrada[:2])
    minutos_entrada = int(hora_entrada[2:])
    horas_salida = int(hora_salida[:2])
    minutos_salida = int(hora_salida[2:])

    # Calcular tiempo total en minutos
    tiempo_total_min = (horas_salida * 60 + minutos_salida) - (horas_entrada * 60 + minutos_entrada)
    if tiempo_total_min <= 0:
        tiempo_total_min += 24 * 60  # manejar si el tiempo cruza la medianoche

    # Convertir tiempo total a horas, redondeando hacia arriba
    tiempo_total = (tiempo_total_min + 59) // 60

    # Calcular monto total
    if tiempo_total > 1:
        monto_total = 15 + (tiempo_total - 1) * 20
    else:
        monto_total = 15
    
    return tiempo_total, monto_total

# Función para guardar la factura en el archivo de texto
def generar_factura_txt(nombre_cliente, id_vehiculo, tiempo_total, monto_total):
    try:
        with open("facturas.txt", "a") as file:
            file.write(f"Nombre del cliente: {nombre_cliente}\n")
            file.write(f"Identificación del vehículo: {id_vehiculo}\n")
            file.write(f"Tiempo en el parqueo: {tiempo_total} horas\n")
            file.write(f"Monto total a pagar: Q{monto_total:.2f}\n")
            file.write("-----------------------------------------\n")
        print("¡Factura guardada en 'facturas.txt' con éxito!")
    except IOError:
        print("Error al escribir en el archivo 'facturas.txt'.")

# Función para guardar la información en un archivo de texto
def guardar_en_salida_txt(nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida):
    try:
        with open("salida.txt", "a") as file:
            file.write(f"Nombre del cliente: {nombre_cliente}\n")
            file.write(f"NIT: {nit_cliente}\n")
            file.write(f"Vehículo: {id_vehiculo}\n")
            file.write(f"Fecha: {fecha}\n")
            file.write(f"Hora Entrada: {hora_entrada}\n")
            file.write(f"Hora Salida: {hora_salida}\n")
            file.write("-----------------------------------------\n")
        print("¡Información guardada en 'salida.txt' con éxito!")
    except IOError:
        print("Error al escribir en el archivo 'salida.txt'.")

# Función para validar que la entrada sea numérica
def validar_entrada_numerica(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            else:
                print("Entrada no válida. Debes ingresar un número positivo.")
        except ValueError:
            print("Entrada no válida. Debes ingresar un número.")

# Función para mostrar el historial desde la base de datos
def mostrar_historial_postgres(conn):
    query = "SELECT * FROM salida;"
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            records = cur.fetchall()
            if not records:
                print("No hay registros en la base de datos aún.")
            else:
                print("\nHistorial de Parqueos (Base de Datos):")
                for i, record in enumerate(records, 1):
                    print(f"Registro {i}:")
                    print(f"Nombre del cliente: {record[0]}")
                    print(f"NIT: {record[1]}")
                    print(f"Vehículo: {record[2]}")
                    print(f"Fecha: {record[3]}")
                    print(f"Hora Entrada: {record[4]}")
                    print(f"Hora Salida: {record[5]}\n")
    except psycopg2.Error as e:
        print(f"Error ejecutando la consulta SQL: {e}")

# Función para mostrar el historial desde el archivo de texto
def mostrar_historial_facturas():
    try:
        with open("facturas.txt", "r") as file:
            print("\nHistorial de Facturas (Archivo de Texto):")
            for linea in file:
                print(linea.strip())
    except IOError:
        print("Error al leer el archivo 'facturas.txt'.")

# Función para borrar el historial en la base de datos
def borrar_historial_postgres(conn):
    confirmacion = input("¿Estás seguro de que deseas borrar todos los registros? (s/n): ").lower()
    if confirmacion == 's':
        query = "DELETE FROM salida;"
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
            print("Historial borrado con éxito.")
        except psycopg2.Error as e:
            print(f"Error ejecutando la consulta SQL: {e}")
    else:
        print("Borrado cancelado.")

# Función para borrar el historial de facturas del archivo de texto
def borrar_historial_facturas():
    confirmacion = input("¿Estás seguro de que deseas borrar todas las facturas? (s/n): ").lower()
    if confirmacion == 's':
        try:
            open("facturas.txt", "w").close()
            print("Historial de facturas borrado con éxito.")
        except IOError:
            print("No se pudo abrir el archivo.")
    else:
        print("Borrado cancelado.")

# Función para guardar la información en la base de datos
def guardar_info_db(conn, nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida):
    query = """
    INSERT INTO salida (nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    try:
        with conn.cursor() as cur:
            cur.execute(query, (nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida))
            conn.commit()
        print("Información guardada en la base de datos con éxito.")
    except psycopg2.Error as e:
        print(f"Error al guardar en la base de datos: {e}")

# Función principal con menú
def main():
    conn = connect_to_db()  # Conectar a la base de datos PostgreSQL
    if conn is None:
        return
    
    while True:
        print("\nSistema de Gestión de Parqueo")
        print("1. Registrar transacción")
        print("2. Ver historial")
        print("3. Borrar historial")
        print("4. Salir")

        opcion = validar_entrada_numerica("Selecciona una opción: ")

        if opcion == 1:
            # Registrar transacción
            nombre_cliente = input("Por favor, ingresa el nombre del cliente: ")
            nit_cliente = input("Ingresa el NIT del cliente: ")
            fecha = solicitar_fecha()
            id_vehiculo = input("Ingresa la identificación del vehículo (número de placa): ")
            hora_entrada = ingresar_hora("Ingresa la hora de entrada (HHMM): ")
            hora_salida = ingresar_hora("Ingresa la hora de salida (HHMM): ")

            # Calcular tiempo total y monto a pagar
            tiempo_total, monto_total = calcular_monto(hora_entrada, hora_salida)

            # Mostrar el monto total en la terminal
            print(f"Monto total a pagar: Q{monto_total:.2f}")

            # Guardar la información en la base de datos
            guardar_info_db(conn, nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida)

            # Guardar la información en el archivo salida.txt
            guardar_en_salida_txt(nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida)

            # Generar factura en facturas.txt
            generar_factura_txt(nombre_cliente, id_vehiculo, tiempo_total, monto_total)

            print("Transacción registrada con éxito.")
        
        elif opcion == 2:
            # Ver historial
            while True:
                print("\nVer Historial")
                print("1. Ver historial de registros")
                print("2. Ver historial de facturas")
                print("3. Regresar al menú principal")

                sub_opcion = validar_entrada_numerica("Selecciona una opción: ")

                if sub_opcion == 1:
                    mostrar_historial_postgres(conn)
                elif sub_opcion == 2:
                    mostrar_historial_facturas()
                elif sub_opcion == 3:
                    break
                else:
                    print("Opción no válida. Por favor, selecciona una opción correcta.")
        
        elif opcion == 3:
            # Borrar historial
            while True:
                print("\nBorrar Historial")
                print("1. Borrar historial de registros")
                print("2. Borrar historial de facturas")
                print("3. Regresar al menú principal")

                sub_opcion = validar_entrada_numerica("Selecciona una opción: ")

                if sub_opcion == 1:
                    borrar_historial_postgres(conn)
                elif sub_opcion == 2:
                    borrar_historial_facturas()
                elif sub_opcion == 3:
                    break
                else:
                    print("Opción no válida. Por favor, selecciona una opción correcta.")
        
        elif opcion == 4:
            # Salir del programa
            print("Saliendo del programa. ¡Hasta pronto!")
            conn.close()  # Cerrar la conexión a la base de datos
            break

        else:
            print("Opción no válida. Por favor, selecciona una opción correcta.")

if __name__ == "__main__":
    main()
