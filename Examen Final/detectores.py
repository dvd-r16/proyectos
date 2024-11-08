import psycopg2
import re
from datetime import datetime
from unidecode import unidecode  # Importamos la librería para eliminar tildes

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    dbname="detector",
    user="postgres",
    password="202010039",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Función para almacenar en el archivo .txt
def save_to_history(data):
    with open("history.txt", "a") as file:
        file.write(data + "\n")

# Funciones para el detector
def is_palindrome(sentence):
    normalized = re.sub(r'[^a-zA-Z]', '', unidecode(sentence).lower())
    return normalized == normalized[::-1]

def is_prime(number):
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

def is_perfect(number):
    return number > 1 and sum(i for i in range(1, number) if number % i == 0) == number

# Función principal del menú del detector
def detector_menu(user):
    while True:
        print("\n1) Detector de palíndromos\n2) Detector de números primos\n3) Detector de números perfectos")
        option = input("Selecciona una opción: ")

        if option == '1':
            sentence = input("Ingresa una oración: ")
            if not re.search(r'[a-zA-Z]', sentence):
                print("Error: Solo se permiten letras en la oración.")
                continue

            result = "SI" if is_palindrome(sentence) else "NO"
            cursor.execute("INSERT INTO detector (usuario, palindromos, resultado) VALUES (%s, %s, %s)", 
                           (user, sentence, result))
            conn.commit()
            message = f"La oración {'SI' if result == 'SI' else 'NO'} es palíndroma"
            print(message)
            save_to_history(f"{datetime.now()} - Usuario: {user} - Palíndromo: {sentence} - Resultado: {result}")

        elif option == '2':
            try:
                number = int(input("Ingresa un número: "))
            except ValueError:
                print("Error: Solo se permiten números.")
                continue

            result = "SI ES PRIMO" if is_prime(number) else "NO ES PRIMO"
            cursor.execute("INSERT INTO detector (usuario, numero, resultado) VALUES (%s, %s, %s)", 
                           (user, number, result))
            conn.commit()
            message = f"El número {result}"
            print(message)
            save_to_history(f"{datetime.now()} - Usuario: {user} - Número primo: {number} - Resultado: {result}")

        elif option == '3':
            try:
                number = int(input("Ingresa un número: "))
            except ValueError:
                print("Error: Solo se permiten números.")
                continue

            result = "SI ES PERFECTO" if is_perfect(number) else "NO ES PERFECTO"
            cursor.execute("INSERT INTO detector (usuario, numero, resultado) VALUES (%s, %s, %s)", 
                           (user, number, result))
            conn.commit()
            message = f"El número {result}"
            print(message)
            save_to_history(f"{datetime.now()} - Usuario: {user} - Número perfecto: {number} - Resultado: {result}")

        else:
            print("Opción inválida. Inténtalo de nuevo.")
            continue

        again = input("¿Deseas realizar otra operación? (s/n): ").lower()
        if again == 'n':
            return  # Salir del detector_menu y regresar a main_menu

# Menú principal
def main_menu():
    while True:
        user = input("Ingresa tu nombre de usuario: ").strip()
        while not user:  # Verificar si el usuario ingresó un nombre en blanco
            print("Debe ingresar un nombre de usuario válido.")
            user = input("Ingresa tu nombre de usuario: ").strip()
        
        user = f"{user} - Python"  # Agregar el identificador "- Python" al usuario
        # Insertar inicio de sesión con "////////////" en columnas `palindromos` y `resultado`, y NULL en `numero`
        cursor.execute("INSERT INTO detector (usuario, palindromos, numero, resultado) VALUES (%s, %s, %s, %s)", 
                       (user, "////////////", None, "////////////"))
        conn.commit()

        while True:
            print("\n1) Detector\n2) Historial de datos ingresados\n3) Borrar datos\n4) Salir")
            option = input("Selecciona una opción: ")

            if option == '1':
                detector_menu(user)  # Llamar al detector_menu sin volver a pedir el nombre de usuario
            elif option == '2':
                cursor.execute("SELECT * FROM detector WHERE usuario = %s", (user,))
                records = cursor.fetchall()
                for record in records:
                    print(record)
            elif option == '3':
                user_to_delete = input("Ingresa el nombre de usuario cuyos datos deseas borrar: ").strip()
                user_to_delete = f"{user_to_delete} - Python"  # Agregar "- Python" al nombre del usuario
                cursor.execute("DELETE FROM detector WHERE usuario = %s", (user_to_delete,))
                conn.commit()
                print(f"Datos de {user_to_delete} eliminados.")
            elif option == '4':
                print("Saliendo del programa...")
                cursor.close()
                conn.close()  # Cerrar la conexión antes de salir
                return  # Detener el programa al seleccionar la opción de salir
            else:
                print("Opción inválida. Inténtalo de nuevo.")

# Ejecución del programa
main_menu()
