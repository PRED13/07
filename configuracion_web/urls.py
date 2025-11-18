# configuracion_web/urls.py (Archivo principal del proyecto)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # DEBE SER ESTA LÍNEA EXACTA para que funcione en la URL raíz (/)
    path('', include('datos_app.urls')), 
]