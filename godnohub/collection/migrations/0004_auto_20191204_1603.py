# Generated by Django 2.2.7 on 2019-12-04 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_type_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
