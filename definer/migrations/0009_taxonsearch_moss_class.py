# Generated by Django 3.1.1 on 2021-01-04 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0008_taxonsearch'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxonsearch',
            name='moss_class',
            field=models.CharField(default='Bryopsida', max_length=150),
        ),
    ]