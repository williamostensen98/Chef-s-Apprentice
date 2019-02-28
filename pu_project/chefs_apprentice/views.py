from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def home(request):
   queryset = Recipe.objects.all()
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
