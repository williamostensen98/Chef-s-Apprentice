from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator


@login_required
def home(request):
   queryset = Recipe.objects.all().order_by("-date_posted")
   recipe = queryset[0]
   i = recipe.ingredients.all()
   #print(i)
   query = request.GET.get("q")
   if query:
       queryset = queryset.filter(
           Q(title__icontains=query)
           )

   query_i = request.GET.get("q_i")
   if query_i:
       input = query_i.split(',')
       ingredients = [x.strip() for x in input]
       ingredients = list(set(ingredients))
       queryset = getRecipies(queryset, ingredients)

   context = {
       #'posts': queryset,
       'recipies': queryset

   }
   return render(request, 'chefs_apprentice/home.html', context)

def getRecipies(queryset, ingredients):
   count = {}
   print(ingredients)
   for recipe in queryset:
       count[recipe] = 0
       recipe_ingr = recipe.ingredients.all()
       print(recipe_ingr)
       for i in recipe_ingr:
   #    for i in recipe_ingr
           for j in ingredients:
               if i.name==j:
                   count[recipe] += 1
   if count[recipe]==0:
       del count[recipe]

   # Sorting by number of ingredients matched
   sorted_count = sorted(count.items(), key=lambda kv: kv[1], reverse=True)

   # List of recipies with highest match-count in descending order
   n = min(len(sorted_count), 5)

   # Extracting top n recipies
   top = []
   for i in range(n):
       top.append(sorted_count[i][0])

   return top

# def about(request):
#     return HttpResponse("<h1>About Page</h1>")
@login_required
def about(request):
    return render(request, 'chefs_apprentice/about.html', {'title': 'About'})

def view_recipe(request, pk, recipetitle):
    recipe=get_object_or_404(Recipe, pk=pk)
    context = {
        "recipe":recipe,
    }
    return render(request, 'chefs_apprentice/recipe.html', context)

def downloadedrecipes(request):
    return render(request, 'chefs_apprentice/downloadedrecipes.html', {'title': 'downloadedrecipes'})

def favoriterecipes(request):
        return render(request, 'chefs_apprentice/favoriterecipes.html', {'title': 'favoriterecipes'})


def myrecipes(request):
        return render(request, 'chefs_apprentice/myrecipes.html', {'title': 'myrecipes'})


# class RecipeListView(ListView):
#     model = Recipe
#     template_name = 'chefs_apprentice/home.html'
#     context_object_name = 'recipies'
#
def downloadrecipe(request, id=0):
    recipe=get_object_or_404(recipe, pk=id)
    if id!=0 and request.user.is_authenticated:
        if not recipe.download.filter(id=request.user.id).exists():
            recipe.download.add(request.user.id)
        else:
            recipe.download.remove(request.user.id)
    return HttpResponseRedirect("/recipe" + id)


def download_list(request):
    user=request.user
    queryset = user.download.all().order_by("-pk")
    #paginator = Paginator(queryset, 10)
    #page = request.GET.get('page')
    #recipe = paginator.get_page(page)
    #isExecEd = isExecutiveEditor(request.user)
    context ={
    'maintitle': 'Downloaded recipes',
    'recipes' : queryset
    }
    return render(request, 'chefs_apprentice/downloadedrecipes.html', context)
