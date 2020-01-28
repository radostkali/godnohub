from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    page_address = models.CharField(max_length=23, blank=True, null=True, unique=True)
    page_private = models.BooleanField(default=False, blank=False, null=False)
    avatar = models.URLField(blank=True, null=True)
    last_news_check = models.DateTimeField(auto_created=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.page_address:
            self.page_address = self.user.id
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Following(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField(User, related_name='follower', blank=True)

    def __str__(self):
        return self.user.username