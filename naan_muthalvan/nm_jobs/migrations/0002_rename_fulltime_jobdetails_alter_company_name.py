# Generated by Django 4.0.6 on 2023-02-19 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nm_jobs', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FullTime',
            new_name='JobDetails',
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
