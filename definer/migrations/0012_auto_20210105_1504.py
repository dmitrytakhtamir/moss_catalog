# Generated by Django 3.1.1 on 2021-01-05 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0011_taxonsearch_activation'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxonsearch',
            name='activ',
            field=models.CharField(default='deact', max_length=10),
        ),
        migrations.AlterField(
            model_name='taxonsearch',
            name='activation',
            field=models.CharField(blank=True, choices=[('Act', 'Выбрать'), ('Отменить выбор', 'Отменить выбор')], max_length=30),
        ),
    ]