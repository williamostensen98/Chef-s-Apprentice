from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Recipe
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def home(request):
   queryset = Recipe.objects.all()

   if request.GET.get("sortBy") == 'date':
      queryset=sort_by_date(queryset)
      context = {
          #'posts': queryset,
          'recipies': queryset
      }
      return render(request, 'chefs_apprentice/home.html', context)


   recipe = queryset[0]
   i = recipe.ingredients.all()
   #print(i)
   #Ønsker her å prioritere oppskrifter fra kokker på startsiden.
   start_list=[]
   for a in queryset:
      if a.author.is_staff:
         start_list.append(a)

   for b in queryset:
      if b.author.is_staff==False:
         start_list.append(b)

   if request.GET.get("search"):
      #queryset=start_list
      query = request.GET.get("q")
      print('tittel: ', query)
      if query:
          queryset = queryset.filter(
              Q(title__icontains=query)
              )

      query_i = request.GET.get("q_i")
      print('ingredients: ', query_i)
      if query_i:
          input = query_i.split(',')
          ingredients = [x.strip() for x in input]
          ingredients = list(set(ingredients))
          queryset = getRecipies(queryset, ingredients)

      context = {
          #'posts': queryset,
          'recipies': queryset

      }
      if not query and not query_i:
         context = {
             #'posts': queryset,
             'recipies': start_list

         }
   else:
      context = {
          #'posts': queryset,
          'recipies': start_list

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
   #   for i in recipe_ingr
         for j in ingredients:
            if i.name==j:
               count[recipe] += 1

      if count[recipe]==0:
         del count[recipe]
   # Sorting by number of ingredients matched
   sorted_count = sorted(count.items(), key=lambda kv: kv[1], reverse=True)

   # List of recipies with highest match-count in descending order
   n = len(sorted_count)
   top = []
   print(sorted_count)
   for i in range (n):
      print(sorted_count[i][0].author)
      temp = i
      if sorted_count[i][0].author.is_staff and i != 0:
         counter = i-1
         for j in range (i,0,-1):
            if sorted_count[i][1]<sorted_count[counter][1]:
               break
            counter -= 1
            temp -= 1
      top.insert(temp,sorted_count[i][0] )
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

def sort_by_date(queryset):
   print(queryset)
   return sorted(queryset, key=lambda x: x.date_posted, reverse=True)
   #recipee_date = {}
   #for oppskrift in queryset:
   #   recipee_date[oppskrift] = (oppskrift.date_posted.month, oppskrift.date_posted.day, oppskrift.date_posted.hour, oppskrift.date_posted.minutes )
      # Impelenterer radix sort, sorterer først på minst signifikante siffer.

   #print(recipee_date)
   #sorted_on_minutes= sorted(recipee_date.items(), key=lambda kv: kv[3], reverse=True)
   #totally_sorted = sorted(recipee_date.items(), key=lambda kv: kv[1], reverse=True)
   #sorted_on_days = sorted(sorted_on_hours.items(), key=lambda kv: kv[0], reverse=True)
   #totally_sorted = sorted(recipee_date.items(), key=lambda kv: kv[1])
   #evt totally_sorted = sorted(sorted_on_days.items(), key=lambda kv: kv[0], reverse=True)
   #Ønsker å sortere på alle verdiene i en smekk
   #n= len(totally_sorted)
   #sortert_dato=[]
   #for i in range (n):
   #   sortert_dato.append(totally_sorted[i][0])
   #return queryset
