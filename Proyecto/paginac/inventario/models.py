from tabnanny import verbose
from django.db import models
from usuarios.models import Profesor
from django.contrib.auth.models import User  # Para relacionar con catedráticos

class articulos(models.Model):
    nombre = models.CharField(max_length=30, null=False)
    categoria = models.CharField(max_length=30, null=False)
    precio = models.FloatField(null=False)
    horario = models.CharField(max_length=100)
    descuento = models.FloatField(null=False)
    descripcion = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='servicios')
    cantidad = models.IntegerField(null=False, default= 0)
    catedratico = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    estudiantes = models.ManyToManyField(User, related_name='cursos_inscritos', blank=True)  # Relación con los estudiantes
    disponibilidad = models.BooleanField()
    creacion = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)

    #Para las paginas de cada curso
    banner_image = models.ImageField(upload_to='banners', null=True, blank=True)
    welcome_message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name= 'articulo'

    def __str__(self):
        return self.nombre
    
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)  # Relación con el profesor
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre
    

class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


class Nota(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  # Relación con Curso
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)  # Relación con Estudiante
    valor = models.DecimalField(max_digits=5, decimal_places=2)  # Ejemplo de valor de nota, hasta 100.00

    def __str__(self):
        return f'{self.estudiante} - {self.curso} - {self.valor}'

# class clientes(models.Model):
#     nombre = models.CharField(max_length=50)
#     apellido = models.CharField(max_length=50)
#     dpi = models.IntegerField()
#     telefono = models.IntegerField()
#     direccion = models.CharField(max_length=150)