from django.contrib import admin
from .models import  Utlisateur

# Register your models here.



@admin.register(Utlisateur)
class UtlisateurAdmin(admin.ModelAdmin):
    list_display=  ("username", "email")
    search_fields = ("username", )