# Generated by Django 5.0.6 on 2024-07-09 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionAdministration', '0020_notifications_employe_alter_notifications_date_notif_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='statut',
            field=models.CharField(default='en attente', max_length=100),
        ),
    ]
