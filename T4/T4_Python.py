import tkinter as tk
from tkinter import messagebox, simpledialog
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read
from scipy.signal import welch, get_window
import matplotlib.pyplot as plt
import os

# Variables globales
file_name = "audio_py.wav"

# Función para grabar audio
def grabar_audio():
    try:
        # Ventana emergente solicitando duración de la grabación
        duracion = simpledialog.askinteger("Duración de Grabación", "Ingrese la duración de la grabación en segundos:")
        
        if duracion is None:  # Si el usuario cierra la ventana o cancela
            return
        
        messagebox.showinfo("Grabación", "Comenzando la grabación...")
        fs = 44100  # Frecuencia de muestreo
        audio = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype='float64')
        sd.wait()  # Espera hasta que la grabación esté completa
        write(file_name, fs, audio)  # Guarda el archivo WAV
        messagebox.showinfo("Grabación", "Grabación finalizada y guardada.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al grabar el audio: {e}")

# Función para reproducir audio
def reproducir_audio():
    try:
        if not os.path.exists(file_name):
            raise FileNotFoundError("El archivo de audio no existe")
        
        fs, data = read(file_name)
        sd.play(data, fs)
        sd.wait()  # Espera a que termine la reproducción
    except Exception as e:
        messagebox.showerror("Error", f"Error al reproducir el audio: {e}")

# Función para graficar audio
def graficar_audio():
    try:
        if not os.path.exists(file_name):
            raise FileNotFoundError("El archivo de audio no existe")
        
        fs, data = read(file_name)
        tiempo = np.linspace(0, len(data) / fs, len(data))
        plt.figure()
        plt.plot(tiempo, data)
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Amplitud')
        plt.title('Gráfico de Audio')
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error al graficar el audio: {e}")

# Función para graficar densidad espectral de potencia
def graficar_densidad():
    try:
        if not os.path.exists(file_name):
            raise FileNotFoundError("El archivo de audio no existe")

        fs, audio = read(file_name)
        
        # Asegurarse de que el audio esté en formato 1D si es mono
        if len(audio.shape) > 1:  # Si el audio tiene múltiples canales (estéreo)
            audio = audio[:, 0]  # Selecciona el primer canal
        
        N = len(audio)
        ventana = get_window('hann', N)
        f, Pxx = welch(audio, fs, window=ventana, nperseg=N, scaling='density')
        
        plt.figure()
        plt.semilogy(f, Pxx)
        plt.xlabel('Frecuencia (Hz)')
        plt.ylabel('Densidad espectral de potencia (dB/Hz)')
        plt.title('Espectro de Frecuencia de la Señal Grabada')
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error al graficar la densidad espectral: {e}")

# Crear la ventana de tkinter
root = tk.Tk()
root.title("Grabador de Audio")

# Botones del menú
grabar_btn = tk.Button(root, text="Grabar Audio", command=grabar_audio)
grabar_btn.grid(row=1, column=0, padx=10, pady=10)

reproducir_btn = tk.Button(root, text="Reproducir Audio", command=reproducir_audio)
reproducir_btn.grid(row=1, column=1, padx=10, pady=10)

graficar_btn = tk.Button(root, text="Graficar Audio", command=graficar_audio)
graficar_btn.grid(row=2, column=0, padx=10, pady=10)

densidad_btn = tk.Button(root, text="Graficar Densidad Espectral", command=graficar_densidad)
densidad_btn.grid(row=2, column=1, padx=10, pady=10)

salir_btn = tk.Button(root, text="Salir", command=root.quit)
salir_btn.grid(row=3, column=0, columnspan=2, pady=20)

# Iniciar la ventana
root.mainloop()