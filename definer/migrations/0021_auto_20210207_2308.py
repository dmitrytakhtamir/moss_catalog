# Generated by Django 3.1.1 on 2021-02-07 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0020_auto_20210207_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonsearch',
            name='division',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]