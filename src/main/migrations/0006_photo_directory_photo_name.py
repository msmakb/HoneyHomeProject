# Generated by Django 4.0.6 on 2022-07-28 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_employee_account_alter_employee_person_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='directory',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='name',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
