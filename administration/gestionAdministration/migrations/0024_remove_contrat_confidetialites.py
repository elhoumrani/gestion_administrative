# Generated by Django 5.0.6 on 2024-07-09 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAdministration', '0023_rename_confidetialite_contrat_confidetialites_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrat',
            name='confidetialites',
        ),
    ]
