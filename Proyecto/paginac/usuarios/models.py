from email.policy import default
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    cui = models.BigIntegerField()  # Cambia a BigIntegerField
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    login_attempts = models.BigIntegerField(default=0)
    birth_date = models.DateField(null=True, blank=True)  # Agrega este campo
    phone = models.CharField(max_length=20, null=True, blank=True)  # Agrega este campo

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'usuarios_info'
        verbose_name='Cliente'
        verbose_name_plural = 'Estudiantes'
        ordering=['id']

class Profesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dpi = models.CharField(max_length=13, unique=True)  # DPI único para identificación
    password = models.CharField(max_length=128)  # Contraseña encriptada
    password_confirmation = models.CharField(max_length=128)  # Confirmación de contraseña

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    class Meta:
        db_table = 'profesores_info'
        verbose_name = 'Catedrático'
        verbose_name_plural = 'Catedráticos'
        ordering = ['apellido', 'nombre']