# Generated by Django 2.2.7 on 2019-12-15 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20191215_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='last_news_check',
            field=models.DateTimeField(auto_created=True),
        ),
    ]
