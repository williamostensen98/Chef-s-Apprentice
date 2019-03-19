from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator


@login_required
def home(request):
    queryset = Recipe.objects.all().order_by("-date_posted")
    recipe = queryset[0]

    # i = recipe.ingredients.all()
   #print(i)


    if request.GET.get("sortBy"):
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
    if query_i:
        input = query_i.split(',')
        ingredients = [x.strip() for x in input]
        ingredients = list(set(ingredients))
        queryset = getRecipies(queryset, ingredients)


    if not query_i and not query:
        queryset = start_list

    paginator = Paginator(queryset, 3) # Show 25 contacts per page

    page = request.GET.get('page')
    queryset = paginator.get_page(page)
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

# Oppretting av oppskrift og validering av dette

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['title','ingredients','image', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ['title','ingredients','image', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False


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

# View for egne lagde oppskrifter i my account menyen

def myrecipes(request):
        queryset = Recipe.objects.all().order_by("-date_posted") # sorter etter sist opprettet
        paginator = Paginator(queryset, 3) # Show 3 contacts per page

        page = request.GET.get('page') # pagination hvis det er flere sider
        queryset = paginator.get_page(page)
        context = {
           #'posts': queryset,
            'recipies': queryset

        }

        return render(request, 'chefs_apprentice/myrecipes.html', context)


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
