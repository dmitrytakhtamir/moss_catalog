# Generated by Django 3.1.1 on 2021-01-05 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0012_auto_20210105_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonsearch',
            name='activ',
            field=models.CharField(blank=True, default='deact', max_length=10),
        ),
        migrations.AlterField(
            model_name='taxonsearch',
            name='activation',
            field=models.CharField(blank=True, choices=[('Act', 'Act'), ('Deact', 'Deact')], default='Deact', max_length=30),
        ),
    ]