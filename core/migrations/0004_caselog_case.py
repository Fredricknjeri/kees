# Generated by Django 2.1.1 on 2018-10-03 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20181003_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='caselog',
            name='case',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='core.Case'),
            preserve_default=False,
        ),
    ]
