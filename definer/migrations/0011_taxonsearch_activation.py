# Generated by Django 3.1.1 on 2021-01-04 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0010_auto_20210104_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxonsearch',
            name='activation',
            field=models.CharField(blank=True, choices=[('Выбрать', 'Выбрать'), ('Отменить выбор', 'Отменить выбор')], max_length=30),
        ),
    ]
