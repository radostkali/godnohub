# Generated by Django 2.2.7 on 2019-12-29 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0015_auto_20191229_1935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postcard',
            old_name='tag_list',
            new_name='tags',
        ),
    ]
