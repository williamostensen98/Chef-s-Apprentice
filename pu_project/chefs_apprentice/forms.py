
from .models import Recipe, ChosenIngredient
from django.forms import ModelForm
# from django.forms.models import inlineformset_factory




class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description','ingredients', 'image']

# ChosenIngredientFormSet = inlineformset_factory(Recipe, ChosenIngredient)
