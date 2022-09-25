# Generated by Django 4.0.6 on 2022-09-20 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warehouse_admin', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('instagram', models.CharField(blank=True, default='-', max_length=20, null=True)),
                ('shopee', models.CharField(blank=True, default='-', max_length=20, null=True)),
                ('facebook', models.CharField(blank=True, default='-', max_length=20, null=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.person')),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('numbers_of_questions', models.IntegerField(blank=True, default=0, null=True)),
                ('numbers_of_replies', models.IntegerField(blank=True, default=0, null=True)),
                ('period', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Running', 'Running'), ('Closed', 'Closed')], default='Pending', max_length=10, null=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SimpleQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('question', models.CharField(max_length=255)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media_manager.questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='SempleAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media_manager.customer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media_manager.simplequestion')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerPurchase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField()),
                ('Purchase_from', models.CharField(choices=[('Direct', 'Direct'), ('instagram', 'instagram'), ('shopee', 'shopee'), ('facebook', 'facebook'), ('Other', 'Other')], max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media_manager.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse_admin.itemtype')),
            ],
        ),
        migrations.CreateModel(
            name='ChoicesQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order', models.IntegerField()),
                ('question', models.CharField(max_length=255)),
                ('choice_one', models.CharField(max_length=50)),
                ('choice_two', models.CharField(max_length=50)),
                ('choice_three', models.CharField(max_length=50)),
                ('choice_four', models.CharField(max_length=50)),
                ('choice_five', models.CharField(max_length=50)),
                ('choice_six', models.CharField(max_length=50)),
                ('choice_seven', models.CharField(max_length=50)),
                ('choice_eight', models.CharField(max_length=50)),
                ('choice_nine', models.CharField(max_length=50)),
                ('choice_ten', models.CharField(max_length=50)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media_manager.questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='ChoicesAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('choice_one', models.BooleanField(blank=True, null=True)),
                ('choice_two', models.BooleanField(blank=True, null=True)),
                ('choice_three', models.BooleanField(blank=True, null=True)),
                ('choice_four', models.BooleanField(blank=True, null=True)),
                ('choice_five', models.BooleanField(blank=True, null=True)),
                ('choice_six', models.BooleanField(blank=True, null=True)),
                ('choice_seven', models.BooleanField(blank=True, null=True)),
                ('choice_eight', models.BooleanField(blank=True, null=True)),
                ('choice_nine', models.BooleanField(blank=True, null=True)),
                ('choice_ten', models.BooleanField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media_manager.customer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social_media_manager.choicesquestion')),
            ],
        ),
    ]
