from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Employe)
class Employe(admin.ModelAdmin):
    list_display=  ("nom", "prenom", "matricule", "depart", "emails")
    search_fields = ("nom","prenom","matricule", "depart" )

@admin.register(ArchiveEmploye)
class ArchiveEAdmin(admin.ModelAdmin):
    list_display=  ("nom", "prenom", "matricule", "depart", "emails", "motif")
    search_fields = ("nom","prenom","matricule", "depart", "motif" )


@admin.register(Contrat)
class ContratAdmin(admin.ModelAdmin):
    list_display=  ("employe", "poste","types",  "dateSignature", "date_fin", "salaire")
    search_fields = ("employe","types","depart")

@admin.register(ContratArchive)
class ArchiveContratAdmin(admin.ModelAdmin):
    list_display=  ("employe", "poste","types", "dateSignature", "date_fin", "date_archive")
    search_fields = ("employe","types","depart", "motif" )

@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display=  ("types", "description","date_debut", "date_fin")
    search_fields = ("types","description" )

@admin.register(Conge)
class CongeAdmin(admin.ModelAdmin):
    list_display=  ("employe","types", "motif", "date_debut", "date_fin")
    search_fields = ("employe","types", "motif" )

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display=  ("employe","intitule", "description", "date_notif",)
    search_fields = ("employe","date_notif", "intitule" )

@admin.register(Messagess)
class MessagesAdmin(admin.ModelAdmin):
    list_display=  ("obj","contenu", "emetteur", "recepteur", "date_envoie")
    search_fields = ("emetteur","recepteur", "date_envoie" )

@admin.register(Departement)
class DepartsAdmin(admin.ModelAdmin):
    list_display=  ("nom","responsable",)
    search_fields = ("nom","responsable",)







