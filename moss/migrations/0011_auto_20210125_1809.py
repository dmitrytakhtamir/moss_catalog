# Generated by Django 3.1.1 on 2021-01-25 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moss', '0010_auto_20210104_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='family',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='subclass',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]