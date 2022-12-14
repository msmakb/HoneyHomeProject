# Generated by Django 4.1.1 on 2022-09-27 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('position', models.CharField(choices=[('CEO', 'CEO'), ('Human Resources', 'Human Resources'), ('Warehouse Admin', 'Warehouse Admin'), ('Accounting Manager', 'Accounting Manager'), ('Social Media Manager', 'Social Media Manager'), ('Designer', 'Designer'), ('Distributor', 'Distributor')], max_length=20)),
                ('account', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('person', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.person')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, default='-', max_length=500, null=True)),
                ('status', models.CharField(blank=True, choices=[('In-Progress', 'In-Progress'), ('On-Time', 'On-Time'), ('Late-Submission', 'Late-Submission'), ('Overdue', 'Overdue')], default='In-Progress', max_length=20, null=True)),
                ('receiving_date', models.DateTimeField(auto_now_add=True)),
                ('deadline_date', models.DateTimeField(blank=True, null=True)),
                ('submission_date', models.DateTimeField(blank=True, null=True)),
                ('is_rated', models.BooleanField(blank=True, default=False, null=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='human_resources.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Week',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('week_start_date', models.DateField(blank=True, null=True)),
                ('week_end_date', models.DateField(blank=True, null=True)),
                ('is_rated', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('rate', models.FloatField()),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='human_resources.employee')),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='human_resources.week')),
            ],
        ),
        migrations.CreateModel(
            name='TaskRate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('on_time_rate', models.FloatField()),
                ('rate', models.FloatField()),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='human_resources.task')),
            ],
        ),
    ]
