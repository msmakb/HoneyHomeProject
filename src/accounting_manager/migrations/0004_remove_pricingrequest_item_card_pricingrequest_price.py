# Generated by Django 4.0.6 on 2022-08-13 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_manager', '0003_pricingrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricingrequest',
            name='item_card',
        ),
        migrations.AddField(
            model_name='pricingrequest',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
