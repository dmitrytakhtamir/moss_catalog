# Generated by Django 3.1.1 on 2021-01-28 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moss', '0017_auto_20210128_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepageimages',
            name='img_field',
            field=models.CharField(choices=[], max_length=100),
        ),
    ]
