from django.contrib import admin
from django.urls import path

from gestionAdministration import views

urlpatterns = [
     #acceuil
     path('AcceuilRH/', views.acceuilrh, name='acceuilRH'),
     path('AcceuilDG/', views.acceuildg, name='acceuilDG'),
     path('AcceuilChef/', views.acceuilchef, name='acceuilChef'),
     path('AcceuilE/', views.acceuilemploye, name='acceuilEmploye'),
     path('Acceuil/', views.acceuil, name='acceuil'),

     #personnel (ajout, modification, ...)
     path('register/', views.afficherAjout, name='formulairePersonnel'),
     path('listePersonnel/', views.afficherListPersonnel, name='listePersonnel'),
     path('archivePersonnel/', views.archivePersonnel, name='archivePersonnel'),
     path('details_archives/<int:id>/', views.detailsArchive, name='details_archive'),
     path('supprimer_archives/<int:id>/', views.supprimerArchive, name='supprimerArchive'),
     path('details_personnel/<int:id>/', views.detailsPersonnel, name='details'),
     path('details/', views.detailsPerso, name='detailsPerson'),
     path('modifier/<int:id>/', views.modifierP, name='modifierP'),
     path('supprimer/<int:id>/', views.supprimerPersonnel, name='supprimerP'),
     path('supprimer_compte/<int:id>/', views.supprimerCompte, name='supprimerCompte'),
     path('Liste_compte/', views.listecompte, name='listeCompte'),

     #Contrat (ajout, modification, archie, ...)
     path('contrat/', views.listeContrat, name='listeContrat'),
     path('archive/', views.archivesContrat, name='archiveContrat'),
     path('ajouterContrat/', views.ajouterContrat, name='ajouterContrat'),
     path('modifierContrat/<int:id>/', views.modifierContrat, name='modifierContrat'),
      path('details_contrat/<int:id>/', views.detailsContrat, name='details_contrat'),
     path('supprimerContrat/<int:id>/', views.supprimerContrat, name='supprimerContrat'),
     path('archiverContrat/<int:id>/', views.archiverContrat, name='archiverContrat'),
     path('renouvelerContrat/<int:id>/', views.renouvelerContrat, name='renouvelerContrat'),

     #Evenement
     path('evenement/', views.evenement, name='evenement'),
     path('ajouterEvent/', views.ajouterEvenement, name='ajouterEvent'),
     path('annulerEvent/<int:id>', views.supprimerEvent, name='annulerEvent'),

     #Message (lecture, envoie, reception, ...)
     path('Message/', views.affichemsg, name='message_msg'),
     path('message_envoyé/', views.sendedmessage, name='message_envoye'),
     path('Lecture/<int:id>', views.liremessage, name='lire_message'),
     path('lecture_archive/<int:id>', views.lireArchivemessage, name='lire_archive_message'),
     path('envoyer_message/', views.envoyermessage, name="envoyer_message"),
     path('repondre/<int:id>', views.repondreMessage, name='repondre_message'),
     path('supprimer_msg/<int:id>', views.supprimerMsg, name='supprimer_msg'),
     path('supprimer_arhive_msg/<int:id>', views.supprimerArchiveMessage, name='supprimer_archive_message'),
     path('archive_msg/', views.afficheArchivemsg, name='archive_msg'),

     #notification
     path('notifications/', views.affichenotif, name="notifcations"),
     path('lire_notification/<int:id>', views.lireNotif, name="lire_notif"),
     path('supprimer_notification/<int:id>', views.supprimerNotif, name="supprimer_notif"),
     

     #departement
     path('departement/', views.departement_views, name='departement'),
     path('ajouter_Depatement/', views.ajouterDepart, name='ajouter_deprt'),
     path('modifier_depart/<int:id>', views.modifierDepartement, name='modifier_Depart'),

     #demande de congé
     path('demader_congé/', views.demandeConge, name='demande_Congé'),
     path('liste_demande/', views.listeDemande, name='liste_demande_Congé'),
     path('details_demande/<int:id>', views.detailsDemande, name='details_demande_congé'),
     path('refus_demande/<int:id>', views.refuserConge, name='refuser'),
     path('approuver_demande/<int:id>', views.accorderConge, name='accorder'),
     path('congé/', views.afficherConge, name='liste_congé'),
    ]