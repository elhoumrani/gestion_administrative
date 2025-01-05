from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from comptes.form import UserForm
from comptes.models import Utlisateur
from gestionAdministration.models import Employe

# Create your views here.

def loginUser(request):
    erreur = ''
    if request.method == 'POST':
        usern = request.POST.get('username')
        pwd = request.POST.get('pwd')
        utlisateur = authenticate(request, username = usern, password=pwd)

        if utlisateur is not  None :
                login(request, utlisateur)
                if utlisateur.is_admin :
                    return redirect('acceuil')
             
                elif utlisateur.is_dg:
                    return redirect('acceuilDG')
                elif utlisateur.is_rh:
                    return redirect('acceuilRH')
                elif utlisateur.is_chef:
                    return redirect('acceuilChef')
                else :
                    return redirect('acceuilEmploye')
        else :
            erreur = 'Identifiants incorrects'
            context = {
                'msg': erreur}
            return render(request, "login.html", context)
    else:
        return render(request, "login.html")

def register(request):
    error = ''
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('loginUser')
        else:
            error ="Une erreur s'est produite"
            print(form.errors)

    return render(request, 'comptes.html', {'form': form, 'error': error})
       
   