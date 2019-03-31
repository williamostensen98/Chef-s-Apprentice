from django.shortcuts import render, get_object_or_404
from .models import Recipe, ChosenIngredient
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from .forms import RecipeForm

from django.http import HttpResponse
from django.template.loader import get_template
from .utils import render_to_pdf

class curr_i:
    current_ingredients = set([])

@login_required
def home(request):
    queryset = Recipe.objects.all().order_by("-date_posted")
    recipe = queryset[0]

    # i = recipe.ingredients.all()
    # print(i)

    if request.GET.get("sortBy"):
        queryset = Recipe.objects.all().order_by("-date_posted")
        context = {
            'recipies': queryset
        }
        return render(request, 'chefs_apprentice/home.html', context)
    start_list = []
    for a in queryset:
        if a.author.is_staff:
            start_list.append(a)

    for b in queryset:
        if b.author.is_staff == False:
            start_list.append(b)

    query = request.GET.get("q")

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
        )

    query_i = request.GET.get("q_i")
    if request.GET.get("addIngredient"):
        input = query_i.split(',')
        ingredients = [x.strip() for x in input]
        ingredients = list(set(ingredients))
        #queryset = getRecipies(queryset, ingredients)
        print(curr_i.current_ingredients)
        curr_i.current_ingredients.update(ingredients)

    if request.GET.get("search_ingredient"):
        queryset = getRecipies(queryset, curr_i.current_ingredients)


    if not request.GET.get("search_ingredient") and not query:
        queryset = start_list
    #if not query_i and not query:
    #    queryset = start_list

    if request.GET.get("reset"):
        curr_i.current_ingredients = set([])


    paginator = Paginator(queryset, 5) # Show 5 contacts per page

    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context = {
       #'posts': queryset,
        'recipies': queryset,
        'current_ingredients': curr_i.current_ingredients
    }
    return render(request, 'chefs_apprentice/home.html', context)


def getRecipies(queryset, ingredients):
    count = {}
    print(ingredients)
    for recipe in queryset:
        count[recipe] = 0
        recipe_ingr = []
        for i in ChosenIngredient.objects.filter(recipe__title=recipe.title):
            recipe_ingr.append(i.ingredient)
        print(recipe_ingr)
        print(recipe)
        for i in recipe_ingr:
            for j in ingredients:
                if i.name == j:
                    count[recipe] += 1
        print(count[recipe])
        if count[recipe] == 0:
            del count[recipe]
            print(recipe.title + ' deleted')

    # Sorting by number of ingredients matched
    sorted_count = sorted(count.items(), key=lambda kv: kv[1], reverse=True)

    n = len(sorted_count)
    top = []
    for i in range(n):
        temp = i
        if sorted_count[i][0].author.is_staff and i != 0:
            counter = i - 1
            for j in range(i, 0, -1):
                if sorted_count[i][1] < sorted_count[counter][1]:
                    break
                counter -= 1
                temp -= 1
        top.insert(temp, sorted_count[i][0])
    return top


# Oppretting av oppskrift og validering av dette

def add_recipe(request):
    IngredientFormSet = inlineformset_factory(Recipe, ChosenIngredient, fields=['ingredient', 'measurement', 'unit'], extra=5)
    if request.method == "POST":
        recipe_form = RecipeForm(request.POST, prefix='recipe')
        ingredient_formset = IngredientFormSet(request.POST, request.FILES, prefix='ingredient')
        if recipe_form.is_valid() and ingredient_formset.is_valid():
            recipe = recipe_form.save(False)
            recipe.author = request.user
            recipe.save()
            ingredient_formset = IngredientFormSet(request.POST, request.FILES, prefix='ingredient', instance=recipe)
            ingredient_formset.is_valid()
            ingredient_formset.save()
            recipe_form = RecipeForm(prefix='recipe')
            ingredient_formset = IngredientFormSet(prefix='ingredient')
            return render(request, 'chefs_apprentice/recipe_form.html', {
                'recipe_form': recipe_form,
                'ingredient_formset': ingredient_formset, })
        else:
            return render(request, 'chefs_apprentice/recipe_form.html', {
                'recipe_form': recipe_form,
                'ingredient_formset': ingredient_formset,
            })
    else:
        recipe_form = RecipeForm(prefix='recipe')
        ingredient_formset = IngredientFormSet(prefix='ingredient')
        return render(request, 'chefs_apprentice/recipe_form.html', {
            'recipe_form': recipe_form,
            'ingredient_formset': ingredient_formset,
        })


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title','ingredients','image', 'description','niva','tid' ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['title','ingredients','image', 'description', 'niva','tid', 'visible']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author or self.request.user.is_staff:
            return True
        return False


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author or self.request.user.is_staff:
            return True
        return False


@login_required
def about(request):
    return render(request, 'chefs_apprentice/about.html', {'title': 'About'})


def view_recipe(request, pk, recipetitle):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = ChosenIngredient.objects.filter(recipe__title=recipe.title)
    context = {
        "recipe": recipe,
        "ingredients": ingredients,
    }

    return render(request, 'chefs_apprentice/recipe.html', context)


def downloadedrecipes(request):
    return render(request, 'chefs_apprentice/downloadedrecipes.html', {'title': 'downloadedrecipes'})


def favoriterecipes(request):
    return render(request, 'chefs_apprentice/favoriterecipes.html', {'title': 'favoriterecipes'})


# View for egne lagde oppskrifter i my account menyen

def myrecipes(request):
    queryset = Recipe.objects.all().order_by("-date_posted")  # sorter etter sist opprettet
    paginator = Paginator(queryset, 3)  # Show 3 contacts per page

    page = request.GET.get('page')  # pagination hvis det er flere sider
    queryset = paginator.get_page(page)
    context = {
        # 'posts': queryset,
        'recipies': queryset

    }

    return render(request, 'chefs_apprentice/myrecipes.html', context)


class GeneratePdf(View):
    def get(self, request, pk, recipetitle, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        context = {
            "recipe": recipe
        }
        # getting the template
        pdf = render_to_pdf('chefs_apprentice/recipe.html', context)

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
