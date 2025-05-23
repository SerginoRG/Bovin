# Generated by Django 5.1.7 on 2025-04-15 11:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0014_vaccin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Traitement',
            fields=[
                ('id_traitement', models.AutoField(primary_key=True, serialize=False)),
                ('medicament', models.CharField(max_length=50)),
                ('dose', models.CharField(max_length=20)),
                ('date_traitement', models.DateField()),
                ('id_individu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traitements', to='my_app.individu')),
                ('id_maladie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traitements', to='my_app.maladie')),
                ('id_veterinaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traitements', to='my_app.veterinaire')),
            ],
        ),
    ]
