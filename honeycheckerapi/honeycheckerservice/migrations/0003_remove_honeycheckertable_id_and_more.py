# Generated by Django 5.1.3 on 2024-11-21 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('honeycheckerservice', '0002_rename_honeychecker_honeycheckertable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='honeycheckertable',
            name='id',
        ),
        migrations.AlterField(
            model_name='honeycheckertable',
            name='user_random_index',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='User Random Index'),
        ),
    ]
