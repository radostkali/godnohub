# Generated by Django 2.2.7 on 2019-12-23 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0010_remove_card_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='author',
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
