# Generated by Django 4.2.1 on 2023-05-04 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('retinoscope', '0004_user_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='age',
        ),
    ]