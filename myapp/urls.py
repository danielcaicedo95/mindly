from django.urls import path
from . import views

urlpatterns = [
    path('seo_diagnosis/', views.seo_diagnosis, name='seo_diagnosis'),
    path('', views.home, name='home'),  # URL para la página de inicio
]
