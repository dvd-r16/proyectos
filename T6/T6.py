import math

def calcular_estacionamiento():
    # Solicitar datos al usuario
    nombre_cliente = input('Ingrese el nombre del cliente: ')
    nit_cliente = input('Ingrese el NIT del cliente: ')
    identificacion_vehiculo = input('Ingrese la identificación del vehículo (placa): ')
    hora_entrada = input('Ingrese la hora de entrada (HH:MM): ')
    hora_salida = input('Ingrese la hora de salida (HH:MM): ')

    # Convertir horas a minutos
    hora_entrada_minutos = convertir_hora_a_minutos(hora_entrada)
    hora_salida_minutos = convertir_hora_a_minutos(hora_salida)

    # Calcular tiempo en el estacionamiento en horas completas
    tiempo_total = math.ceil((hora_salida_minutos - hora_entrada_minutos) / 60)

    # Calcular monto a pagar
    if tiempo_total <= 1:
        monto_total = 15
    else:
        monto_total = 15 + (tiempo_total - 1) * 20

    # Mostrar resumen de la transacción
    print('Resumen de la transacción:')
    print(f'Nombre del cliente: {nombre_cliente}')
    print(f'Identificación del vehículo: {identificacion_vehiculo}')
    print(f'Tiempo en el estacionamiento: {tiempo_total} horas')
    print(f'Monto total a pagar: Q{monto_total:.2f}')

    # Guardar información en archivo de texto
    with open('facturas.txt', 'a') as archivo_factura:
        archivo_factura.write(f'Nombre del cliente: {nombre_cliente}\n')
        archivo_factura.write(f'NIT del cliente: {nit_cliente}\n')
        archivo_factura.write(f'Identificación del vehículo: {identificacion_vehiculo}\n')
        archivo_factura.write(f'Hora de entrada: {hora_entrada}\n')
        archivo_factura.write(f'Hora de salida: {hora_salida}\n')
        archivo_factura.write(f'Tiempo en el estacionamiento: {tiempo_total} horas\n')
        archivo_factura.write(f'Monto total a pagar: Q{monto_total:.2f}\n')
        archivo_factura.write('-----------------------------\n')

def convertir_hora_a_minutos(hora):
    horas, minutos = map(int, hora.split(':'))
    return horas * 60 + minutos

if __name__ == "__main__":
    calcular_estacionamiento()
