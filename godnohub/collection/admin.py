from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Card)
admin.site.register(PostCard)
admin.site.register(Rating)
admin.site.register(Tag)
admin.site.register(Type)