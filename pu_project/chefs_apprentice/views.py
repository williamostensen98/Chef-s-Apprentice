from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def home(request):
    queryset = Recipe.objects.all()
    query = request.GET.get("q")
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)

            )
    context = {
        # 'Recipe': Recipe.objects.all(),
        'Recipe': queryset
    }
    return render(request, 'chefs_apprentice/home.html', context)

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
