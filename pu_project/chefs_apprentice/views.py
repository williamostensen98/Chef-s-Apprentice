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
    queryset = Recipe.objects.all().order_by("-date_posted") # sorterer visning av oppskrifter på hjemmesiden slik at de nyeste kommer øverst.
    recipe = queryset[0]

    # legger først til alle oppskrifter opprettet av sertifiserte kokker
    start_list = []
    for a in queryset:
        if a.author.is_staff:
            start_list.append(a)

    # så de resterende oppskriften laget av vanlige brukere
    # disse legges inn i start_list og denne blir så querysettet som skal vises gitt at det ikke er noe søk.
    for b in queryset:
        if b.author.is_staff == False:
            start_list.append(b)

    # henter ut innhold i søkefeltet(oppskrift)
    query = request.GET.get("q")

    # hvis det er skrevet noe inn der så skal querysettet filtreres på det som søkes på
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) # hvis en oppskriftstittel inneholder søkeordet - legg til oi queryset
        )

    # henter ut innhold fra ingrediens-søkefelt
    query_i = request.GET.get("q_i")

    # hvis det er innhold og ADD trykkes
    if request.GET.get("addIngredient"):
        input = query_i.split(',') # hvis det er skrevet flere ingredienser inn - split på komma
        ingredients = [x.strip() for x in input] # strip for alt annet
        ingredients = list(set(ingredients)) # lag et set() for å unngå duplikater
        #queryset = getRecipies(queryset, ingredients)
        print(curr_i.current_ingredients)
        curr_i.current_ingredients.update(ingredients) # legg til ingrediensen i current_ingredients settet

    # hvis det er innhold i current_ingredients og det trykkes på søke knappen
    if request.GET.get("search_ingredient"):
        queryset = getRecipies(queryset, curr_i.current_ingredients)
        # legger alle ingredienser i current_ingredients inn i query som filterer ut alle oppskrifter som inneholder disse ingrediensen(se getRecipes)

    # hvis det ikke er noe innhold i hverken av søkefeltene skal start_list som ble opprettet på begynnelsen vises
    if not request.GET.get("search_ingredient") and not query:
        queryset = start_list
    #if not query_i and not query:
    #    queryset = start_list

    # resetter søkefeltene
    if request.GET.get("reset"):
        curr_i.current_ingredients = set([])


    # funksjonalitet for å dele opp sidene i x antall oppskrifter per side med paginering
    paginator = Paginator(queryset, 5) # Vis 5 oppskrifter per side

    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context = {
       #'posts': queryset,
        'recipies': queryset,
        'current_ingredients': curr_i.current_ingredients
    }
    return render(request, 'chefs_apprentice/home.html', context)

# henter ut oppskriftene med best match mellom queryset og ingredients
#
#
def getRecipies(queryset, ingredients):
    count = {}
    for recipe in queryset:
        count[recipe] = 0
        recipe_ingr = []
        for i in ChosenIngredient.objects.filter(recipe__title=recipe.title):
            recipe_ingr.append(i.ingredient)
        for i in recipe_ingr:
            for j in ingredients:
                if i.name == j:
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


# View for oppretting av oppskrifter
# Tar inn LoginRequiredMixin(krever at bruker er logget inn) og CreateView(ferdig innebygd funksjonalitet for oppretting i Django)
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe # tar utgangspunkt i Recipe modellen( se models)
    fields = ['title','ingredients','image', 'description','niva','tid', 'visible' ] # definerer hvilke felter som skal være med i dette skjemaet

    # funksjon for validering av skjemaet
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# View for oppdatering av oppskrifter
# Tar inn LoginRequiredMixin, UserPassesTestMixin(krever at innlogget bruker er samme bruker somn har laget oppskriften og UpdateView(ferdig modul i Django))
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

# View for å slette Oppskrfter og kjører samme krav til bruker
class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'
    # sender siden tilbake til hjemsiden og sletter oppskeriften fra db
    # funskjon som tester om brukeren er forfatteren av oppskriften
    # enten er forfatter brukeren selv eller kokk/admin

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author or self.request.user.is_staff:
            return True
        return False


@login_required # funksjonalitet for å kreve at bruker er logget inn
def about(request):
    return render(request, 'chefs_apprentice/about.html', {'title': 'About'})


# function-based-view for siden når man trykker på en oppskrift
def view_recipe(request, pk, recipetitle):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = ChosenIngredient.objects.filter(recipe__title=recipe.title) # henter ut alle ingrediense
    context = {
        "recipe": recipe,
        "ingredients": ingredients,
    }
    # legger oppskrften og ingrediensene til i dictionaryen

    return render(request, 'chefs_apprentice/recipe.html', context) # rendrer html templaten med innholdet hentet i denne funksjonen


def downloadedrecipes(request):
    return render(request, 'chefs_apprentice/downloadedrecipes.html', {'title': 'downloadedrecipes'})


def favoriterecipes(request):
    return render(request, 'chefs_apprentice/favoriterecipes.html', {'title': 'favoriterecipes'})


# View for egne lagde oppskrifter i my account menyen
#henter bare ut alle oppsrkfiter i databasen
# Disse blir så filtrert etter hvilken som er brukeren sine egenlagde i html templaten

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


# Klasse for oppretting av pdf av oppskriften
class GeneratePdf(View):
    # get metoden henter ut hvilken oppskrft det gjelder(hvilken oppskrift man er inne på)
    # sender så denne i en dictionary til render_to_pdf funksjonen som gjør oppskriften om til pdf
    # Viser så en HttpResponse med denne pdfen
    def get(self, request, pk, recipetitle, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        context = {
            "recipe": recipe
        }
        # getting the template
        pdf = render_to_pdf('chefs_apprentice/recipe.html', context)

        # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
