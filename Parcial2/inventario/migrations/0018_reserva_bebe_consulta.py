# Generated by Django 5.1.1 on 2024-10-13 17:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0017_reserva_archivo_reserva_notas_profesor'),
        ('usuarios', '0022_alter_profesor_options_alter_usuarios_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='bebe_consulta',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.bebeconsulta'),
        ),
    ]
