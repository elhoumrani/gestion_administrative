# Generated by Django 5.0.6 on 2024-07-06 09:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAdministration', '0015_conge_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='conge',
            name='depart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestionAdministration.departement'),
        ),
    ]
