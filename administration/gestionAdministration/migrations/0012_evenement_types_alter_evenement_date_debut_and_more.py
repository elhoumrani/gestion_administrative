# Generated by Django 5.0.6 on 2024-07-03 21:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAdministration', '0011_contrat_renouvelle'),
    ]

    operations = [
        migrations.AddField(
            model_name='evenement',
            name='types',
            field=models.CharField(blank=True, default='Reunion', max_length=200),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='date_debut',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='date_fin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='description',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='ArchiveEmploye',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=200, unique=True)),
                ('nom', models.CharField(max_length=25)),
                ('prenom', models.CharField(max_length=15)),
                ('sexe', models.CharField(max_length=2)),
                ('emails', models.EmailField(max_length=254)),
                ('date_naissance', models.DateField(blank=True)),
                ('lieu_naissance', models.CharField(max_length=200)),
                ('cni', models.CharField(max_length=14)),
                ('lieu_residence', models.CharField(max_length=150)),
                ('civilite', models.CharField(max_length=200)),
                ('nombre_enf', models.IntegerField(default=0)),
                ('nationalite', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=12)),
                ('profession', models.CharField(max_length=12)),
                ('diplome', models.CharField(max_length=200)),
                ('adresse', models.CharField(max_length=200)),
                ('motif', models.CharField(blank=True, max_length=200)),
                ('depart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestionAdministration.departement')),
            ],
        ),
    ]
