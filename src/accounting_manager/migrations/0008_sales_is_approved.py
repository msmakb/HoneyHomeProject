# Generated by Django 4.0.6 on 2022-08-14 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting_manager', '0007_alter_sales_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='sales',
            name='is_approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
