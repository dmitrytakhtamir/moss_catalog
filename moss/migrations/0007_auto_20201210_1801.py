# Generated by Django 3.1.1 on 2020-12-10 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moss', '0006_subclass_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='order',
            new_name='parent_class',
        ),
        migrations.RenameField(
            model_name='genus',
            old_name='family',
            new_name='parent_class',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='subclass',
            new_name='parent_class',
        ),
        migrations.RenameField(
            model_name='species',
            old_name='genus',
            new_name='parent_class',
        ),
        migrations.RenameField(
            model_name='subclass',
            old_name='class_tax',
            new_name='parent_class',
        ),
    ]