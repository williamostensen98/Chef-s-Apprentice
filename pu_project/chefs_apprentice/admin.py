from django.contrib import admin
from .models import Recipe, Ingredient

# Register your models here.
# admin.site.register(Recipe)
admin.site.register(Ingredient)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "visible", "author")
    actions = ["make_visible", "make_hidden"]

    def make_visible(self, request, queryset):
        queryset.update(visible=True)

    def make_hidden(self, request, queryset):
        queryset.update(visible=False)
