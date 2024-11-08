pkg load database;  # Cargar el paquete necesario para trabajar con bases de datos

function conn = conectar_db()
    try
        conn = pq_connect(setdbopts('dbname', 'detect', 'host', 'localhost', 'port', '5432', 'user', 'postgres', 'password', 'Dali6478'));
    catch
        disp("Error al conectar a la base de datos");
        return;
    end
end

% Función para almacenar en el archivo .txt
function save_to_history(data)
    fid = fopen("history.txt", "a");
    fprintf(fid, "%s\n", data);
    fclose(fid);
endfunction

% Función para verificar si una palabra es palíndroma
function result = is_palindrome(sentence)
    normalized = lower(strrep(sentence, ' ', ''));
    normalized = unideblank(normalized);  % Elimina tildes
    result = strcmp(normalized, fliplr(normalized));  % Compara si es igual al reverso
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
function detector_menu()
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
            query = sprintf("INSERT INTO detect (palindromos, resultado) VALUES ('%s', '%s')", sentence, result_str);

            message = sprintf("La oración %s es palíndroma", result_str);
            printf("%s\n", message);
            save_to_history(sprintf("%s - Palíndromo: %s - Resultado: %s", datestr(now, 'yyyy-mm-dd HH:MM:SS'), sentence, result_str));

        elseif option == '2'
            number = input("Ingresa un número: ");
            if !isnumeric(number)
                printf("Error: Solo se permiten números.\n");
                continue;
            endif
            result = is_prime(number);
            result_str = 'NO';
            if result
                result_str = 'SI';
            endif
            query = sprintf("INSERT INTO detect (numero, resultado) VALUES (%d, '%s')", number, result_str);

            message = sprintf("El número %s es primo", result_str);
            printf("%s\n", message);
            save_to_history(sprintf("%s - Número primo: %d - Resultado: %s", datestr(now, 'yyyy-mm-dd HH:MM:SS'), number, result_str));

        elseif option == '3'
            number = input("Ingresa un número: ");
            if !isnumeric(number)
                printf("Error: Solo se permiten números.\n");
                continue;
            endif
            result = is_perfect(number);
            result_str = 'NO';
            if result
                result_str = 'SI';
            endif
            query = sprintf("INSERT INTO detect (numero, resultado) VALUES (%d, '%s')", number, result_str);
            pq_exec(conn, query);
            message = sprintf("El número %s es perfecto", result_str);
            printf("%s\n", message);
            save_to_history(sprintf("%s - Número perfecto: %d - Resultado: %s", datestr(now, 'yyyy-mm-dd HH:MM:SS'), number, result_str));

        else
            printf("Opción inválida. Inténtalo de nuevo.\n");
            continue;
        endif

        again = input("¿Deseas realizar otra operación? (s/n): ", "s");
        if again == 's'
            return;  % Si el usuario elige 's', reiniciar el programa
        elseif again == 'n'

            printf("Saliendo del programa...\n");
            return;  % Detener el programa
        endif
    endwhile
endfunction

% Menú principal
function main_menu()
    while true
        user = input("Ingresa tu nombre de usuario: ", "s");
        query = sprintf("INSERT INTO detect (usuario) VALUES ('%s')", user);


        while true
            printf("\n1) Detector\n2) Historial de datos ingresados\n3) Borrar datos\n4) Salir\n");
            option = input("Selecciona una opción: ", "s");

            if option == '1'
                detector_menu();
            elseif option == '2'
                result = pq_exec(conn, "SELECT * FROM detect");
                disp(result);
            elseif option == '3'
                user_to_delete = input("Ingresa el nombre de usuario cuyos datos deseas borrar: ", "s");
                query = sprintf("DELETE FROM detect WHERE usuario = '%s'", user_to_delete);

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


