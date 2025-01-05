"""
URL configuration for administration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from django.conf.urls.static import static
from administration import settings
import gestionAdministration
from gestionAdministration import views
from comptes import views
from django.contrib.auth import views

urlpatterns = [
    path('gestion_systeme/', admin.site.urls),
    path('', include('comptes.urls')),
    path('administration/', include('gestionAdministration.urls')),
    path('reset_pass/', views.PasswordResetView.as_view(), name='reset_pwd'),
    path('reset_pass_send/', views.PasswordResetDoneView.as_view(), name='envoie_mail'),
    path('reset_confirm/<uid64>/<token>', views.PasswordResetConfirmView.as_view(), name='cofirmation' ),
    path('reset_complet', views.PasswordResetCompleteView.as_view(), name='resetComplet'),
   
]

urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

