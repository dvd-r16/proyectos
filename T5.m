# Definición de las categorías
bajoPeso = "Bajo peso";
pesoNormal = "Peso normal";
sobrePeso = "Sobrepeso";

# Función principal
function main()
  while true
    # Mostrar opciones
    MostrarOpciones();
    
    # Leer la opción del usuario
    opcion = input('Ingrese la opción deseada: ');
    
    # Validar la opción
    if ~(1 <= opcion && opcion <= 4)
      disp('Opción no válida. Intente de nuevo.');
      continue;
    endif
    
    # Ejecutar la acción según la opción
    switch opcion
      case 1
        # Calcular IMC y Mostrar resultados
        CalcularYMostrarIMC();
        
      case 2
        # Leer información del archivo
        LeerInformacion();
        
      case 3
        # Borrar información del archivo
        BorrarInformacion();
        
      case 4
        # Salir del programa
        break;
    endswitch
  endwhile
  
  # Mensaje de despedida
  disp('Gracias por usar el programa!');
endfunction

# Función para mostrar las opciones disponibles al usuario
function MostrarOpciones()
  disp('Opciones:');
  disp('1. Calcular IMC');
  disp('2. Leer información del archivo');
  disp('3. Borrar información del archivo');
  disp('4. Salir');
endfunction

# Función para calcular el IMC y mostrar resultados
function CalcularYMostrarIMC()
  nombre = input('Ingrese su nombre: ', 's');
  peso = input('Ingrese su peso en kilogramos: ');
  altura = input('Ingrese su altura en metros: ');

  # Calcular IMC
  imc = peso / (altura ^ 2);
  fprintf('Su IMC es: %.2f\n', imc);

  # Determinar la categoría del IMC
  if imc < 18.5
    categoria = "Bajo peso";
  elseif imc >= 18.5 && imc <= 24.9
    categoria = "Peso normal";
  else
    categoria = "Sobrepeso";
  endif
  fprintf('Categoría del IMC: %s\n', categoria);

  # Guardar la información en un archivo si el usuario lo desea
  guardar = input('¿Desea guardar la información en un archivo? (s/n): ', 's');
  if guardar == 's'
    archivo = fopen('imc.txt', 'a');
    fprintf(archivo, 'Nombre: %s, Peso: %.2f kg, Altura: %.2f m, IMC: %.2f, Categoría: %s\n', nombre, peso, altura, imc, categoria);
    fclose(archivo);
    disp('Información guardada exitosamente.');
  endif
endfunction

# Función para leer la información del archivo
function LeerInformacion()
  if exist('imc.txt', 'file')
    archivo = fopen('imc.txt', 'r');
    while ~feof(archivo)
      linea = fgetl(archivo);
      if ischar(linea)
        disp(linea);
      endif
    endwhile
    fclose(archivo);
  else
    disp('El archivo "imc.txt" no existe.');
  endif
endfunction

# Función para borrar la información del archivo
function BorrarInformacion()
  if exist('imc.txt', 'file')
    delete('imc.txt');
    disp('Archivo "imc.txt" borrado exitosamente.');
  else
    disp('El archivo "imc.txt" no existe.');
  endif
endfunction

# Programa inicial
main();