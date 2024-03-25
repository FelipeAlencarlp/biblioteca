# Generated by Django 5.0.3 on 2024-03-25 21:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0019_alter_emprestimos_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimos',
            name='data_emprestimo',
            field=models.DateField(default=datetime.datetime(2024, 3, 25, 18, 4, 2, 80878)),
        ),
        migrations.AlterField(
            model_name='livros',
            name='emprestado',
            field=models.BooleanField(default=False),
        ),
    ]
