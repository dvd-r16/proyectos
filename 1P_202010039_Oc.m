pkg load database;

% Función para conectarse a la base de datos PostgreSQL
function conn = connect_to_db()
  conn = pq_connect(setdbopts("dbname", "postgres", "host", "localhost", "port", "5432", "user", "postgres", "password", "202010039"));
end

% Función para seleccionar el tipo de combustible
function tipo_combustible = seleccionar_combustible()
  printf("\nSelecciona el tipo de combustible:\n");
  printf("1. Gasolina Regular\n");
  printf("2. Gasolina Súper\n");
  printf("3. Diesel\n");
  printf("4. Vpower\n");

  opcion = validar_entrada_numerica("Selecciona una opción: ");

  switch opcion
    case 1
      tipo_combustible = "Gasolina Regular";
    case 2
      tipo_combustible = "Gasolina Súper";
    case 3
      tipo_combustible = "Diesel";
    case 4
      tipo_combustible = "Vpower";
    otherwise
      printf("Opción no válida. Selecciona una opción válida.\n");
      tipo_combustible = seleccionar_combustible();  % Volver a preguntar
  end
end

% Función para ingresar la cantidad de litros con validación de entrada numérica
function cantidad_litros = ingresar_litros()
  cantidad_litros = validar_entrada_numerica("Ingresa la cantidad de litros a despachar: ");
  if cantidad_litros <= 0
    printf("La cantidad de litros debe ser un número positivo. Intenta de nuevo.\n");
    cantidad_litros = ingresar_litros();  % Volver a preguntar
  end
end

% Función para obtener el precio por litro según el tipo de combustible
function precio_por_litro = obtener_precio_combustible(tipo_combustible)
  switch tipo_combustible
    case "Gasolina Regular"
      precio_por_litro = 3.50;
    case "Gasolina Súper"
      precio_por_litro = 4.00;
    case "Diesel"
      precio_por_litro = 3.00;
    case "Vpower"
      precio_por_litro = 4.50;
    otherwise
      precio_por_litro = 0;  % En caso de error
  end
end

% Función para calcular el monto total a pagar
function monto_total = calcular_monto(cantidad_litros, precio_por_litro)
  monto_total = cantidad_litros * precio_por_litro;
end

% Función para mostrar el resumen de la transacción
function mostrar_resumen(nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total)
  printf("\nResumen de la Transacción:\n");
  printf("Nombre del cliente: %s\n", nombre_cliente);
  printf("Identificación del vehículo: %s\n", identificacion_vehiculo);
  printf("Tipo de combustible: %s\n", tipo_combustible);
  printf("Cantidad de litros: %.2f\n", cantidad_litros);
  printf("Precio por litro: Q. %.2f\n", precio_por_litro);
  printf("Monto total a pagar: Q. %.2f\n", monto_total);
end

% Función para guardar la factura en la base de datos
function guardar_factura(conn, nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total)
  query = "INSERT INTO facturas (nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total) VALUES ($1, $2, $3, $4, $5, $6);";
  
  valores = {nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total};
  
  try
    pq_exec_params(conn, query, valores);  % Ejecutar la consulta con parámetros
    printf("¡Factura registrada en la base de datos!\n");
  catch err
    error("Error ejecutando la consulta SQL: %s", err.message);
  end
end

% Función para generar la factura en el archivo de texto
function success = generar_factura_txt(nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total)
  try
    fid = fopen("facturas.txt", "a");
    if fid == -1
      error("No se pudo abrir el archivo.");
    end
    
    fprintf(fid, "Nombre del cliente: %s\n", nombre_cliente);
    fprintf(fid, "Identificación del vehículo: %s\n", identificacion_vehiculo);
    fprintf(fid, "Tipo de combustible: %s\n", tipo_combustible);
    fprintf(fid, "Cantidad de litros: %.2f\n", cantidad_litros);
    fprintf(fid, "Precio por litro: Q. %.2f\n", precio_por_litro);
    fprintf(fid, "Monto total a pagar: Q. %.2f\n", monto_total);
    fprintf(fid, "-----------------------------------------\n");

    fclose(fid);
    printf("¡Factura guardada en 'facturas.txt' con éxito!\n");
    success = true;
  catch
    printf("Error al escribir en el archivo 'facturas.txt'.\n");
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


% Función para ver el historial de facturas desde la base de datos
% Función para ver el historial de facturas desde la base de datos
function ver_historial_facturas(conn)
  query = "SELECT * FROM facturas;";
  try
    result = pq_exec_params(conn, query, {});  % Ejecutar la consulta sin parámetros
    if isempty(result.data)
      printf("No hay facturas registradas aún.\n");
    else
      printf("\nHistorial de Facturas:\n");
      for i = 1:rows(result.data)
        printf("Factura %d:\n", i);
        printf("Nombre del cliente: %s\n", result.data{i, 1});
        printf("Identificación del vehículo: %s\n", result.data{i, 2});
        printf("Tipo de combustible: %s\n", result.data{i, 3});
        printf("Cantidad de litros: %.2f\n", result.data{i, 4});
        printf("Precio por litro: Q. %.2f\n", result.data{i, 5});
        printf("Monto total: Q. %.2f\n\n", result.data{i, 6});
      end
    end
  catch err
    error("Error ejecutando la consulta SQL: %s", err.message);
  end
end

% Función para borrar el historial de facturas en la base de datos
function borrar_historial_facturas(conn)
  confirmacion = input("¿Estás seguro de que deseas borrar todas las facturas? (s/n): ", "s");
  if lower(confirmacion) == 's'
    query = "DELETE FROM facturas;";
    try
      pq_exec_params(conn, query, {});  % Ejecutar la consulta sin parámetros
      printf("Historial de facturas borrado con éxito.\n");
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
    printf("\nSistema de Gestión de Combustible\n");
    printf("1. Registrar transacción\n");
    printf("2. Ver historial de facturas\n");
    printf("3. Borrar historial de facturas\n");
    printf("4. Salir\n");

    opcion = validar_entrada_numerica("Selecciona una opción: ");

    switch opcion
      case 1
        % Registrar transacción de combustible
        nombre_cliente = input("Por favor, ingresa el nombre del cliente: ", "s");
        identificacion_vehiculo = input("Ingresa la identificación del vehículo (número de placa): ", "s");
        tipo_combustible = seleccionar_combustible();
        cantidad_litros = ingresar_litros();
        precio_por_litro = obtener_precio_combustible(tipo_combustible);
        monto_total = calcular_monto(cantidad_litros, precio_por_litro);
        mostrar_resumen(nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total);
        guardar_factura(conn, nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total);
        if ~generar_factura_txt(nombre_cliente, identificacion_vehiculo, tipo_combustible, cantidad_litros, precio_por_litro, monto_total)
          error("Error al escribir en el archivo 'facturas.txt'. Programa terminado.");
        end
        printf("Transacción registrada con éxito.\n");
        pause(2);  % Pausar para que el usuario pueda ver el mensaje antes de volver al menú

      case 2
        % Ver historial de facturas
         ver_historial_facturas(conn);
        printf("\nPresiona Enter para regresar al menú principal...\n");
        pause;  % Espera a que el usuario presione Enter

      case 3
        % Borrar historial de facturas
        borrar_historial_facturas(conn);
        pause(2);  % Pausar para que el usuario pueda ver el mensaje de confirmación antes de volver al menú

      case 4
        % Salir del programa
        printf("Saliendo del programa. ¡Hasta pronto!\n");
        close(conn);  % Cerrar la conexión a la base de datos
        break;

      otherwise
        % Manejar opción no válida
        printf("Opción no válida. Por favor, selecciona una opción correcta.\n");
        pause(2);  % Pausar para que el usuario pueda leer el mensaje de error
    end

    if opcion == 4
      break;  % Salir del bucle si la opción es 4
    end
  end
end

% Ejecutar la función principal
main();