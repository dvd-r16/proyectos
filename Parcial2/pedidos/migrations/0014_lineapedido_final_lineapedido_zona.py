# Generated by Django 5.1.1 on 2024-10-06 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0013_alter_pedido_entregado'),
    ]

    operations = [
        migrations.AddField(
            model_name='lineapedido',
            name='final',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lineapedido',
            name='zona',
            field=models.IntegerField(default=0),
        ),
    ]
