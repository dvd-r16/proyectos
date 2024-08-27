import psycopg2
import os

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            host="localhost",
            port="5432",
            user="postgres",
            password="202010039"
        )
        print("Conexión exitosa a la base de datos")
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return None
# Función para seleccionar el tipo de combustible
def seleccionar_combustible():
    print("\nSelecciona el tipo de combustible:")
    print("1. Gasolina Regular")
    print("2. Gasolina Súper")
    print("3. Diesel")
    print("4. Vpower")

    opcion = validar_entrada_numerica("Selecciona una opción: ")

    if opcion == 1:
        return "Gasolina Regular"
    elif opcion == 2:
        return "Gasolina Súper"
    elif opcion == 3:
        return "Diesel"
    elif opcion == 4:
        return "Vpower"
    else:
        print("Opción no válida. Selecciona una opción válida.")
        return seleccionar_combustible()

# Función para ingresar la cantidad de litros con validación de entrada numérica
def ingresar_litros():
    cantidad_litros = validar_entrada_numerica("Ingresa la cantidad de litros a despachar: ")
    if cantidad_litros <= 0:
        print("La cantidad de litros debe ser un número positivo. Intenta de nuevo.")
        return ingresar_litros()
    return cantidad_litros

# Función para obtener el precio por litro según el tipo de combustible
def obtener_precio_combustible(tipo_combustible):
    precios = {
        "Gasolina Regular": 3.50,
        "Gasolina Súper": 4.00,
        "Diesel": 3.00,
        "Vpower": 4.50
    }
    return precios.get(tipo_combustible, 0)

# Función para calcular el monto total a pagar
def calcular_monto(cantidad_litros, precio_por_litro):
    return cantidad_litros * precio_por_litro

# Función para mostrar el resumen de la transacción
def mostrar_resumen(nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total):
    print("\nResumen de la Transacción:")
    print(f"Nombre del cliente: {nombre_cliente}")
    print(f"Identificación del vehículo: {identificacion_vehiculo}")
    print(f"Tipo de combustible: {tipo_combustible}")
    print(f"Cantidad de litros: {cantidad_litros:.2f}")
    print(f"Precio por litro: Q. {precio_por_litro:.2f}")
    print(f"Monto total a pagar: Q. {monto_total:.2f}")

# Función para guardar la factura en la base de datos
def guardar_factura(conn, nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total):
    query = """
        INSERT INTO facturas (nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    valores = (nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total)

    try:
        with conn.cursor() as cur:
            cur.execute(query, valores)
            conn.commit()
            print("¡Factura registrada en la base de datos!")
    except psycopg2.Error as e:
        print(f"Error ejecutando la consulta SQL: {e}")
        conn.rollback()

# Función para generar la factura en el archivo de texto
def generar_factura_txt(nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total):
    # Ruta específica para guardar el archivo
    directorio = r"D:\Desktop\Proyectos"  # Cambia a la ruta deseada
    archivo = os.path.join(directorio, "facturas.txt")
    try:
        with open("facturas.txt", "a") as file:
            file.write(f"Nombre del cliente: {nombre_cliente}\n")
            file.write(f"Identificación del vehículo: {identificacion_vehiculo}\n")
            file.write(f"Tipo de combustible: {tipo_combustible}\n")
            file.write(f"Cantidad de litros: {cantidad_litros:.2f}\n")
            file.write(f"Precio por litro: Q. {precio_por_litro:.2f}\n")
            file.write(f"Monto total a pagar: Q. {monto_total:.2f}\n")
            file.write("-----------------------------------------\n")
        print("¡Factura guardada en 'facturas.txt' con éxito!")
        return True
    except Exception as e:
        print(f"Error al escribir en el archivo 'facturas.txt': {e}")
        return False

# Función para validar que la entrada sea numérica
def validar_entrada_numerica(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("Entrada no válida. Debes ingresar un número.")

# Función para ver el historial de facturas desde la base de datos
def ver_historial_facturas(conn):
    query = "SELECT * FROM facturas;"
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            facturas = cur.fetchall()
            if not facturas:
                print("No hay facturas registradas aún.")
            else:
                print("\nHistorial de Facturas:")
                for i, factura in enumerate(facturas, 1):
                    print(f"Factura {i}:")
                    print(f"Nombre del cliente: {factura[0]}")
                    print(f"Identificación del vehículo: {factura[1]}")
                    print(f"Tipo de combustible: {factura[2]}")
                    print(f"Cantidad de litros: {factura[3]:.2f}")
                    print(f"Precio por litro: Q. {factura[4]:.2f}")
                    print(f"Monto total: Q. {factura[5]:.2f}\n")
    except psycopg2.Error as e:
        print(f"Error ejecutando la consulta SQL: {e}")

# Función para borrar el historial de facturas en la base de datos
def borrar_historial_facturas(conn):
    confirmacion = input("¿Estás seguro de que deseas borrar todas las facturas? (s/n): ").lower()
    if confirmacion == 's':
        query = "DELETE FROM facturas;"
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()
                print("Historial de facturas borrado con éxito.")
        except psycopg2.Error as e:
            print(f"Error ejecutando la consulta SQL: {e}")
            conn.rollback()
    else:
        print("Borrado cancelado.")

# Función principal con menú
def main():
    conn = connect_to_db()
    if conn is None:
        return
    
    while True:
        print("\nSistema de Gestión de Combustible")
        print("1. Registrar transacción")
        print("2. Ver historial de facturas")
        print("3. Borrar historial de facturas")
        print("4. Salir")

        opcion = validar_entrada_numerica("Selecciona una opción: ")

        if opcion == 1:
            # Registrar transacción de combustible
            nombre_cliente = input("Por favor, ingresa el nombre del cliente: ")
            identificacion_vehiculo = input("Ingresa la identificación del vehículo (número de placa): ")
            tipo_combustible = seleccionar_combustible()
            cantidad_litros = ingresar_litros()
            precio_por_litro = obtener_precio_combustible(tipo_combustible)
            monto_total = calcular_monto(cantidad_litros, precio_por_litro)
            mostrar_resumen(nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total)
            guardar_factura(conn, nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total)
            if not generar_factura_txt(nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total):
                print("Error al escribir en el archivo 'facturas.txt'. Programa terminado.")
                break
            print("Transacción registrada con éxito.")
            input("Presiona Enter para continuar...")
        
        elif opcion == 2:
            # Ver historial de facturas
            ver_historial_facturas(conn)
            input("\nPresiona Enter para regresar al menú principal...")
        
        elif opcion == 3:
            # Borrar historial de facturas
            borrar_historial_facturas(conn)
            input("Presiona Enter para continuar...")

        elif opcion == 4:
            # Salir del programa
            print("Saliendo del programa. ¡Hasta pronto!")
            if conn is not None:
                conn.close()  # Cerrar la conexión a la base de datos
            break

        else:
            print("Opción no válida. Por favor, selecciona una opción correcta.")
            input("Presiona Enter para continuar...")

# Verifica que el script se esté ejecutando directamente
if __name__ == "__main__":
    main()