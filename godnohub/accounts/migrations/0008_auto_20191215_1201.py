# Generated by Django 2.2.7 on 2019-12-15 09:01

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20191215_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_news_check',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 17, 9, 1, 22, 972733, tzinfo=utc)),
        ),
    ]
