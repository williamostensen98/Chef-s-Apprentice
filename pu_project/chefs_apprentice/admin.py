from django.contrib import admin
from .models import Post, Recipe, Ingredient

# Register your models here.
# admin.site.register(Post)
admin.site.register(Recipe)
admin.site.register(Ingredient)
