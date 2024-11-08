import psycopg2
import re
from datetime import datetime
from unidecode import unidecode  # Importamos la librería para eliminar tildes

# Configuración de la conexión a la base de datos
conn = psycopg2.connect(
    dbname="detector",
    user="postgres",
    password="Dali6478",
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
    # Normalizar la oración: eliminar caracteres no alfabéticos, convertir a minúsculas y eliminar tildes
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
def detector_menu():
    while True:
        print("\n1) Detector de palíndromos\n2) Detector de números primos\n3) Detector de números perfectos")
        option = input("Selecciona una opción: ")

        if option == '1':
            sentence = input("Ingresa una oración: ")
            if not re.search(r'[a-zA-Z]', sentence):
                print("Error: Solo se permiten letras en la oración.")
                continue

            result = "SI" if is_palindrome(sentence) else "NO"
            cursor.execute("INSERT INTO detect (palindromos, resultado) VALUES (%s, %s)", (sentence, result))
            conn.commit()
            message = f"La oración {'SI' if result == 'SI' else 'NO'} es palíndroma"
            print(message)
            save_to_history(f"{datetime.now()} - Palíndromo: {sentence} - Resultado: {result}")

        elif option == '2':
            try:
                number = int(input("Ingresa un número: "))
            except ValueError:
                print("Error: Solo se permiten números.")
                continue

            result = "SI" if is_prime(number) else "NO"
            cursor.execute("INSERT INTO detect (numero, resultado) VALUES (%s, %s)", (number, result))
            conn.commit()
            message = f"El número {'SI' if result == 'SI' else 'NO'} es primo"
            print(message)
            save_to_history(f"{datetime.now()} - Número primo: {number} - Resultado: {result}")

        elif option == '3':
            try:
                number = int(input("Ingresa un número: "))
            except ValueError:
                print("Error: Solo se permiten números.")
                continue

            result = "SI" if is_perfect(number) else "NO"
            cursor.execute("INSERT INTO detect (numero, resultado) VALUES (%s, %s)", (number, result))
            conn.commit()
            message = f"El número {'SI' if result == 'SI' else 'NO'} es perfecto"
            print(message)
            save_to_history(f"{datetime.now()} - Número perfecto: {number} - Resultado: {result}")

        else:
            print("Opción inválida. Inténtalo de nuevo.")
            continue

        again = input("¿Deseas realizar otra operación? (s/n): ").lower()
        if again == 's':
            # Si el usuario elige 's', reiniciar el programa pidiendo el nombre de usuario
            return False  # Esto vuelve al menú principal

        elif again == 'n':
            # Si el usuario elige 'n', cerrar la conexión y salir
            cursor.close()
            conn.close()  # Cerramos la conexión antes de salir.
            print("Saliendo del programa...")
            return True  # Detiene el programa

# Menú principal
def main_menu():
    while True:
        user = input("Ingresa tu nombre de usuario: ")
        cursor.execute("INSERT INTO detect (usuario) VALUES (%s)", (user,))
        conn.commit()

        while True:
            print("\n1) Detector\n2) Historial de datos ingresados\n3) Borrar datos\n4) Salir")
            option = input("Selecciona una opción: ")

            if option == '1':
                if not detector_menu():  # Si el detector retorna False, se detiene la ejecución.
                    break  # Si el detector devuelve True, es que se terminó el proceso.
            elif option == '2':
                cursor.execute("SELECT * FROM detect")
                records = cursor.fetchall()
                for record in records:
                    print(record)
            elif option == '3':
                user_to_delete = input("Ingresa el nombre de usuario cuyos datos deseas borrar: ")
                cursor.execute("DELETE FROM detect WHERE usuario = %s", (user_to_delete,))
                conn.commit()
                print(f"Datos de {user_to_delete} eliminados.")
            elif option == '4':
                print("Saliendo del programa...")
                cursor.close()
                conn.close()  # Cerramos la conexión antes de salir.
                return  # Detenemos el programa al seleccionar la opción de salir.
            else:
                print("Opción inválida. Inténtalo de nuevo.")

# Ejecución del programa
main_menu()
