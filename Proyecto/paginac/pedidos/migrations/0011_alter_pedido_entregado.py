# Generated by Django 4.1.1 on 2022-10-09 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0010_pedido_entregado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='entregado',
            field=models.BooleanField(),
        ),
    ]
