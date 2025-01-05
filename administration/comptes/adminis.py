from django.contrib.admin import AdminSite

from administration.comptes.models import Utlisateur
from administration.gestionAdministration import admin
class CustomAdminsite(AdminSite):
    site_title =" Espace d'administration "
    site_header = " Espace d'administration "
    index_title = "Bienvenue sur K-Assali Administration"

admin_site = CustomAdminsite(name="custom_admin")

admin.site.register(Utlisateur)