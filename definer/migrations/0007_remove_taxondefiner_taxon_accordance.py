# Generated by Django 3.1.1 on 2020-12-03 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0006_taxondefiner_taxon_accordance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxondefiner',
            name='taxon_accordance',
        ),
    ]
