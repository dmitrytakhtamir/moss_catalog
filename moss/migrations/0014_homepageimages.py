# Generated by Django 3.1.1 on 2021-01-28 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moss', '0013_delete_homepageimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
