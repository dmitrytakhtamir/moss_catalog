# Generated by Django 3.1.1 on 2021-02-12 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0021_auto_20210207_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonsearch',
            name='activation',
            field=models.CharField(blank=True, choices=[('Act', 'Act'), ('Deact', 'Deact'), ('Frozen', 'Frozen')], default='Act', max_length=30),
        ),
    ]
