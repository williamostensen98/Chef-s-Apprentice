from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ChosenIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', related_name='+', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    measurement = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=5,
                                      validators=[MinValueValidator(0.00)])
    unit_choices = (
        ("liter", "liter"),
        ("dl", "dl"),
        ("kg", "kg"),
        ("gram", "gram"),
        ("ss", "ss"),
        ("ts", "ts"),
        ("klype", "klype"),
        ("dråpe", "dråpe"),
        ("boks", "boks"),
        ("pakke", "pakke"),
        ("pose", "pose"),
    )
    unit = models.CharField(choices=unit_choices, max_length=15, blank=True)


class Recipe(models.Model):
    title = models.CharField(max_length=100)  # tenkt samme som tilhørende post
    ingredients = models.ManyToManyField(ChosenIngredient, blank=True, related_name='+')  # liste av ingrediensobjekter
    description = models.TextField()  # tenkt sammen med content i post
    date_posted = models.DateTimeField(
        default=timezone.now)  # DateTimeField(auto_now=True) ville satt datoen til akkurat nå
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)  # on_delete=models.CASCADE sier at hvis brukeren blir slettet vil postene også bli slettet
    image = models.ImageField(default='default.jpg', upload_to='food_pics')
    visible = models.BooleanField(default=True)
    NIVA = (
        ('E','Enkel'),
        ('M','Middels'),
        ('V','Vanskelig'),
    )
    TID = (
        ('L','Under 30 min'),
        ('M', 'Ca. 30-60 min'),
        ('S', 'Over 1 time'),
    )
    tid = models.CharField(default='L', max_length=1, choices=TID)
    niva = models.CharField(default='E',max_length=1, choices=NIVA)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_recipe', kwargs={'recipetitle': self.title, 'pk': self.pk})


class User(models.Model):
    username = models.CharField(max_length=100)
