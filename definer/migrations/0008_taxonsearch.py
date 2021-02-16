# Generated by Django 3.1.1 on 2021-01-04 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('definer', '0007_remove_taxondefiner_taxon_accordance'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxonSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subclass', models.CharField(blank=True, max_length=150)),
                ('order', models.CharField(blank=True, max_length=150)),
                ('family', models.CharField(blank=True, max_length=150)),
                ('genus', models.CharField(blank=True, max_length=150)),
                ('species', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]