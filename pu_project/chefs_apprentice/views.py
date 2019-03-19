from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator


class curr_i:
    current_ingredients = set([])


@login_required
def home(request):
    queryset = Recipe.objects.all() # .order_by("-date_posted")

    if request.GET.get("sortBy") == 'date':
        queryset =  Recipe.objects.all().order_by("-date_posted")
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

    paginator = Paginator(queryset, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    context = {
       #'posts': queryset,
        'recipies': queryset,
        'current_ingredients': curr_i.current_ingredients
    }


    return render(request, 'chefs_apprentice/home.html', context)


#current_ingredients = set([])



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
        if count[recipe] == 0:
            del count[recipe]

   # Sorting by number of ingredients matched
    sorted_count = sorted(count.items(), key=lambda kv: kv[1], reverse=True)

    n = len(sorted_count)
    top = []
    for i in range(n):
        temp = i
        if sorted_count[i][0].author.is_staff and i != 0:
            counter = i-1
            for j in range(i, 0, -1):
                if sorted_count[i][1] < sorted_count[counter][1]:
                    break
                counter -= 1
                temp -= 1
        top.insert(temp, sorted_count[i][0])
    return top

   # n = len(sorted_count)
   #
   # # Extracting top n recipies
   # top = []
   # for i in range(n):
   #     # top.append(sorted_count[i][0])
   #     temp = i
   #     if sorted_count[i][0].author.is_staff and i != 0:
   #         counter = i-1
   #         for j in range(i,0,-1):
   #             if sorted_count[i][0] < sorted_count[counter][1]:
   #                 break
   #          counter -= 1
   #              temp -= 1
   #      top.insert(temp, sorted_count[i][0])
   #
   #  return top
   # List of recipies with highest match-count in descending order


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
