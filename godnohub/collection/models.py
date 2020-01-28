from django.db import models
from django.contrib.auth.models import User
from .scripts import get_average_color
from django.utils import timezone


# Create your models here.
class Rating(models.Model):

    rate = models.IntegerField(blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Type(models.Model):

    class Meta:
        ordering = ['-timestamp']
        
    name = models.CharField(max_length=120, blank=False, null=False)
    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    picture = models.URLField(blank=True, null=True)
    color = models.CharField(max_length=9, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.picture:
            self.color = get_average_color(self.picture)
        super(Type, self).save(*args, **kwargs)

    def __str__(self):
        return '%s.%s: %s' % (self.id, self.name, self.owner)


class Tag(models.Model):

    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=120, blank=False, null=False)
    type = models.ForeignKey(Type, null=False, blank=False, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return '%s.%s: %s - %s' % (self.id, self.name, self.owner, self.type)


class Card(models.Model):

    class Meta:
        ordering = ['-timestamp']

    timestamp = models.DateTimeField(auto_created=True, null=False, blank=False)  # Adding entry timestamp
    title = models.CharField(max_length=300, blank=False, null=True)
    picture = models.ImageField(upload_to='images', null=True, blank=True)
    imgur_url = models.URLField(blank=True, null=True)
    color = models.CharField(max_length=9, blank=True, null=True)
    type = models.ForeignKey(Type, null=True, blank=False, on_delete=models.SET_NULL)
    rating = models.ForeignKey(Rating, null=True, blank=False, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag)
    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.imgur_url:
            self.color = get_average_color(self.imgur_url)
        card_type = self.type
        card_type.timestamp = timezone.now()
        card_type.save()
        super(Card, self).save(*args, **kwargs)

    def __str__(self):
        return '%s.%s: %s' % (self.id, self.title, self.owner)


class PostCard(models.Model):

    class Meta:
        ordering = ['-timestamp']

    timestamp = models.DateTimeField(auto_created=True, null=False, blank=False)  # Adding entry timestamp
    title = models.CharField(max_length=300, blank=False, null=True)
    imgur_url = models.URLField(blank=True, null=True)
    color = models.CharField(max_length=9, blank=True, null=True)
    type = models.CharField(max_length=300, blank=False, null=True)
    tags = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.imgur_url:
            self.color = get_average_color(self.imgur_url)
        super(PostCard, self).save(*args, **kwargs)

    def __str__(self):
        return '%s.%s: %s' % (self.id, self.title, self.owner)
