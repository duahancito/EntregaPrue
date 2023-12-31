# Generated by Django 3.1.2 on 2023-06-28 17:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20230625_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compra',
            name='estado',
            field=models.CharField(choices=[('Validacion', 'Validacion'), ('Preparacion', 'Preparacion'), ('Reparto', 'Reparto'), ('Entregado', 'Entregado')], default='validacion', max_length=20),
        ),
        migrations.AddField(
            model_name='compra',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
