# Generated by Django 4.2.5 on 2023-09-14 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='unit',
            field=models.CharField(max_length=17, verbose_name='Единица измерения'),
        ),
    ]
