# Generated by Django 4.0.6 on 2022-08-13 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_itemcard_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodsmovement',
            name='sender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
