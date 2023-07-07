# Generated by Django 4.2.1 on 2023-06-13 13:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('retinoscope', '0013_alter_history_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='img',
            field=models.ImageField(default='default.jpg', upload_to='account_pics'),
        ),
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 6, 13, 13, 11, 49, 941935, tzinfo=datetime.timezone.utc)),
        ),
    ]