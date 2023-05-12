"""
URL configuration for GestionInventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appGestionInventario import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/',views.vistaLogin),
    path('iniciarSesion/',views.login),
    path('vistaRegistrarUsuario/',views.vistaRegistrarUsuarios),
    path('registrarUsuario/',views.registrarUsuario),
    path('inicioAdministrador/',views.inicioAdministrador),
    path('inicioInstructor/',views.inicioInstructor),
    path('inicioAsistente/',views.inicioAsistente),
    path('vistaGestionUsuarios/',views.vistaGestionUsuarios),
    path('eliminarUsuario/<int:id>/', views.eliminarUsuario),
    path('consultarUsuario/<int:id>/', views.consultarUsuario),
    path('actualizarUsuario/', views.actualizarUsuario),
    path('vistaGestionarDevolutivos/',views.vistaGestionarDevolutivos),
    path('vistaRegistrarDevolutivo/',views.vistaRegistrarDevolutivo),
    path('registrarDevolutivo/',views.registrarDevolutivo),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )