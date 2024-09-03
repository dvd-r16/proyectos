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

% Función para guardar la información en la base de datos
function guardar_info_db(conn, nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida)
  query = "INSERT INTO salida (nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida) VALUES ($1, $2, $3, $4, $5, $6);";
  valores = {nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida};
  
  try
    pq_exec_params(conn, query, valores);  % Ejecutar la consulta con parámetros
    printf("¡Información registrada en la base de datos!\n");
  catch err
    error("Error ejecutando la consulta SQL: %s", err.message);
  end
end

% Función para generar la factura en el archivo de texto
function success = generar_factura_txt(nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida)
  try
    ruta_archivo = "salida.txt";
    fid = fopen(ruta_archivo, "a");
    if fid == -1
      error("No se pudo abrir el archivo.");
    end
    
    fprintf(fid, "Cliente: %s, NIT: %s, Vehículo: %s, Fecha: %s, Hora Entrada: %s, Hora Salida: %s\n", ...
            nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida);
    fprintf(fid, "-----------------------------------------\n");

    fclose(fid);
    printf("¡Información guardada en 'salida.txt' con éxito!\n");
    success = true;
  catch
    printf("Error al escribir en el archivo 'salida.txt'.\n");
    success = false;
  end
end

% Función para validar que la entrada sea numérica
function valor = validar_entrada_numerica(mensaje)
  while true
    valor = input(mensaje);
    if isnumeric(valor) && isscalar(valor)
      break;
    else
      printf("Entrada no válida. Debes ingresar un número.\n");
    end
  end
end

% Función para mostrar el historial desde la base de datos
function mostrar_historial(conn)
  query = "SELECT * FROM salida;";
  try
    result = pq_exec_params(conn, query, {});  % Ejecutar la consulta sin parámetros
    if isempty(result.data)
      printf("No hay registros en la base de datos aún.\n");
    else
      printf("\nHistorial de Parqueos:\n");
      for i = 1:rows(result.data)
        printf("Registro %d:\n", i);
        printf("Nombre del cliente: %s\n", result.data{i, 1});
        printf("NIT: %s\n", result.data{i, 2});
        printf("Vehículo: %s\n", result.data{i, 3});
        printf("Fecha: %s\n", datestr(result.data{i, 4}, 'dd-mm-yyyy'));
        printf("Hora Entrada: %s\n", result.data{i, 5});
        printf("Hora Salida: %s\n\n", result.data{i, 6});
      end
    end
  catch err
    error("Error ejecutando la consulta SQL: %s", err.message);
  end
end

% Función para borrar el historial en la base de datos
function borrar_historial(conn)
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

% Función principal con menú
function main()
  conn = connect_to_db();  % Conectar a la base de datos PostgreSQL
  while true
    clc;  % Limpiar la pantalla
    printf("\nSistema de Gestión de Parqueo\n");
    printf("1. Registrar transacción\n");
    printf("2. Ver historial de registros\n");
    printf("3. Borrar historial de registros\n");
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
        guardar_info_db(conn, nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida);
        if ~generar_factura_txt(nombre_cliente, nit_cliente, id_vehiculo, fecha, hora_entrada, hora_salida)
          error("Error al escribir en el archivo 'salida.txt'. Programa terminado.");
        end
        printf("Transacción registrada con éxito.\n");
        pause(2);

      case 2
        % Ver historial de registros
        mostrar_historial(conn);
        printf("\nPresiona Enter para regresar al menú principal...\n");
        pause;

      case 3
        % Borrar historial de registros
        borrar_historial(conn);
        pause(2);

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
