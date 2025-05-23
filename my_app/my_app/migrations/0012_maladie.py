# Generated by Django 5.1.7 on 2025-04-14 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0011_paiement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maladie',
            fields=[
                ('id_maladie', models.AutoField(primary_key=True, serialize=False)),
                ('nom_maladie', models.CharField(max_length=50, verbose_name='Nom de la maladie')),
                ('description_maladie', models.TextField(verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Maladie',
                'verbose_name_plural': 'Maladies',
            },
        ),
    ]
