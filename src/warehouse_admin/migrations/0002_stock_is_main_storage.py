# Generated by Django 4.1.1 on 2022-09-27 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='is_main_storage',
            field=models.BooleanField(default=False),
        ),
    ]
