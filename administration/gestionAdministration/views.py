from datetime import date, datetime, timedelta
import random
import string
from typing import Self
from django.db.models import Q
from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from comptes.models import Utlisateur
from gestionAdministration.models import ArchiveEmploye, Conge, ContratArchive, Departement, Employe, Contrat, Evenement,  Messagess, Notifications
from .form import CongeForm, ContratForm, DepartForm, EmployeForm, EventForm, MessageForm, MessageRForm

# Create your views here.


@login_required(login_url=reverse_lazy('loginUser'))
def acceuil(request) :
    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombreM = Messagess.objects.filter(req1).count()
    nombreN = Notifications.objects.filter(statut='en attente', employe=reccupereId).count()
    context = {"notif": nombreN, "msg":nombreM}
  
    return render(request, "index.html", context)

@login_required(login_url=reverse_lazy('loginUser'))
def acceuildg(request) :

    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombreM = Messagess.objects.filter(req1).count()
    nombreN = Notifications.objects.filter(statut='en attente', employe=reccupereId).count()
    context = {"notif": nombreN, "msg":nombreM}
    return render(request, "accueildg.html", context)

@login_required(login_url=reverse_lazy('loginUser'))
def acceuilrh(request) :
    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombreM = Messagess.objects.filter(req1).count()
    demandeR = Conge.objects.filter(approbation ='En attente', approbation1 = True).count()
    print(demandeR)
    nombreN = Notifications.objects.filter(statut='en attente', employe=reccupereId).count()
    context = {"notif": nombreN, "msg":nombreM, 'conge':demandeR}
    
    return render(request, "accueilrh.html", context)

@login_required(login_url=reverse_lazy('loginUser'))
def acceuilchef(request) :
    matricules = request.user.matricule
    emetteurs = Employe.objects.get( matricule = matricules)
    employe = Employe.objects.filter(depart_id = emetteurs.depart_id)

    for elt in employe:
            req =Q(approbation ='En attente') & Q(approbation1 = False) & Q(employe=elt)
            demandeC = Conge.objects.filter(req).count()

    print(demandeC)
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombreM = Messagess.objects.filter(req1).count()
    nombreN = Notifications.objects.filter(statut='en attente', employe=reccupereId).count()
    context = {"notif": nombreN, "msg":nombreM, 'conge':demandeC}

    
    return render(request, "accueilchef.html",  context)

@login_required(login_url=reverse_lazy('loginUser'))
def acceuilemploye(request) :
    matricules = request.user.matricule
    
    matricules = request.user.matricule
    #reccupereId = Employe.objects.get(matricule = matricules)
    #id = reccupereId.id
    #req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    #nombreM = Messagess.objects.filter(req1).count()
    #nombreN = Notifications.objects.filter(statut='en attente', employe=reccupereId).count()
    #context = {"notif": nombreN, "msg":nombreM}
   
    return render(request, "accueilE.html")

def generateMat():
        nom = "assali"
        random_digits = "".join(random.choices(string.digits, k=4))
        
        random_digits = f"{nom}{random_digits}"

        return random_digits
#Employe
#Ajouter un employé
@login_required(login_url=reverse_lazy('loginUser'))
def afficherAjout(request):

    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombreM = Messagess.objects.filter(req1).count()
    nombreN = Notifications.objects.filter(statut='en attente', employe=reccupereId).count()
    
    
    if request.method == 'POST':
        formulaire = EmployeForm(request.POST)
        
        if formulaire.is_valid():

            event = formulaire.save(commit=False) 
            event.matricule = generateMat()
            event.save()
            return redirect('listePersonnel')   
        else :  
            print(formulaire.errors)  
    else :
        formulaire = EmployeForm()
    if request.user.is_admin:
        return render(request, "enregistrer.html", {"context": formulaire, "notif": nombreN, "msg":nombreM} )
    elif request.user.is_rh:
        return render(request, "enregistrerRh.html", {"context": formulaire, "notif": nombreN, "msg":nombreM} )
    elif request.user.is_dg:
        return render(request, "enregistrerDg.html", {"context": formulaire, "notif": nombreN, "msg":nombreM} )

#Modifier
def modifierP(request, id):

    employe = Employe.objects.get(pk=id)
    form = EmployeForm(request.POST or None, instance=employe)
    if form.is_valid():
        form.save()
        print('ok')
        return redirect('listePersonnel')   
    else: 
        print('erreur')
        if request.user.is_admin: 
            return render(request, "modifierPersonnel.html", {"context": form} )
        elif request.user.is_dg:
            return render(request, "modifierPersonnelDg.html", {"context": form} )
        elif request.user.is_rh:
            return render(request, "modifierPersonnelRh.html", {"context": form} )

#Supprimer
def supprimerPersonnel(request, id):
    try:
        personnel = get_object_or_404(Employe, pk = id)
        
        nom = personnel.nom
        utilisateur = Utlisateur.objects.get(is_admin=True)
        admin = Employe.objects.get(matricule = utilisateur.matricule)
    except:
        return redirect('listePersonnel')  
    
    if request.method== 'POST':
        motifs = request.POST.get('motif') 
        #Archvier informations du personnel
        archive = ArchiveEmploye.objects.create(
            matricule = personnel.matricule,
            nom = personnel.nom,
            prenom = personnel.prenom,
            sexe = personnel.sexe,
            emails = personnel.emails,
            date_naissance = personnel.date_naissance,
            lieu_naissance = personnel.lieu_naissance,
            cni = personnel.cni,
            lieu_residence = personnel.lieu_residence,
            civilite = personnel.civilite,
            nombre_enf = personnel.nombre_enf,
            nationalite = personnel.nationalite,
            telephone = personnel.telephone,
            profession = personnel.profession,
            diplome = personnel.diplome,
            adresse = personnel.adresse,
            motif = motifs,
            depart = personnel.depart)
        notif = Notifications.objects.create(
                    employe=admin,
                    intitule= motifs,
                    description=f"L'employé {personnel.nom} {personnel.prenom} de matricule {personnel.matricule} ne figure plus dans la liste des employés")
        
        #enfin supprimer
        personnel.delete()
        return redirect('listePersonnel')
    if request.user.is_admin:
        return render(request, 'supprimer.html',{"context":nom})
    elif request.user.is_dg:
        return render(request, 'supprimerDg.html',{"context":nom})
    elif request.user.is_rh:
        return render(request, 'supprimerRh.html',{"context":nom})


def archivePersonnel(request):

    liste  = ArchiveEmploye.objects.all()
    
    context = {"liste":liste}

    return render(request, "archivesPersonnel.html", context)

#liste de personnel
def afficherListPersonnel(request):
    list = Employe.objects.order_by('-id').all()
    context = {"liste":list}
    matricules = request.user.matricule
    noms = Employe.objects.get( matricule = matricules)
    if noms is not None and request.user.is_chef:
        departement = noms.depart_id
        list = Employe.objects.order_by('-id').filter( depart_id = departement)
        return render(request, 'employeDepartement.html', {"liste": list} )
    elif request.user.is_rh:
        return render(request, "employeRh.html", context)
    elif request.user.is_dg:
        return render(request, "employeDg.html", context)
    else:
        return render(request, "employeAdmin.html", context)



#details d'un personnel
def detailsPersonnel(request, id):
    details = get_object_or_404(Employe, pk = id)
    message =''
    contrat = Contrat.objects.filter(employe_id=id)
    event = Evenement.objects.filter(participant=details)
    archiveC = ContratArchive.objects.filter(employe_id=id)
    if contrat is None or archiveC is None:
        message = "Aucune informations"
    context = {"details": details, 
               "message": message,
                 "contrat": contrat,
                  "event": event,
                   "archivec": archiveC }
    if request.user.is_admin:
        return render(request, 'details.html', context)
    elif request.user.is_rh:
        return render(request, 'detailsrh.html', context)
    elif request.user.is_dg:
        return render(request, 'detailsdg.html', context)

#afficher le details des archives d'un employe   
def detailsArchive(request, id):
    details = get_object_or_404(ArchiveEmploye, pk = id)
    message =''
    
    archiveC = ContratArchive.objects.filter(employe_id=id)
    if archiveC is None:
        message = "Aucune informations"
    context = {"details": details, 
               "message": message,
                   "archivec": archiveC }
    if request.user.is_admin:
        return render(request, 'details_archiveadmin.html', context)
    elif request.user.is_rh:
        return render(request, 'details_archiveRh.html', context)
    elif request.user.is_dg:
        return render(request, 'details_archiveDg.html', context)

#supprimer un employe de l'archive   
def supprimerArchive(request, id):
    try:
        archive = get_object_or_404(ArchiveEmploye, pk=id)
    except:
        return redirect('archivePersonnel')
    
    archive.delete()
    return redirect('archivePersonnel')

#Afficher tous les details d'un personnel
# ses infos , contrat, event assister
def detailsPerso(request):

    matricules = request.user.matricule

    details = get_object_or_404(Employe, matricule = matricules)
    contrat = Contrat.objects.filter(employe_id=details.id)
    event = Evenement.objects.filter(participant=details)
    
    
    context = {"details": details, "contrat":contrat, "event": event}

    return render(request, 'detailsPerso.html', context)

def listecompte(request):
    comptes = Utlisateur.objects.all()
    return render(request, 'listecomptes.html', {"liste":comptes})

def supprimerCompte(request, id):
    try:
        comptes = get_object_or_404(Utlisateur, pk=id)
    except:
        return redirect('listeCompte')
    comptes.delete()
    return redirect('listeCompte')
    
#Contrat 
#Ajouter contrat
def ajouterContrat(request):
    formulaire = ContratForm()
    error = ''
    msg = ''
  
    if request.method == 'POST':
        formulaire = ContratForm(request.POST)
        
        if formulaire.is_valid():
            
            forms = formulaire.save(commit=False)
            types = formulaire.cleaned_data['types']
            formulaire.save()
            return redirect('listeContrat')
        else:
            print(formulaire.errors)
    if request.user.is_admin:
        return render(request, 'ajouterContrat.html', {'form': formulaire, 'error':error})
    elif request.user.is_dg:
        return render(request, 'ajouterContratDg.html', {'form': formulaire, 'error':error})
    elif request.user.is_rh:
        return render(request, 'ajouterContratRh.html', {'form': formulaire, 'error':error})
        



#Afficher contrat
def listeContrat(request):

    try:
        utilisateur = Utlisateur.objects.get(is_rh=True)
        rh = Employe.objects.get(matricule = utilisateur.matricule)
    except:
        return redirect('archiveContrat')
    listes = Contrat.objects.filter(statut='encours')
    date_actu = date.today()
    for elt in listes:
            print(elt)
            if elt.types=='CDD':
                difference = elt.date_fin - date_actu
                com = timedelta(days=0)
                print("diff ",difference)
                print(com)
                if difference <= timedelta(days=0):
                
                    notif = Notifications.objects.create(
                        employe=rh,
                        intitule= "Fin de contrat",
                        description=f"L'employé {elt.employe.nom} {elt.employe.prenom} de matricule {elt.employe.matricule}, du departement {elt.employe.depart} occupant le poste de {elt.poste} son contrat signé le {elt.dateSignature} est arrivé à terme le {elt.date_fin}")
                    
                    notif = Notifications.objects.create(
                        employe=elt.employe,
                        intitule= "Fin de contrat",
                        description=f"{elt.employe.nom} {elt.employe.prenom}({elt.employe.matricule}) votre contrat signé le {elt.dateSignature} est arrivé à terme le {elt.date_fin}")
                    elt.statut ='expiré'
                    elt.save()
                else:
                    print(" ça n as pas marché")
            else:
                print("none")
                
    
    liste = Contrat.objects.order_by('-id').filter(statut='encours')
    listeE = Contrat.objects.order_by('-id').filter(statut='expiré')
    
    context = {"liste":liste, "listeE":listeE}
    if request.user.is_admin:
        return render(request, "listeContrat.html", context)
    elif request.user.is_dg:
         return render(request, "listeContratDg.html", context)
    elif request.user.is_rh:
         return render(request, "listeContratRh.html", context)

    
    
#modifier contrat
def modifierContrat(request, id):

    contrat = get_object_or_404(Contrat, pk = id)

    formulaire = ContratForm(request.POST or None, instance=contrat)
    if formulaire.is_valid():
        archive = ContratArchive.objects.create(
            employe_id = contrat.employe_id,
            poste = contrat.poste,
            types = contrat.types,
            salaire = contrat.salaire,
            dateSignature = contrat.dateSignature,
            date_fin = contrat.date_fin,
            avantages = contrat.avantages,
            obligations = contrat.obligations,
            resialiasion = contrat.resialiasion,
            motif = "modification du contrat"
            )

        formulaire.save()
        return redirect('listeContrat')   
    else: 
         if request.user.is_admin: 
            return render(request, "modifierContrat.html", {"form": formulaire} )
         elif request.user.is_dg:
             return render(request, "modifierContratDg.html", {"form": formulaire} )
         elif request.user.is_rh:
             return render(request, "modifierContratRh.html", {"form": formulaire} )

# en savoir plus sur un contrat
def detailsContrat(request, id):
    try:
        contrat = get_object_or_404(Contrat, pk=id)
    except:
        return('listeContrat')
    
    if request.user.is_admin:
        return render(request, 'detailsContratadmin.html', {'contrat':contrat})
    elif request.user.is_dg:
        return render(request, 'detailsContratdg.html', {'contrat':contrat})
    elif request.user.is_rh:
        return render(request, 'detailsContratrh.html', {'contrat':contrat})
#Supprimer un contrat
def supprimerContrat(request, id):
    contrat = get_object_or_404(Contrat, pk=id)
   
    if request.method== 'POST':
        motifs = request.POST.get('motif')
        archive = ContratArchive.objects.create(
            employe_id = contrat.employe_id,
            poste = contrat.poste,
            types = contrat.types,
            salaire = contrat.salaire,
            dateSignature = contrat.dateSignature,
            date_fin = contrat.date_fin,
            avantages = contrat.avantages,
            obligations = contrat.obligations,
            resialiasion = contrat.resialiasion,
            motif = motifs
            )
       
        contrat.delete()

        return redirect('listeContrat')
    if request.user.is_admin:
        return render(request, 'supprimerContrat.html')
    elif request.user.is_dg:
        return render(request, 'supprimerContratDg.html')
    elif request.user.is_rh:
        return render(request, 'supprimerContratRh.html')

#archiver contrat
def archiverContrat(request, id):
    try:
        contrat = get_object_or_404(Contrat, pk=id)
    except:
        return redirect('listeContrat')
    archive = ContratArchive.objects.create(
            employe_id = contrat.employe_id,
            poste = contrat.poste,
            types = contrat.types,
            salaire = contrat.salaire,
            dateSignature = contrat.dateSignature,
            date_fin = contrat.date_fin,
            avantages = contrat.avantages,
            obligations = contrat.obligations,
            resialiasion = contrat.resialiasion,
            motif = 'fin de contrat'
            )
    contrat.delete()
    return redirect('listeContrat')

#renouveler contrat
def renouvelerContrat(request, id):
    try:
        contrat = get_object_or_404(Contrat, pk=id)
    except:
        return redirect('listeContrat')
    
    #creer un archive du contrat à renouveler (garder l'historique du contrat expiré) 

    archive = ContratArchive.objects.create(
            employe_id = contrat.employe_id,
            poste = contrat.poste,
            types = contrat.types,
            salaire = contrat.salaire,
            dateSignature = contrat.dateSignature,
            date_fin = contrat.date_fin,
            avantages = contrat.avantages,
            obligations = contrat.obligations,
            resialiasion = contrat.resialiasion,
            motif = 'fin de contrat'
            )

    # obtenir la durrée du contrat 
    diff = contrat.date_fin -  contrat.dateSignature

    #assigner une nouvelle date de signature et date de fin
    contrat.dateSignature = date.today()
    contrat.date_fin = date.today() + diff

    contrat.statut = 'encours'
    contrat.renouvelle = True
    contrat.save()
    return redirect('listeContrat')

#archive contrat
def archivesContrat(request):
    
    liste = ContratArchive.objects.order_by('-id').all()
    context = { "liste": liste} 
    if request.user.is_admin:
        return render(request, "archiveContrat.html", context)
    elif request.user.is_dg:
        return render(request, "archiveContratDg.html", context)
    elif request.user.is_rh:
        return render(request, "archiveContratRh.html", context)


# evenement
def evenement(request):
    evenements = Evenement.objects.order_by('-id').all()
    matricules = request.user.matricule
    emetteurs = Employe.objects.get( matricule = matricules)
   
    for event in evenements:
        difference = event.date_fin.timestamp() - datetime.today().timestamp()
        com = timedelta(days=0)
        if event.date_fin.timestamp() <= datetime.today().timestamp():
            event.statut = 'Passé'
            event.save()
        else:
            print("non")

    req1 = Q(statut = 'Passé') & Q(initiateur = emetteurs)
    events= Evenement.objects.order_by('-id').filter(req1)
    evenement = Evenement.objects.order_by('-id').filter(statut = 'en attente', initiateur= emetteurs)
    context = {"eventA": evenement, "eventsP": events,}
    if request.user.is_admin:
        return render(request, 'evenementadmin.html', context )
    elif request.user.is_dg:
        return render(request, 'evenementdg.html', context )
    elif request.user.is_chef:
        return render(request, 'evenement.html', context )
    else:
        return render(request, 'evenementrh.html', context )

   
#ajouter event
def ajouterEvenement(request):

    formulaire = EventForm()
    error = ''
    if request.method == 'POST':
        formulaire = EventForm(request.POST)
        matricules = request.user.matricule
        emetteurs = Employe.objects.get( matricule = matricules)
       
        if formulaire.is_valid():
            event=formulaire.save()
            event.initiateur = emetteurs
            event.save()
            for employe_id in request.POST.getlist('participant'):
                participants =Employe.objects.get(id=employe_id)
                event.participant.add(participants)

            for participants in event.participant.all():

                msg = Messagess.objects.create(
                    obj = f"{event.types}",
                    contenu = f"Hello, nous avons le plaisir de vous inviter à prendre part de l'evenement( {event.description} ) qui aura lieu le {event.date_debut} dans {event.lieu} ",
                    emetteur= emetteurs,
                    recepteur = participants)
            return redirect('evenement')
        else: 
            
            error = 'Saisie incorrect. verifiez vos données'
    
    if request.user.is_admin:
        return render(request, "enregistrerEventadmin.html", {"form": formulaire, "error": error})
    elif request.user.is_dg:
        return render(request, "enregistrerEventdg.html", {"form": formulaire, "error": error})
    elif request.user.is_chef:
        return render(request, "enregistrerEvent.html", {"form": formulaire, "error": error})
    else:
        return render(request, "enregistrerEventrh.html", {"form": formulaire, "error": error})

    
#modifier event                


    
   

#supprimer event
def supprimerEvent(request, id):
    events = get_object_or_404(Evenement, pk=id)
    matricules = request.user.matricule
    emetteurs = Employe.objects.get( matricule = matricules)
        
    for elt in events.participant.all():
            msg = Messagess.objects.create(
                    obj = f"{events.types}",
                    contenu = f"Hello, nous venons vous informer que l'evenement( {events.description} ) qui aura lieu le {events.date_debut} dans {events.lieu} a été annulé. ",
                    emetteur= emetteurs,
                    recepteur = elt)
           
    events.delete()
    return redirect('evenement')
    
   

def nombreMsg(request):
    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombreM = Messagess.objects.filter(req1).count()
    nombreN = Notifications.objects.filter(statut='en attente')
    context = {"notif": nombreN, "msg":nombreM}
    
    return render(request, 'base.html', context )


#afficher message
def affichemsg(request):

    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombre = Messagess.objects.filter(req1).count()
    req2 = Q(statut='lus') & Q(recepteur = reccupereId)
    reccupereMsgRecu = Messagess.objects.order_by('-date_envoie').filter(req2)
    non_lus = Messagess.objects.order_by('-date_envoie').filter(req1)

    context ={"nombre": nombre,
              "recu":reccupereMsgRecu,
              "nonlus": non_lus}
    if request.user.is_chef:
        return render(request, 'messageChef.html', context)
    elif request.user.is_admin:
        return render(request, 'messageadmin.html',context)
    elif request.user.is_dg:
        return render(request, 'messagedg.html', context)
    elif request.user.is_rh:
        return render(request, 'messagerh.html', context)
    else:
        return render(request, 'message.html', context)
    
def affichenotif(request):

    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombreM = Messagess.objects.filter(req1).count()
    nombreN = Notifications.objects.filter(statut='en attente', employe=reccupereId).count()
    req1=Q(employe = reccupereId) & Q(statut='en attente')
    req2 = Q(statut='lus') & Q(employe = reccupereId)
    notifs = Notifications.objects.order_by('-date_notif').filter(req2)
    non_lus = Notifications.objects.order_by('-date_notif').filter(req1)

    context ={"msg": nombreM,
              "notif":nombreN,
              "recu":notifs,
              "nonlus": non_lus}
    if request.user.is_chef:
        return render(request, 'notificationchef.html', context)
    elif request.user.is_admin:
        return render(request, 'notificationadmin.html',context)
    elif request.user.is_dg:
        return render(request, 'notificationdg.html', context)
    elif request.user.is_rh:
        return render(request, 'notificationrh.html', context)
    else:
        return render(request, 'notificationemploye.html', context)

def lireNotif(request, id):

    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    req1=Q(recepteur = reccupereId) & Q(statut='en attente')
    nombreM = Messagess.objects.filter(req1).count()
    nombreN = Notifications.objects.filter(statut='en attente', employe=reccupereId).count()

    try:
        notifs = get_object_or_404(Notifications, pk=id)
    except:
        return redirect('notifcations')
    
    if notifs.statut =='en attente':
        notifs.statut='lus'
        notifs.save()
    context = {"notifs":notifs, "msg":nombreM, "notif":nombreN}

    if request.user.is_admin:
        return render(request, 'lirenotifadmin.html', context)
    elif request.user.is_dg:
        return render(request, 'lirenotifdg.html', context)
    elif request.user.is_rh:
        return render(request, 'lirenotifrh.html', context)
    elif request.user.is_chef:
        return render(request, 'lirenotifchef.html', context)
    else:
        return render(request, 'lirenotifemploye.html', context)

def supprimerNotif(request, id):
        try:
            notifs = get_object_or_404(Notifications, pk=id)
        except:
            return redirect('notifcations')
        notifs.delete()
        return redirect('notifcations')

#archives message
def afficheArchivemsg(request):
    pass


def sendedmessage(request):
    msg = Messagess.objects.all().order_by('-date_envoie')
    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    nombre = Messagess.objects.filter(emetteur = reccupereId).count()
    reccupereMsgEnv = Messagess.objects.order_by('-date_envoie').filter(emetteur = reccupereId)
    if request.user.is_admin:
        return render(request, 'sendMessageadmin.html', {"nombre": nombre, "envoye": reccupereMsgEnv})
    elif request.user.is_chef:
        return render(request, 'sendMessageChef.html', {"nombre": nombre, "envoye": reccupereMsgEnv})
    elif request.user.is_dg:
        return render(request, 'sendMessagedg.html', {"nombre": nombre, "envoye": reccupereMsgEnv})
    elif request.user.is_rh:
        return render(request, 'sendMessagerh.html', {"nombre": nombre, "envoye": reccupereMsgEnv})
    else:
        return render(request, 'sendMessage.html', {"nombre": nombre, "envoye": reccupereMsgEnv})
    

def liremessage(request, id):

    try:
        msg = get_object_or_404(Messagess, pk=id)
        
    except:
        return redirect('message_msg')
    
    recepteur = Employe.objects.get(id = msg.recepteur_id)
    emetteur = Employe.objects.get(id = msg.emetteur_id )
    if msg.statut =='en attente':
            msg.statut='lus'
            msg.save()
    if request.user.is_admin:
        return render(request, 'readMessageadmin.html', {"message": msg, "recepteur": recepteur, "emetteur": emetteur})
    elif request.user.is_chef:
        return render(request, 'readMessagechef.html', {"message": msg, "recepteur": recepteur, "emetteur": emetteur})
    elif request.user.is_dg:
        return render(request, 'readMessagedg.html', {"message": msg, "recepteur": recepteur, "emetteur": emetteur})
    elif request.user.is_rh:
        return render(request, 'readMessagerh.html', {"message": msg, "recepteur": recepteur, "emetteur": emetteur})
    else:
        return render(request, 'readMessage.html', {"message": msg, "recepteur": recepteur, "emetteur": emetteur}) 
        

def lireArchivemessage(request, id):
    pass
    
def supprimerArchiveMessage(request, id):
   pass

def envoyermessage(request):
    form = MessageForm()
    matricules = request.user.matricule
    emetteurs = Employe.objects.get( matricule = matricules)
    error = ''
    if request.method == 'POST':

        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            messagess = form.save(commit=False)
            messagess.emetteur = emetteurs
            messagess.save()
            return redirect('message_msg') 
        else:
            error = "une erreur s'est produite "
            print(form.errors)
            return render(request, "envoyerMessage.html", {"form":form, "msg": error})

    if request.user.is_admin:
        return render(request, "envoyerMessageadmin.html", {"form":form})
    elif request.user.is_employe:
        return render(request, "envoyerMessage.html", {"form":form})
    elif request.user.is_chef:
        return render(request, "envoyerMessagechef.html", {"form":form})
    elif request.user.is_dg:
        return render(request, "envoyerMessagedg.html", {"form":form})
    else:
        return render(request, "envoyerMessagerh.html", {"form":form})

def repondreMessage(request, id):

    try:
        msg = get_object_or_404(Messagess, pk=id)
    except:
        return redirect('message_msg')

    form = MessageForm()
    matricules = request.user.matricule
    print(msg.recepteur)
    emetteurs = Employe.objects.get( matricule = matricules)
    error = ''
    if request.method == 'POST':

        form = MessageRForm(request.POST, request.FILES)
        if form.is_valid():
            messagess = form.save(commit=False)
            messagess.emetteur = emetteurs
            messagess.save()
            messagess.recepteur = msg.emetteur
            messagess.save()
            return redirect('message_msg') 
        else:
            error = "une erreur s'est produite"
            print(form.errors)
            if request.user.is_admin:
                return render(request, "repondreMessageadmin.html", {"form":form})
            elif request.user.is_employe:
                return render(request, "repondreMessage.html", {"form":form})
            elif request.user.is_chef:
                return render(request, "repondreMessagechef.html", {"form":form})
            elif request.user.is_dg:
                return render(request, "repondreMessagedg.html", {"form":form})
            else:
                return render(request, "repondreMessagerh.html", {"form":form})

    if request.user.is_admin:
        return render(request, "repondreMessageadmin.html", {"form":form})
    elif request.user.is_employe:
        return render(request, "repondreMessage.html", {"form":form})
    elif request.user.is_chef:
        return render(request, "repondreMessagechef.html", {"form":form})
    elif request.user.is_dg:
        return render(request, "repondreMessagedg.html", {"form":form})
    else:
        return render(request, "repondreMessagerh.html", {"form":form})

    

def supprimerMsg(request, id):

    try:
        msg = get_object_or_404(Messagess, pk=id)
    except:
        return redirect('message_msg')
    
    matricules = request.user.matricule
    reccupereId = Employe.objects.get(matricule = matricules)
    id = reccupereId.id
    nombre = Messagess.objects.filter(recepteur = reccupereId).count()
    reccupereMsgRecu = Messagess.objects.order_by('-date_envoie').filter(recepteur = reccupereId)

    
    msg.delete()

    if request.user.is_chef:
        return render(request, 'messageChef.html', {"nombre": nombre,"recu":reccupereMsgRecu})
    elif request.user.is_admin:
        return render(request, 'messageadmin.html', {"nombre": nombre,"recu":reccupereMsgRecu})
    elif request.user.is_dg:
        return render(request, 'messagedg.html', {"nombre": nombre,"recu":reccupereMsgRecu})
    elif request.user.is_rh:
        return render(request, 'messagerh.html', {"nombre": nombre,"recu":reccupereMsgRecu})
    else:
        return render(request, 'message.html', {"nombre": nombre,"recu":reccupereMsgRecu})

    


#departement
def departement_views(request):

    depart = Departement.objects.all().order_by('-id')

    context = {"depart": depart}

    if request.user.is_dg:
        return render(request, 'departement.html', context)
    elif request.user.is_admin:
        return render(request, 'departementadmin.html', context)


#Ajout depart
def ajouterDepart(request):
    formulaire = DepartForm()
    erreur = ''
    if request.method == 'POST':

        formulaire = DepartForm(request.POST)

        if formulaire.is_valid():
             formulaire.save()
             return redirect('departement')
        
        else: 
            erreur = "Une erreur s'est produite"
            return render(request, 'ajouterDepart.html', {"form": formulaire,'error': erreur})
        
    if request.user.is_admin:  
        return render(request, 'ajouterDepart.html', {"form": formulaire} )
    elif request.user.is_dg:
        return render(request, 'ajouterDepartdg.html', {"form": formulaire} )

#Modifier Depart
def modifierDepartement(request, id):

    depart = Departement.objects.get(pk = id)
    formulaire = DepartForm(request.POST or None, instance=depart)
    if formulaire.is_valid():
        formulaire.save()
        return redirect('departement')
    else :
        if request.user.is_admin:
            return render(request, 'modifierDepartementadmin.html', {'form': formulaire})
        elif request.user.is_dg:
            return render(request, 'modifierDepartement.html', {'form': formulaire})

#demande congé
def demandeConge(request):

    formulaire = CongeForm()

    matricules = request.user.matricule
    emetteurs = Employe.objects.get( matricule = matricules)
    employe = Employe.objects.filter(depart = emetteurs.depart_id)

    error = ''
    if request.method == 'POST':
        formulaire = CongeForm(request.POST)
        print(emetteurs.id)
        if formulaire.is_valid():
            requete=formulaire.save(commit=False)
            if request.user.is_chef or request.user.is_rh or request.user.is_dg:
                requete.employe = emetteurs
                requete.approbation1 = True
                requete.save()
                return redirect('liste_congé')
                print("cool")
            
            else:
                requete.employe = emetteurs
                requete.save()
                return redirect('liste_congé')
                print("cool")

        
        else:
            print(formulaire.errors)
            error = 'error',formulaire.errors
            print(formulaire.errors)
            if request.user.is_chef:
                return render(request, 'demandeChef.html',  {'error': error, 'form': formulaire})
            elif request.user.is_rh:
                return render(request, 'demandarh.html' , {'error': error, 'form': formulaire})
            elif request.user.is_dg:
                return render(request, 'demandedg.html',  {'error': error, 'form': formulaire})
            else:
                return render(request, 'demandeEmploye.html', {'error': error, 'form': formulaire})
        
    else:
        if request.user.is_chef:
            return render(request, 'demandeChef.html',{'form': formulaire})
        elif request.user.is_rh:
            return render(request, 'demanderh.html', {'form': formulaire})
        elif request.user.is_dg:
            return render(request, 'demandedg.html', {'form': formulaire})
        else:
            return render(request, 'demandeEmploye.html', {'form': formulaire})
        

def afficherConge(request):

    matricules = request.user.matricule
    emetteurs = Employe.objects.get( matricule = matricules)
    employe = Employe.objects.filter(depart_id = emetteurs.depart_id)

    congeA = Conge.objects.filter(approbation ='Approuvé')
    for elt in congeA:
        
        diff = date.today() - elt.date_fin
       
        if elt.date_debut == date.today() and date.today() < elt.date_fin :
            elt.statut ='en cours'
            elt.save()
            
        elif  elt.date_fin <= date.today():
            elt.statut ='epuisé'
            elt.save()
            

    congeE = Conge.objects.filter(statut ='en cours')
    conge = Conge.objects.filter(statut ='epuisé')
    context = {'congeEc': congeE, 'congeEp':conge}

    if request.user.is_admin:
        return render(request, 'afficherCongeadmin.html', context)
    elif request.user.is_dg:
        return render(request, 'afficherCongedg.html', context)
    elif request.user.is_rh:
        return render(request, 'afficherCongerh.html', context)
    elif request.user.is_chef:
        for elt in employe:
            req =Q(statut ='en cours') & Q(employe=elt)
            req1 =Q(statut ='epuisé') & Q(employe=elt)
            congeEp = Conge.objects.filter(req1)
            congeEn = Conge.objects.filter(req)
        return render(request, 'afficherCongechef.html', {"congeEp": congeEp, "congeEn":congeEn})
    elif request.user.is_employe:
        employes = Employe.objects.get(matricule = request.user.matricule)
        
        rq =Q(statut ='en cours') & Q(employe_id=employes.id)
        rq1 =Q(statut ='epuisé') & Q(employe_id=employes.id)
        congep = Conge.objects.filter(rq1)
        congen = Conge.objects.filter(rq)
        
        return render(request, 'afficherCongeEmploye.html', {"congep": congep, "congen":congen})


def listeDemande(request):
    
    matricules = request.user.matricule
    emetteurs = Employe.objects.get( matricule = matricules)
    employe = Employe.objects.filter(depart_id = emetteurs.depart_id)
    print(employe)


    if request.user.is_chef:
        for elt in employe:
            req =Q(approbation ='En attente') & Q(approbation1 = False) & Q(employe=elt)
            demandeC = Conge.objects.order_by('-id').filter(req)
            return render(request, 'listeDemandechef.html',{'forms': demandeC} )

    elif request.user.is_rh:
        demandeR = Conge.objects.order_by("-id").filter(approbation ='En attente', approbation1 = True)
        return render(request, 'listeDemanderh.html',{'form': demandeR})

  
def detailsDemande(request, id):
    
    details_c = Conge.objects.get(id = id)
    demandeR = Conge.objects.filter(approbation = 'refusé', employe_id = details_c.employe_id)
    demandeA= Conge.objects.filter(approbation = 'Approuvé', employe_id = details_c.employe_id)
    print(demandeR)
    context ={
            'detail': details_c,
            'demandeR': demandeR,
            'demandeA': demandeA,}
    if request.user.is_rh:
        return render(request, 'detailsDemandeRh.html', context)
    elif request.user.is_chef:
        return render(request, 'detailsDemandechef.html', context)
    

def refuserConge(request, id):
    demande = Conge.objects.get(id=id)
    mat = request.user.matricule
    emetteur = Employe.objects.get(matricule = mat)
    recepteur = Employe.objects.get(id=demande.employe_id)
    
    if request.method =='POST':
        comment = request.POST.get('comment')
        msg = Messagess.objects.create(
                    obj = f" Refus de demande de congé ",
                    contenu = f"Hello, nous avons le regret de vous informer que votre demande de congé pour la periode du {demande.date_debut} au {demande.date_fin}  n'a pas été  accepté. {comment} ",
                    emetteur= emetteur,
                    recepteur = recepteur)
        if request.user.is_rh:
        
            demande.approbation2 = False
            demande.approbation = 'refusé'
            demande.save()
            return redirect('liste_demande_Congé')
    
        elif request.user.is_chef:
            demande.approbation1 = False
            demande.approbation2 = False
            demande.approbation = 'refusé'
            demande.save()
            return redirect('liste_demande_Congé')

    else:
        if request.user.is_rh:
            return render(request, 'refusDemandeRh.html')
        elif request.user.is_chef:
            return render(request, 'refusDemandechef.html')

def accorderConge(request, id):
    demande = Conge.objects.get(id=id)
    mat = request.user.matricule
    emetteur = Employe.objects.get(matricule = mat)
    recepteur = Employe.objects.get(id=demande.employe_id)
    
   
    if request.user.is_rh:

        msg = Messagess.objects.create(
                    obj = f" Approbation de demande de congé ",
                    contenu = f"Hello, nous avons le plaisir de vous informer que votre demande de congé pour la periode du {demande.date_debut} au {demande.date_fin}  a été accepté. La date de reprise est juste deux jours aprés la date de fin de votre congé",
                    emetteur= emetteur,
                    recepteur = recepteur)
        
        demande.approbation2 = True
        demande.approbation = 'Approuvé'
        demande.save()
        return redirect('liste_demande_Congé')
    
    elif request.user.is_chef:
        msg = Messagess.objects.create(
                    obj = f" Suivi de demande de congé ",
                    contenu = f"Hello, nous avons le plaisir de vous informer que votre demande de congé pour la periode du {demande.date_debut} au {demande.date_fin}  a été envoyé à la direction de RH",
                    emetteur= emetteur,
                    recepteur = recepteur)
        demande.approbation1 = True
        demande.approbation2 = False
        demande.approbation = 'En attente'
        demande.save()
        return redirect('liste_demande_Congé')

    

    




        






    