# Generated by Django 2.1.1 on 2018-10-10 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20181010_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phasefields',
            old_name='name',
            new_name='label',
        ),
        migrations.RenameField(
            model_name='phasefields',
            old_name='field_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='phasefields',
            old_name='field_widget',
            new_name='widget',
        ),
    ]
