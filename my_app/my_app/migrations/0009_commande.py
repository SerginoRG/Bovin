# Generated by Django 5.1.7 on 2025-04-11 07:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0008_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id_commande', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.PositiveIntegerField()),
                ('date_commande', models.DateField(auto_now_add=True)),
                ('id_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='my_app.client')),
                ('id_produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commandes', to='my_app.produit')),
            ],
        ),
    ]
