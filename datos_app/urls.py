# datos_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Esto define que la raíz de la APP llama a la vista mostrar_datos
    path('', views.mostrar_datos, name='datos_generados'),
]