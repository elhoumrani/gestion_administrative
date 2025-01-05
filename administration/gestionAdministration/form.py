
from django import forms
from django.forms import DateInput, NumberInput, TextInput, DateTimeInput, EmailInput, Form, ModelForm

from comptes.models import Utlisateur
from .models import Conge, Contrat, Departement, Employe, Evenement, Messagess


SEXE = (
    ('M', 'M'),
    ('F', 'F'),)

Civilite = (
    ('Celibataire', 'Celibataire'),
    ('Merié(e)', 'Marié(e)'),)
class EmployeForm(forms.ModelForm):
    sexe = forms.ChoiceField(
        choices=SEXE,
        label='Sexe',
        required=True)
    civilite = forms.ChoiceField(
        choices=Civilite,
        label='Civilité',
        required=True)
    

    class Meta:
        model = Employe
        fields = ['nom', 'prenom','sexe', 'emails',
                   'date_naissance', 'lieu_naissance',
                    'cni', 'lieu_residence', 
                    'civilite', 'nombre_enf',
                     'nationalite', 'telephone', 'profession',
                     'diplome', 'adresse',
                     'depart']

        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),}
        
class DepartForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom', 'responsable'] 


CONTRAT_TYPE = (
    ('CDD', 'CDD'),
    ('CDI', 'CDI'),)

class ContratForm(forms.ModelForm):
    types = forms.ChoiceField(
        choices=CONTRAT_TYPE,
        label='Type de contrat',
        required=True)
    
    class Meta:
        model = Contrat
  
        fields= [
            'employe', 'poste','types', 'salaire','date_fin', 'avantages', 
            'obligations', 'resialiasion',
            ]
        widgets = {
            
            "avantages": forms.Textarea(attrs={'rows': 3}),
            "obligations": forms.Textarea(attrs={'rows': 3}),
            "resialiasion": forms.Textarea(attrs={'rows': 3}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            }
        def __init__(self, *args, **kwargs):
            super(ContratForm, self).__init__(*args, **kwargs)
            self.fields['date_fin'].widget.attrs['readonly'] = False

            def clean(self):
                cleaned_data = super().clean()
                types = cleaned_data.get('types')
                if types == "CDI":
                    self.fields['date_fin'].widget.attrs['readonly'] = True
                    self.fields['date_fin'].required = False
                    cleaned_data['date_fin'] = None
                    return cleaned_data

        
class EventForm(forms.ModelForm):
 
    class Meta:
        model = Evenement
        fields = [
                 'types','description', 'date_debut', 'date_fin', 'lieu', 'participant']
        widgets = {
            "date_debut": DateTimeInput(attrs={"class": "datetimepicker", "type":"datetime-local"}),
            "date_fin": DateTimeInput(attrs={"class": "datetimepicker", "type":"datetime-local"}),
            "description": forms.Textarea(attrs={'rows': 3}),
            "participant" : forms.CheckboxSelectMultiple()

            }
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Messagess
        fields = [
            'obj', 'contenu','recepteur', 'fichier']
        
        def __init__(self, user =None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if user:
                self.fields['recepteur'].queryset = Utlisateur.objects.exclude(matricule = user.matricule) 

class MessageRForm(forms.ModelForm):
    class Meta:
        model = Messagess
        fields = [
            'obj', 'contenu', 'fichier']
        
        

CONGE_TYPE = (
    ('Maladie', 'Maladie'),
    ('Maternité', 'Maternité'),
    ('Annuel', 'Annuel'),)
class CongeForm(forms.ModelForm):
    types = forms.ChoiceField(
        choices=CONGE_TYPE,
        label='Type de congé',
        required=True)
    class Meta:
        model = Conge 
        fields = [
                'types', 'motif', 'date_debut', 'date_fin']
        
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'})}