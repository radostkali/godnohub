# Generated by Django 2.2.7 on 2019-12-05 14:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='follow',
            field=models.ManyToManyField(blank=True, null=True, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
    ]
