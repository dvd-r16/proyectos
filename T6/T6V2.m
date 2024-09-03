pkg load database;

% Función para conectarse a la base de datos PostgreSQL
function conn = connect_to_db()
  conn = pq_connect(setdbopts("dbname", "postgres", "host", "localhost", "port", "5432", "user", "postgres", "password", "202010039"));
end

% Función para solicitar la fecha
function fecha = solicitar_fecha()
  while true
    fecha = input('Ingrese la fecha (dd-mm-aaaa): ', 's');
    if isempty(regexp(fecha, '^\d{2}-\d{2}-\d{4}$', 'once'))
      printf('Formato de fecha inválido. Debe ser dd-mm-aaaa.\n');
    else
      break;
    end
  end
end

% Función para ingresar la hora con validación de formato
function hora = ingresar_hora(mensaje)
  while true
    hora = input(mensaje, 's');
    if isempty(regexp(hora, '^\d{2}\d{2}$', 'once'))
      printf('Formato de hora inválido. Debe ser HHMM.\n');
    else
      break;
    end
  end
end

% Función para calcular el monto a pagar
function [tiempo_total, monto_total] = calcular_monto(hora_entrada, hora_salida)
    % Convertir horas y minutos
    horas_entrada = str2double(hora_entrada(1:2));
    minutos_entrada = str2double(hora_entrada(3:4));
    horas_salida = str2double(hora_salida(1:2));
    minutos_salida = str2double(hora_salida(3:4));

    % Calcular tiempo total en minutos
    tiempo_total_min = (horas_salida * 60 + minutos_salida) - (horas_entrada * 60 + minutos_entrada);
    if tiempo_total_min <= 0
        tiempo_total_min = tiempo_total_min + 24 * 60; % manejar si el tiempo cruza la medianoche
    end

    % Convertir tiempo total a horas, redondeando hacia arriba
    tiempo_total = ceil(tiempo_total_min / 60);

    % Calcular monto total
    if tiempo_total > 1
        monto_total = 15 + (tiempo_total - 1) * 20;
    else
        monto_total = 15;
    end
end

% Función para guardar la factura en el archivo de texto
function generar_factura_txt(nombre_cliente, id_vehiculo, tiempo_total, monto_total)
  try
    ruta_archivo = "facturas.txt";
    fid = fopen(ruta_archivo, "a");
    if fid == -1
      error("No se pudo abrir el archivo.");
    end
    
    fprintf(fid, "Nombre del cliente: %s\n", nombre_cliente);
    fprintf(fid, "Identificación del vehículo: %s\n", id_vehiculo);
    fprintf(fid, "Tiempo en el parqueo: %d horas\n", tiempo_total);
    fprintf(fid, "Monto total a pagar: Q%.2f\n", monto_total);
    fprintf(fid, "-----------------------------------------\n");

    fclose(fid);
    printf("¡Factura guardada en 'facturas.txt' con éxito!\n");
  catch
    printf("Error al escribir en el archivo 'facturas.txt'.\n");
  end
end

% Función para guardar la información en un archivo de texto
function guardar_en_salida_txt(nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida)
  try
    ruta_archivo = "salida.txt";
    fid = fopen(ruta_archivo, "a");
    if fid == -1
      error("No se pudo abrir el archivo.");
    end
    
    fprintf(fid, "Nombre del cliente: %s\n", nombre_cliente);
    fprintf(fid, "NIT: %s\n", nit_cliente);
    fprintf(fid, "Vehículo: %s\n", id_vehiculo);
    fprintf(fid, "Fecha: %s\n", fecha);
    fprintf(fid, "Hora Entrada: %s\n", hora_entrada);
    fprintf(fid, "Hora Salida: %s\n", hora_salida);
    fprintf(fid, "-----------------------------------------\n");

    fclose(fid);
    printf("¡Información guardada en 'salida.txt' con éxito!\n");
  catch
    printf("Error al escribir en el archivo 'salida.txt'.\n");
  end
end

% Función para validar que la entrada sea numérica
function valor = validar_entrada_numerica(mensaje)
  while true
    try
      valor = input(mensaje);
      if isnumeric(valor) && isscalar(valor) && valor > 0
        break;
      else
        printf("Entrada no válida. Debes ingresar un número positivo.\n");
      end
    catch
      printf("Entrada no válida. Debes ingresar un número.\n");
    end
  end
end

% Función para mostrar el historial desde la base de datos
function mostrar_historial_postgres(conn)
  query = "SELECT * FROM salida;";
  try
    result = pq_exec_params(conn, query, {});  % Ejecutar la consulta sin parámetros
    if isempty(result.data)
      printf("No hay registros en la base de datos aún.\n");
    else
      printf("\nHistorial de Parqueos (Base de Datos):\n");
      for i = 1:rows(result.data)
        printf("Registro %d:\n", i);
        printf("Nombre del cliente: %s\n", result.data{i, 1});
        printf("NIT: %s\n", result.data{i, 2});
        printf("Vehículo: %s\n", result.data{i, 3});
        printf("Fecha: %s\n", result.data{i, 4});
        printf("Hora Entrada: %s\n", result.data{i, 5});
        printf("Hora Salida: %s\n\n", result.data{i, 6});
      end
    end
  catch err
    error("Error ejecutando la consulta SQL: %s", err.message);
  end
end

% Función para mostrar el historial desde el archivo de texto
function mostrar_historial_facturas()
  try
    ruta_archivo = "facturas.txt";
    fid = fopen(ruta_archivo, "r");
    if fid == -1
      error("No se pudo abrir el archivo.");
    end
    
    printf("\nHistorial de Facturas (Archivo de Texto):\n");
    while ~feof(fid)
      linea = fgetl(fid);
      if ischar(linea)
        printf("%s\n", linea);
      end
    end

    fclose(fid);
  catch
    printf("Error al leer el archivo 'facturas.txt'.\n");
  end
end

% Función para borrar el historial en la base de datos
function borrar_historial_postgres(conn)
  confirmacion = input("¿Estás seguro de que deseas borrar todos los registros? (s/n): ", "s");
  if lower(confirmacion) == 's'
    query = "DELETE FROM salida;";
    try
      pq_exec_params(conn, query, {});  % Ejecutar la consulta sin parámetros
      printf("Historial borrado con éxito.\n");
    catch err
      error("Error ejecutando la consulta SQL: %s", err.message);
    end
  else
    printf("Borrado cancelado.\n");
  end
end

% Función para borrar el historial de facturas del archivo de texto
function borrar_historial_facturas()
  confirmacion = input("¿Estás seguro de que deseas borrar todas las facturas? (s/n): ", "s");
  if lower(confirmacion) == 's'
    ruta_archivo = "facturas.txt";
    fid = fopen(ruta_archivo, "w");
    if fid == -1
      printf("No se pudo abrir el archivo.\n");
    else
      fclose(fid);
      printf("Historial de facturas borrado con éxito.\n");
    end
  else
    printf("Borrado cancelado.\n");
  end
end

% Función principal con menú
function main()
  conn = connect_to_db();  % Conectar a la base de datos PostgreSQL
  while true
    clc;  % Limpiar la pantalla
    printf("\nSistema de Gestión de Parqueo\n");
    printf("1. Registrar transacción\n");
    printf("2. Ver historial\n");
    printf("3. Borrar historial\n");
    printf("4. Salir\n");

    opcion = validar_entrada_numerica("Selecciona una opción: ");

    switch opcion
      case 1
        % Registrar transacción
        nombre_cliente = input("Por favor, ingresa el nombre del cliente: ", "s");
        nit_cliente = input("Ingresa el NIT del cliente: ", "s");
        fecha = solicitar_fecha();
        id_vehiculo = input("Ingresa la identificación del vehículo (número de placa): ", "s");
         hora_entrada = ingresar_hora("Ingresa la hora de entrada (HHMM): ");
        hora_salida = ingresar_hora("Ingresa la hora de salida (HHMM): ");
        
        % Calcular tiempo total y monto a pagar
        [tiempo_total, monto_total] = calcular_monto(hora_entrada, hora_salida);

        % Mostrar el monto total en la terminal
        printf("Monto total a pagar: Q%.2f\n", monto_total);

        % Guardar la información en la base de datos
        guardar_info_db(conn, nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida);

        % Guardar la información en el archivo salida.txt
        guardar_en_salida_txt(nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida);

        % Generar factura en facturas.txt
        generar_factura_txt(nombre_cliente, id_vehiculo, tiempo_total, monto_total);

        printf("Transacción registrada con éxito.\n");
        pause(2);

      case 2
        % Ver historial
        while true
          clc;
          printf("\nVer Historial\n");
          printf("1. Ver historial de registros\n");
          printf("2. Ver historial de facturas\n");
          printf("3. Regresar al menú principal\n");

          sub_opcion = validar_entrada_numerica("Selecciona una opción: ");

          switch sub_opcion
            case 1
              mostrar_historial_postgres(conn);
              pause;
            case 2
              mostrar_historial_facturas();
              pause;
            case 3
              break;
            otherwise
              printf("Opción no válida. Por favor, selecciona una opción correcta.\n");
              pause(2);
          end

          if sub_opcion == 3
            break;
          end
        end

      case 3
        % Borrar historial
        while true
          clc;
          printf("\nBorrar Historial\n");
          printf("1. Borrar historial de registros\n");
          printf("2. Borrar historial de facturas\n");
          printf("3. Regresar al menú principal\n");

          sub_opcion = validar_entrada_numerica("Selecciona una opción: ");

          switch sub_opcion
            case 1
              borrar_historial_postgres(conn);
              pause;
            case 2
              borrar_historial_facturas();
              pause;
            case 3
              break;
            otherwise
              printf("Opción no válida. Por favor, selecciona una opción correcta.\n");
              pause(2);
          end

          if sub_opcion == 3
            break;
          end
        end

      case 4
        % Salir del programa
        printf("Saliendo del programa. ¡Hasta pronto!\n");
        pq_close(conn);  % Cerrar la conexión a la base de datos
        break;

      otherwise
        % Manejar opción no válida
        printf("Opción no válida. Por favor, selecciona una opción correcta.\n");
        pause(2);
    end

    if opcion == 4
      break;  % Salir del bucle si la opción es 4
    end
  end
end

% Ejecutar la función principal
main();