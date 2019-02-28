from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='chef-home'),
    path('about/', views.about, name='chef-about'),
    path('<str:recipetitle>/<pk>', views.view_recipe, name="view_recipe")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
