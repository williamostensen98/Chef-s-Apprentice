from django.contrib import admin
from .models import Post
from .models import Recipe

# Register your models here.
admin.site.register(Post)
admin.site.register(Recipe)
