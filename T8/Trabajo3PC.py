import psycopg2
import bcrypt
import cv2
import os

# Conexión a la base de datos
def conectar_bd():
    try:
        conexion = psycopg2.connect(
            dbname="nombre_de_tu_base_de_datos",
            user="tu_usuario",
            password="tu_contraseña",
            host="localhost",
            port="5432"
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Registro de un nuevo usuario
def registrar_usuario(nombre, apellido, dpi, fecha_nacimiento, telefono, nombre_usuario, email, contraseña, rol, reconocimiento_facial_model):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    # Hash de la contraseña
    hashed_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute("""
        INSERT INTO usuarios (nombre, apellido, dpi, fecha_nacimiento, telefono, nombre_usuario, email, contraseña, rol, reconocimiento_facial)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, dpi, fecha_nacimiento, telefono, nombre_usuario, email, hashed_contraseña, rol, reconocimiento_facial_model))
        
        conexion.commit()
        print("Usuario registrado con éxito")
    except Exception as e:
        print(f"Error al registrar el usuario: {e}")
    finally:
        cursor.close()
        conexion.close()

# Función de inicio de sesión
def iniciar_sesion(nombre_usuario, contraseña):
    conexion = conectar_bd()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("SELECT id, contraseña, rol FROM usuarios WHERE nombre_usuario = %s", (nombre_usuario,))
        usuario = cursor.fetchone()
        
        if usuario and bcrypt.checkpw(contraseña.encode('utf-8'), usuario[1].encode('utf-8')):
            print(f"Inicio de sesión exitoso. Rol: {usuario[2]}")
            # Redirigir según el rol
            if usuario[2] == 'administrador':
                vista_administracion()
            elif usuario[2] == 'catedrático':
                vista_catedratico()
            elif usuario[2] == 'alumno':
                vista_alumno()
        else:
            print("Nombre de usuario o contraseña incorrecta")
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
    finally:
        cursor.close()
        conexion.close()

# Funciones para diferentes vistas según el rol
def vista_administracion():
    print("Accediendo a la vista de administración")

def vista_catedratico():
    print("Accediendo a la vista de catedrático")

def vista_alumno():
    print("Accediendo a la vista de alumno")

# Reconocimiento facial para iniciar sesión
def reconocimiento_facial():
    dataPath = 'C:/Users/Lenovo/Documents/Proyectos DavidR/Reconocimiento Facial/Data'
    imagePaths = os.listdir(dataPath)
    print('imagePaths=', imagePaths)
    
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('modeloLBPHFace.xml')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()
        faces = faceClassif.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)
            cv2.putText(frame, '{}'.format(result), (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            
            if result[1] < 5700:
                cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print(f"Usuario reconocido: {imagePaths[result[0]]}")
                return True  # Inicia sesión con éxito
            else:
                cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:  # Presiona 'Esc' para salir
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return False

# Función para intentar iniciar sesión con reconocimiento facial
def intentar_inicio_sesion_por_reconocimiento_facial():
    if reconocimiento_facial():
        print("Reconocimiento facial exitoso, redirigiendo a la vista de usuario.")
        # Aquí puedes redirigir al usuario según su rol.
    else:
        print("No se pudo reconocer el rostro.")
