# Generated by Django 5.0.6 on 2024-06-04 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAdministration', '0006_messagess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagess',
            name='date_envoie',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
