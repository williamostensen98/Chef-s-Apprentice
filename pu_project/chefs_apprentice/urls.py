from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chef-home'),
    path('about/', views.about, name='chef-about'),
    path('<str:recipetitle>/<pk>', views.view_recipe, name="view_recipe")
]
