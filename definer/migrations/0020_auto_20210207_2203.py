# Generated by Django 3.1.1 on 2021-02-07 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0019_auto_20210207_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonsearch',
            name='division',
            field=models.CharField(blank=True, default='Bryophita', max_length=150),
        ),
    ]
