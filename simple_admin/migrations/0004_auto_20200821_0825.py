# Generated by Django 3.1 on 2020-08-21 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simple_admin', '0003_auto_20200821_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='is_active'),
        ),
    ]
