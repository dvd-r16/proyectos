# Generated by Django 5.1.1 on 2024-10-25 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0019_reserva_completada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulos',
            name='banner_image',
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='estudiantes',
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='horario',
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='imagen_certificado',
        ),
        migrations.RemoveField(
            model_name='articulos',
            name='welcome_message',
        ),
    ]