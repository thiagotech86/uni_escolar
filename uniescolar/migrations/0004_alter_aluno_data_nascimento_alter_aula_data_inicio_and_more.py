# Generated by Django 5.2 on 2025-04-16 22:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uniescolar', '0003_responsavel_alter_aula_disciplina_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='data_nascimento',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
        migrations.AlterField(
            model_name='aula',
            name='data_inicio',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='aula',
            name='hora_fim',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
        migrations.AlterField(
            model_name='aula',
            name='hora_inicio',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
    ]
