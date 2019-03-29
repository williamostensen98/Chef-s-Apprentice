from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import RecipeCreateView, RecipeUpdateView, RecipeDeleteView, GeneratePdf

urlpatterns = [
    path('', views.home, name='chef-home'),
    path('about/', views.about, name='chef-about'),
    path('<str:recipetitle>/<pk>', views.view_recipe, name="view_recipe"),
    path('downloadedrecipes/', views.downloadedrecipes, name="downloadedrecipes"),
    path('favoriterecipes/', views.favoriterecipes, name="favoriterecipes"),
    path('myrecipes/', views.myrecipes, name="myrecipes"),
    path('new/', views.add_recipe, name='recipe-create'),
    path('<str:recipetitle>/<pk>/update/', RecipeUpdateView.as_view(), name="recipe-update"),
    path('<str:recipetitle>/<pk>/delete/', RecipeDeleteView.as_view(), name="recipe-delete"),
    path('<str:recipetitle>/<pk>/pdf/', GeneratePdf.as_view(), name="recipe-pdf")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
