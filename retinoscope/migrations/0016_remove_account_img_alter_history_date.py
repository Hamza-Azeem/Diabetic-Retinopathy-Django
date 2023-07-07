# Generated by Django 4.2.1 on 2023-06-14 14:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('retinoscope', '0015_alter_history_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='img',
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
