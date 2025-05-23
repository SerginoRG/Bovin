# Generated by Django 5.1.7 on 2025-04-26 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0016_reproduction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100, verbose_name='Nom complet')),
                ('identifiant', models.CharField(max_length=50, unique=True, verbose_name="Nom d'utilisateur")),
                ('role', models.CharField(choices=[('user', 'Utilisateur standard'), ('admin', 'Administrateur')], max_length=20, verbose_name='Rôle')),
                ('mot_de_passe', models.CharField(max_length=128, verbose_name='Mot de passe')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='Dernière modification')),
                ('est_actif', models.BooleanField(default=True, verbose_name='Compte actif')),
            ],
            options={
                'verbose_name': 'Compte utilisateur',
                'verbose_name_plural': 'Comptes utilisateurs',
                'db_table': 'auth_logins',
                'ordering': ['-date_creation'],
            },
        ),
    ]
