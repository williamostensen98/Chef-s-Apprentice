from django.shortcuts import render
from .models import Post
from django.contrib.auth.decorators import login_required

# @login_required
def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'chefs_apprentice/home.html', context)

# def about(request):
#     return HttpResponse("<h1>About Page</h1>")
# @login_required
def about(request):
    return render(request, 'chefs_apprentice/about.html', {'title': 'About'})
