from django.test import TestCase
from .models import Ingredient, Recipe, User, timezone, ChosenIngredient
from .views import getRecipies


# Create your tests here.
class RecipeTest(TestCase):

    def create_ingredient(self, name="test_ingredient"):
        return Ingredient.objects.create(name=name)

    def create_user(self, username="test_user", password="test_password"):
        return User.objects.create(username=username, password=password)

    def create_recipe(self, title="test_title", description="test_description"):
        i = self.create_ingredient()  # må legge til faktiske objekter i ingredients og author
        u = self.create_user()
        r = Recipe.objects.create(title=title, description=description, author=u)
        r.ingredients.add(ChosenIngredient.objects.create(recipe=r, ingredient=i))
        return r

    def test_recipe_creation(self):
        r = self.create_recipe()
        self.assertTrue(isinstance(r, Recipe))  # tester at r er en Recipe
        self.assertTrue(isinstance(r.author, User))  # tester at r.author er en User
        self.assertTrue(isinstance(r.ingredients.filter(ingredient__name="test_ingredient")[0],
                                   ChosenIngredient))  # tester at r.ingredients inneholder ingrediensen vi ga den og at det er en ingrediens
        self.assertEqual(r.visible, True)  # tester at r.visible er satt til False
        self.assertEqual("test_title", r.title)  # testter at tittelen til r er den vi ga
        self.assertEqual("test_user", r.author.username)  # tester at brukernavnet til author er det vi ga
        self.assertEqual("default.jpg", r.image.name)  # tester at r.image er default.jpg
        self.assertLessEqual(r.date_posted,
                             timezone.now())  # tester at tiden r ble laget er nå eller før(siden vi kan teste over et minuttskifte)
        self.assertEqual("E", r.niva)  # tester at nivå er standard, E
        self.assertEqual("L", r.tid)  # tsester at tid er standard, L


class SearchTest(TestCase):

    def create_user(self, username="test_user", password="test_password"):
        return User.objects.create(username=username, password=password)

    def create_user2(self, username="test_user2", password="test_password"):
        return User.objects.create(username=username, password=password)

    def create_ingredient(self, name="test_ingredient"):
        return Ingredient.objects.create(name=name)

    def create_ingredient2(self, name="test_ingredient2"):
        return Ingredient.objects.create(name=name)

    def create_recipe(self, title="test_title", description="test_description"):
        i = self.create_ingredient()  # må legge til faktiske objekter i ingredients og author
        u = self.create_user()
        r = Recipe.objects.create(title=title, description=description, author=u)
        r.ingredients.add(ChosenIngredient.objects.create(recipe=r, ingredient=i))
        return r

    def create_recipe2(self, title="test_title2", description="test_description"):
        i = self.create_ingredient2()  # må legge til faktiske objekter i ingredients og author
        u = self.create_user2()
        r = Recipe.objects.create(title=title, description=description, author=u)
        r.ingredients.add(ChosenIngredient.objects.create(recipe=r, ingredient=i))
        return r

    def test_search_function(self):
        liste = []
        r1 = self.create_recipe()
        r2 = self.create_recipe2()
        liste.append(r1)
        liste.append(r2)
        res = getRecipies(list, {'test_ingredient'})
        self.assertEqual(len(res), 1)  # tester at kun en av oppskriftene matcher søket
