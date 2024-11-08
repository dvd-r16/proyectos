pkg load database;  % Cargar el paquete necesario para trabajar con bases de datos

function conn = conectar_db()
    try
        conn = pq_connect(setdbopts("dbname", "detector", "host", "localhost", "port", "5432", "user", "postgres", "password", "202010039"));
        disp("Conexión a la base de datos establecida exitosamente.");
    catch
        disp("Error al conectar a la base de datos.");
        conn = []; % Retornar una conexión vacía en caso de error
    end
end

% Función para agregar el delimitador solo en la base de datos
function add_delimiter(conn, user)
    % Agregar delimitador en la base de datos con el formato completo del usuario
    user_with_octave = strcat(user, " - Octave");
    query = sprintf("INSERT INTO detector (usuario, palindromos, resultado) VALUES ('%s', '////////////', '////////////')", user_with_octave);
    pq_exec_params(conn, query, {});
endfunction

% Función para almacenar en el archivo .txt
function save_to_history(data)
    fid = fopen("history.txt", "a");
    fprintf(fid, "%s\n", data);
    fclose(fid);
endfunction

% Función para verificar si una palabra es palíndroma
function result = is_palindrome(sentence)
    % Normalizar la oración: eliminar espacios, convertir a minúsculas y reemplazar caracteres acentuados
    sentence = lower(sentence);
    sentence = regexprep(sentence, '[^a-z]', '');  % Eliminar todo excepto letras de la a a la z
    sentence = strrep(sentence, 'á', 'a');
    sentence = strrep(sentence, 'é', 'e');
    sentence = strrep(sentence, 'í', 'i');
    sentence = strrep(sentence, 'ó', 'o');
    sentence = strrep(sentence, 'ú', 'u');
    sentence = strrep(sentence, 'ñ', 'n');
    
    % Comparar si es igual al reverso
    result = strcmp(sentence, fliplr(sentence));
endfunction

% Función para verificar si un número es primo
function result = is_prime(number)
    if number <= 1
        result = false;
    else
        result = true;
        for i = 2:sqrt(number)
            if mod(number, i) == 0
                result = false;
                break;
            end
        end
    end
endfunction

% Función para verificar si un número es perfecto
function result = is_perfect(number)
    if number <= 1
        result = false;
    else
        sum_divisors = sum(find(mod(number, 1:number-1) == 0));
        result = sum_divisors == number;
    end
endfunction

% Función principal del menú del detector
function detector_menu(conn, user)
    user = strcat(user, " - Octave");  % Agregar el identificador "- Octave" al usuario
    while true
        printf("\n1) Detector de palíndromos\n2) Detector de números primos\n3) Detector de números perfectos\n");
        option = input("Selecciona una opción: ", "s");

        if option == '1'
            sentence = input("Ingresa una oración: ", "s");
            if isempty(regexp(sentence, '[a-zA-Z]', 'once'))
                printf("Error: Solo se permiten letras en la oración.\n");
                continue;
            endif
            result = is_palindrome(sentence);
            result_str = 'NO';
            if result
                result_str = 'SI';
            endif
            query = sprintf("INSERT INTO detector (usuario, palindromos, resultado) VALUES ('%s', '%s', '%s')", user, sentence, result_str);
            pq_exec_params(conn, query, {});

            message = sprintf("La oración %s es palíndroma", result_str);
            printf("%s\n", message);
            save_to_history(sprintf("%s - Usuario: %s - Palíndromo: %s - Resultado: %s", datestr(now, 'yyyy-mm-dd HH:MM:SS'), user, sentence, result_str));

        elseif option == '2'
            number = input("Ingresa un número: ");
            if !isnumeric(number)
                printf("Error: Solo se permiten números.\n");
                continue;
            endif
            result = is_prime(number);
            if result
                result_str = 'SI ES PRIMO';
            else
                result_str = 'NO ES PRIMO';
            endif
            query = sprintf("INSERT INTO detector (usuario, numero, resultado) VALUES ('%s', %d, '%s')", user, number, result_str);
            pq_exec_params(conn, query, {});

            message = sprintf("El número %s", result_str);
            printf("%s\n", message);
            save_to_history(sprintf("%s - Usuario: %s - Número primo: %d - Resultado: %s", datestr(now, 'yyyy-mm-dd HH:MM:SS'), user, number, result_str));

        elseif option == '3'
            number = input("Ingresa un número: ");
            if !isnumeric(number)
                printf("Error: Solo se permiten números.\n");
                continue;
            endif
            result = is_perfect(number);
            if result
                result_str = 'SI ES PERFECTO';
            else
                result_str = 'NO ES PERFECTO';
            endif
            query = sprintf("INSERT INTO detector (usuario, numero, resultado) VALUES ('%s', %d, '%s')", user, number, result_str);
            pq_exec_params(conn, query, {});

            message = sprintf("El número %s", result_str);
            printf("%s\n", message);
            save_to_history(sprintf("%s - Usuario: %s - Número perfecto: %d - Resultado: %s", datestr(now, 'yyyy-mm-dd HH:MM:SS'), user, number, result_str));

        else
            printf("Opción inválida. Inténtalo de nuevo.\n");
            continue;
        endif

        again = input("¿Deseas realizar otra operación? (s/n): ", "s");
        if strcmp(again, 'n')
            printf("Saliendo del programa...\n");
            return;  % Detener el programa
        endif
    endwhile
endfunction

% Menú principal
function main_menu()
    conn = conectar_db();  % Conectar a la base de datos al inicio

    while true
        user = input("Ingresa tu nombre de usuario: ", "s");
        % Verificar si el usuario ingresó un nombre en blanco
        while isempty(user)
            printf("Debe ingresar un nombre de usuario válido.\n");
            user = input("Ingresa tu nombre de usuario: ", "s");
        endwhile

        % Agregar delimitador para el nuevo usuario solo en la base de datos con formato "usuario - Octave"
        add_delimiter(conn, user);

        % Continuar con el usuario en formato "usuario - Octave" en todas las consultas
        user_octave = strcat(user, " - Octave");

        while true
            printf("\n1) Detector\n2) Historial de datos ingresados\n3) Borrar datos\n4) Salir\n");
            option = input("Selecciona una opción: ", "s");

            if option == '1'
                detector_menu(conn, user);
            elseif option == '2'
                result = pq_exec_params(conn, "SELECT * FROM detector WHERE usuario = $1", {user_octave});
                disp(result);
            elseif option == '3'
                user_to_delete = input("Ingresa el nombre de usuario cuyos datos deseas borrar: ", "s");
                user_to_delete = strcat(user_to_delete, " - Octave");  % Agregar "- Octave" al nombre del usuario al borrar
                query = sprintf("DELETE FROM detector WHERE usuario = '%s'", user_to_delete);
                pq_exec_params(conn, query, {});
                printf("Datos de %s eliminados.\n", user_to_delete);
            elseif option == '4'
                pq_close(conn);  % Cerrar la conexión
                printf("Saliendo del programa...\n");
                return;  % Detener el programa
            else
                printf("Opción inválida. Inténtalo de nuevo.\n");
            endif
        endwhile
    endwhile
endfunction

% Ejecución del programa
main_menu();
