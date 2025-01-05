from datetime import timedelta, timezone
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Departement(models.Model):
    responsable = models.OneToOneField('Employe', on_delete=models.SET_NULL, null=True, related_name='departement')
    nom = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.nom


class BaseEmploye(models.Model):
    matricule = models.CharField(max_length=200, blank=False, null=False, unique=True)
    nom =models.CharField(max_length=25, blank=False, null=False)
    prenom = models.CharField(max_length=15)
    sexe = models.CharField(max_length=2)
    emails= models.EmailField(null=False, blank=False)
    date_naissance= models.DateField(blank=True)
    lieu_naissance = models.CharField(max_length=200)
    cni = models.CharField(max_length=14, blank=False, null=False)
    lieu_residence = models.CharField(max_length=150, null=False, blank=False)
    civilite = models.CharField(max_length=200, blank=False, null=False)
    nombre_enf= models.IntegerField(null=False, blank=False, default=0)
    nationalite = models.CharField(max_length=200, blank=False, null=False)
    telephone = models.CharField(max_length=12)
    profession = models.CharField(max_length=12, blank=False, null=False)
    diplome = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200)
    depart = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True)
    class Meta:
        abstract = True

    def __str__(self):
        return self.emails
      
class Employe(BaseEmploye):
    statut = models.CharField(max_length=200, blank=True, default='active')

class ArchiveEmploye(BaseEmploye):
    motif = models.CharField(max_length=200, blank=True)
    
class BaseContrat(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    poste = models.CharField(max_length=200, blank=False, null=False)
    types = models.CharField(max_length=200, null=False, blank=False)
    salaire = models.DecimalField(max_digits=15, decimal_places=2)
    dateSignature = models.DateField(auto_now_add = True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    avantages = models.TextField(null=True)
    obligations = models.TextField(null=True)
    resialiasion = models.TextField(null=True)

    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if self.types == 'CDI':
            self.date_fin = None
        super(BaseContrat, self).save(*args, **kwargs)

class Contrat(BaseContrat):
    statut = models.CharField(max_length=200, blank=True, default='encours')
    renouvelle = models.BooleanField(default=False)

class ContratArchive(BaseContrat):
    motif = models.CharField(max_length=100)
    date_archive = models.DateField(auto_now_add=True)

class Evenement(models.Model):

    choix_statut = [
        ('en attente', 'En attente'),
        ('passe', 'Passé'),
        ('annule', 'Annulé'),
        ('archivé', 'Archivé'),
    ]

    types = models.CharField(max_length=200,  blank=True)
    description = models.TextField()
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=100)
    initiateur = models.ForeignKey(Employe, related_name='initiateur', on_delete=models.CASCADE, null=True)
    participant = models.ManyToManyField(Employe, related_name='participant')
    statut = models.CharField(max_length=50, choices=choix_statut, default='en attente')


class Messagess(models.Model):

    choix_status = [
        ('en attente', 'En attente'),
        ('reçu', 'Reçu'),
        ('supprimer', 'Supprimer')
        ]
    obj = models.CharField(max_length=100)
    contenu = models.TextField()
    fichier = models.FileField(upload_to='media/', null =True, blank = True)
    emetteur = models.ForeignKey(Employe, on_delete= models.CASCADE, related_name='emetteur')
    recepteur = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='recepteur', null=True)
    statut = models.CharField(max_length=100, default='en attente', choices=choix_status)
    date_envoie = models.DateTimeField(auto_now_add=True)
   


class Notifications(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    intitule = models.CharField(max_length=100)
    description = models.TextField()
    date_notif  = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=100, default='en attente')



class Conge(models.Model):
    types = models.CharField(max_length=200)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='demandeur')
    motif = models.CharField(max_length=200)
    date_debut = models.DateField()
    date_fin = models.DateField()
    approbation = models.CharField(max_length=100, default='En attente')
    approbation1 = models.BooleanField(default=False)
    approbation2 = models.BooleanField(default=False)
    statut = models.CharField(max_length=100, blank=True, null=True)
    
   







