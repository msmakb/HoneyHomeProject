# Generated by Django 4.0.6 on 2022-07-31 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_task_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taskrate',
            old_name='on_time',
            new_name='on_time_rate',
        ),
    ]
