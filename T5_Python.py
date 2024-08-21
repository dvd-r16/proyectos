import os

# Definición de las categorías
BAJO_PESO = "Bajo peso"
PESO_NORMAL = "Peso normal"
SOBREPESO = "Sobrepeso"

# Función principal
def main():
    while True:
        # Mostrar opciones
        mostrar_opciones()
        
        # Leer la opción del usuario
        try:
            opcion = int(input('Ingrese la opción deseada: '))
        except ValueError:
            print('Opción no válida. Intente de nuevo.')
            continue

        # Validar la opción
        if not (1 <= opcion <= 4):
            print('Opción no válida. Intente de nuevo.')
            continue
        
        # Ejecutar la acción según la opción
        if opcion == 1:
            # Calcular IMC y Mostrar resultados
            calcular_y_mostrar_imc()
        elif opcion == 2:
            # Leer información del archivo
            leer_informacion()
        elif opcion == 3:
            # Borrar información del archivo
            borrar_informacion()
        elif opcion == 4:
            # Salir del programa
            break
    
    # Mensaje de despedida
    print('Gracias por usar el programa!')

# Función para mostrar las opciones disponibles al usuario
def mostrar_opciones():
    print('Opciones:')
    print('1. Calcular IMC')
    print('2. Leer información del archivo')
    print('3. Borrar información del archivo')
    print('4. Salir')

# Función para calcular el IMC y mostrar resultados
def calcular_y_mostrar_imc():
    nombre = input('Ingrese su nombre: ')
    try:
        peso = float(input('Ingrese su peso en kilogramos: '))
        altura = float(input('Ingrese su altura en metros: '))
    except ValueError:
        print("Entrada no válida. Asegúrese de ingresar números.")
        return

    # Calcular IMC
    imc = peso / (altura ** 2)
    print(f'Su IMC es: {imc:.2f}')

    # Determinar la categoría del IMC
    if imc < 18.5:
        categoria = BAJO_PESO
    elif 18.5 <= imc <= 24.9:
        categoria = PESO_NORMAL
    else:
        categoria = SOBREPESO

    print(f'Categoría del IMC: {categoria}')

    # Guardar la información en un archivo si el usuario lo desea
    guardar = input('¿Desea guardar la información en un archivo? (s/n): ').lower()
    if guardar == 's':
        with open('imc_p.txt', 'a') as archivo:
            archivo.write(f'Nombre: {nombre}, Peso: {peso:.2f} kg, Altura: {altura:.2f} m, IMC: {imc:.2f}, Categoría: {categoria}\n')
        print('Información guardada exitosamente.')

# Función para leer la información del archivo
def leer_informacion():
    if os.path.exists('imc_p.txt'):
        with open('imc_p.txt', 'r') as archivo:
            contenido = archivo.read()
            if contenido:
                print(contenido)
            else:
                print("El archivo está vacío.")
    else:
        print('El archivo "imc_p.txt" no existe.')

# Función para borrar la información del archivo
def borrar_informacion():
    if os.path.exists('imc_p.txt'):
        os.remove('imc_p.txt')
        print('Archivo "imc_p.txt" borrado exitosamente.')
    else:
        print('El archivo "imc_p.txt" no existe.')

# Programa inicial
if __name__ == '__main__':
    main()