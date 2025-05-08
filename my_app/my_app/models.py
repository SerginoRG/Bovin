from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Troupeau(models.Model):
    id_troupeau = models.CharField(max_length=20, primary_key=True)
    nom = models.CharField(max_length=100)
    race = models.CharField(max_length=50)
    date_creation = models.DateField()
    TYPE_CHOICES = [
        ('laitier', 'Laitier'),
        ('viande', 'Viande'),
        ('mixte', 'Mixte'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.nom
    
class Aliment(models.Model):
    id_aliment = models.CharField(max_length=20, primary_key=True)
    nom_aliment = models.CharField(max_length=100)
    type_aliment = models.CharField(max_length=50)
    stock_aliment = models.IntegerField()

    def __str__(self):
        return self.nom_aliment


class StockAliment(models.Model):
    id_stock = models.AutoField(primary_key=True)
    id_aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE, related_name='stocks')
    fournisseur_aliment = models.CharField(max_length=50)
    stock_entree = models.IntegerField()
    date_reception = models.DateField()
    prix_aliment = models.IntegerField()

    def __str__(self):
        return f"Stock de {self.id_aliment.nom_aliment} - {self.date_reception}"

class Ration(models.Model):
    id_ration = models.AutoField(primary_key=True)  
    id_troupeau = models.ForeignKey(Troupeau, on_delete=models.CASCADE, related_name='rations')
    id_aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE, related_name='rations')
    quantite_aliment = models.PositiveIntegerField()
    date_ration = models.DateField()

    def __str__(self):
        return f"Ration de {self.id_troupeau.nom} - {self.date_ration}"



class Individu(models.Model):
    id_individu = models.AutoField(primary_key=True)
    id_troupeau = models.ForeignKey(Troupeau, on_delete=models.CASCADE, related_name='individus')
    numero_identification = models.CharField(max_length=50, unique=True)
    SEXE_CHOICES = [
        ('male', 'Mâle'),
        ('femelle', 'Femelle'),
    ]
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    poids = models.DecimalField(max_digits=6, decimal_places=2)  # Changé de ImageField à DecimalField
    ETAT_SANTE_CHOICES = [
        ('bon', 'Bon état'),
        ('malade', 'Malade'),
        ('traitement', 'En traitement'),
    ]
    etat_sante = models.CharField(max_length=10, choices=ETAT_SANTE_CHOICES)
    VACCIN_CHOICES = [
        ('oui', 'Oui'),
        ('non', 'Non'),
    ]
    vaccins = models.CharField(max_length=3, choices=VACCIN_CHOICES)
    description = models.TextField(max_length=500, blank=True)  # Corrigé le nom et augmenté la longueur

    def __str__(self):
        return f"Individu {self.numero_identification} ({self.id_troupeau.nom})"
    

class Produit(models.Model):
    id_produit = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100, unique=True)
    UNITE_MESURE = [
        ('litres', 'Litres'),
        ('kg', 'Kilogrammes'),
        ('mga', 'MGA'),
    ]
    unite_mesure = models.CharField(max_length=10, choices=UNITE_MESURE)
    date_expiration = models.DateField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)  # Corrigé le nom et augmenté la précision
    
    def __str__(self):
        return f"{self.nom} ({self.get_unite_mesure_display()}) - {self.prix_unitaire} MGA"
    

class Production(models.Model):
    id_production = models.AutoField(primary_key=True)
    id_individu = models.ForeignKey(Individu, on_delete=models.CASCADE, related_name='productions')
    id_produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='productions')
    date_production = models.DateField()
    quantite = models.IntegerField()
    poids_carcasse = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"Production #{self.id_production} - {self.id_produit.nom} ({self.date_production})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        from datetime import date
        from dateutil.relativedelta import relativedelta
        
        # Vérification des conditions spécifiques
        if self.id_produit.unite_mesure == 'litres':
            # Pour les produits en litres (lait)
            if self.id_individu.etat_sante in ['malade', 'traitement']:
                raise ValidationError("Un individu malade ou en traitement ne peut pas produire du lait")
            
            age = relativedelta(date.today(), self.id_individu.date_naissance).years
            if age < 2:
                raise ValidationError("Un individu de moins de 2 ans ne peut pas produire du lait")
                
            if self.id_individu.sexe == 'male':
                raise ValidationError("Un individu mâle ne peut pas produire du lait")
        
        elif self.id_produit.unite_mesure == 'kg':
            # Pour les produits en kg (viande)
            if self.id_individu.etat_sante not in ['bon','malade', 'traitement']:
                raise ValidationError("Seuls les individus bon ou malades ou en traitement peuvent être transformés en viande")


from django.core.validators import RegexValidator

class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    nom_client = models.CharField(max_length=100)
    prenom_client = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='Le numéro doit contenir 10 chiffres'
            )
        ]
    )
    email_client = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.nom_client} {self.prenom_client}"

    def clean(self):
        # Nettoyer le numéro de téléphone (supprimer les espaces, etc.)
        self.telephone = ''.join(filter(str.isdigit, self.telephone))
        if len(self.telephone) != 10:
            raise ValidationError("Le numéro de téléphone doit contenir 10 chiffres")


class Commande(models.Model):
    id_commande = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='commandes')
    id_produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='commandes')
    quantite = models.IntegerField()
    date_commande = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.id_commande} pour {self.id_client}"


from django.core.exceptions import ValidationError
from datetime import date

class Commande(models.Model):
    id_commande = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='commandes')
    id_produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='commandes')
    quantite = models.PositiveIntegerField()
    date_commande = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.id_commande} - {self.id_client} ({self.montant_total} MGA)"

    def annuler_commande(self):
        """Réintègre les quantités commandées dans le stock"""
        if self.id_produit.unite_mesure == 'litres':
            productions = Production.objects.filter(
                id_produit=self.id_produit
            ).order_by('-date_production')
            
            quantite_a_reintegrer = self.quantite
            
            for production in productions:
                if quantite_a_reintegrer <= 0:
                    break
                    
                production.quantite += quantite_a_reintegrer
                production.save()
                quantite_a_reintegrer = 0
                
        elif self.id_produit.unite_mesure == 'kg':
            productions = Production.objects.filter(
                id_produit=self.id_produit
            ).order_by('-date_production')
            
            poids_a_reintegrer = self.quantite
            
            for production in productions:
                if poids_a_reintegrer <= 0:
                    break
                    
                production.poids_carcasse += poids_a_reintegrer
                production.save()
                poids_a_reintegrer = 0

    @property
    def montant_total(self):
        return self.quantite * self.id_produit.prix_unitaire

    def clean(self):
        # Vérifier si le produit est expiré
        if self.id_produit.date_expiration < date.today():
            raise ValidationError("Ce produit est expiré, commande impossible")
        
        # Vérification du stock selon le type de produit
        if self.id_produit.unite_mesure == 'litres':
            total_stock = Production.objects.filter(
                id_produit=self.id_produit
            ).aggregate(total=models.Sum('quantite'))['total'] or 0
            
            if total_stock < self.quantite:
                raise ValidationError(f"Stock insuffisant en litres. Il manque {self.quantite - total_stock} litres")
                
        elif self.id_produit.unite_mesure == 'kg':
            total_stock = Production.objects.filter(
                id_produit=self.id_produit
            ).aggregate(total=models.Sum('poids_carcasse'))['total'] or 0
            
            if total_stock < self.quantite:
                raise ValidationError(f"Stock insuffisant en kg. Il manque {self.quantite - total_stock} kg")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.deduire_stock()
    
    def deduire_stock(self):
        """Déduit la quantité commandée du stock disponible"""
        if self.id_produit.unite_mesure == 'litres':
            productions = Production.objects.filter(
                id_produit=self.id_produit,
                quantite__gt=0
            ).order_by('date_production')
            
            quantite_a_deduire = self.quantite
            
            for production in productions:
                if quantite_a_deduire <= 0:
                    break
                    
                if production.quantite >= quantite_a_deduire:
                    production.quantite -= quantite_a_deduire
                    production.save()
                    quantite_a_deduire = 0
                else:
                    quantite_a_deduire -= production.quantite
                    production.quantite = 0
                    production.save()
                    
        elif self.id_produit.unite_mesure == 'kg':
            productions = Production.objects.filter(
                id_produit=self.id_produit,
                poids_carcasse__gt=0
            ).order_by('date_production')
            
            poids_a_deduire = self.quantite
            
            for production in productions:
                if poids_a_deduire <= 0:
                    break
                    
                if production.poids_carcasse >= poids_a_deduire:
                    production.poids_carcasse -= poids_a_deduire
                    production.save()
                    poids_a_deduire = 0
                else:
                    poids_a_deduire -= production.poids_carcasse
                    production.poids_carcasse = 0
                    production.save()


class CommandeDetail(models.Model):
    id_commande = models.AutoField(primary_key=True)
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='commandesdetail')
    date_commande = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"CommandeDetail {self.id_commande} - {self.id_client}"


class Paiement(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('cheque', 'Chèque'),
        ('especes', 'Espèces'),
        ('carte', 'Carte bancaire'),
        ('virement', 'Virement bancaire'),
    ]
    
    id_paiement = models.AutoField(primary_key=True)
    id_commandeDetail = models.ForeignKey(CommandeDetail, on_delete=models.CASCADE, related_name='paiements')
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES)
    date_paiement = models.DateField()
    

    def __str__(self):
        return f"Paiement #{self.id_paiement} - {self.get_mode_paiement_display()} MGA)"

    def clean(self):
        # Vérifier que la date de paiement n'est pas dans le futur
        if self.date_paiement > date.today():
            raise ValidationError("La date de paiement ne peut pas être dans le futur")
        
      

class Maladie(models.Model):
    id_maladie = models.AutoField(primary_key=True)
    nom_maladie = models.CharField(max_length=50, verbose_name="Nom de la maladie")
    description_maladie = models.TextField(verbose_name="Description")

    class Meta:
        verbose_name = "Maladie"
        verbose_name_plural = "Maladies"

    def __str__(self):
        return self.nom_maladie
    
class Veterinaire(models.Model):
    id_veterinaire = models.AutoField(primary_key=True)
    nom_veterinaire = models.CharField(max_length=50)
    prenom_veterinaire = models.CharField(max_length=20)
    telephone_veterinaire = models.CharField(max_length=20)
    adresse_veterinaire = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom_veterinaire} {self.prenom_veterinaire}"
    
class Vaccin(models.Model):
    id_vaccin = models.AutoField(primary_key=True)
    id_individu = models.ForeignKey(Individu, on_delete=models.CASCADE, related_name='vaccinations')
    id_veterinaire = models.ForeignKey(Veterinaire, on_delete=models.CASCADE, related_name='vaccinations')
    nom_vaccin = models.CharField(max_length=50)
    description_vaccin = models.TextField()
    date_vaccin = models.DateField()

    def __str__(self):
        return f"{self.id_individu} - {self.nom_vaccin} ({self.date_vaccin})"

class Traitement(models.Model):
    id_traitement = models.AutoField(primary_key=True)
    id_individu = models.ForeignKey(Individu, on_delete=models.CASCADE, related_name='traitements')
    id_maladie = models.ForeignKey(Maladie, on_delete=models.CASCADE, related_name='traitements')
    id_veterinaire = models.ForeignKey(Veterinaire, on_delete=models.CASCADE, related_name='traitements')
    medicament = models.CharField(max_length=50)
    dose = models.CharField(max_length=20)
    date_traitement = models.DateField()

    def __str__(self):
        return f"{self.id_individu} - {self.id_maladie} ({self.date_traitement})"
    

class Reproduction(models.Model):
    id_reproduction = models.AutoField(primary_key=True)
    id_veterinaire = models.ForeignKey(Veterinaire, on_delete=models.CASCADE, related_name='reproductions')
    id_femelle = models.ForeignKey(
        Individu,
        on_delete=models.CASCADE,
        related_name='reproductions_femelle'
    )
    id_male = models.ForeignKey(
        Individu,
        on_delete=models.CASCADE,
        related_name='reproductions_male'
    )
    date_saillie = models.DateField()
    date_diagnostic = models.DateField()
    date_prevue = models.DateField()
    date_naissance = models.DateField()
    ETAT_VEAU_CHOICES = [
        ('Bon sante', 'Bon état'),
        ('Malade', 'Malade'),
        ('Mort-ne', 'Mort-né'),
    ]

    etat_veau = models.CharField(max_length=20, choices=ETAT_VEAU_CHOICES)

    def __str__(self):
        return f"{self.id_femelle} - {self.id_male} ({self.date_naissance})"
    

from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.db import models

class Login(models.Model):

    ROLE_CHOICES = [
        ('user', 'Utilisateur standard'),
        ('admin', 'Administrateur'),
        ('gestion_animaux', 'Gestionnaire des animaux'),
        ('gestion_alimentation', 'Responsable alimentation'),
        ('gestion_sanitaire', 'Vétérinaire'),
        ('gestion_production', 'Technicien de production'),
        ('gestion_ventes', 'Responsable commercial'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    identifiant = models.CharField(max_length=50, unique=True, verbose_name="Nom d'utilisateur")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name="Rôle")
    mot_de_passe = models.CharField(max_length=128, verbose_name="Mot de passe")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    est_actif = models.BooleanField(default=True, verbose_name="Compte actif")

    class Meta:
        verbose_name = "Compte utilisateur"
        verbose_name_plural = "Comptes utilisateurs"
        ordering = ['-date_creation']
        db_table = 'auth_logins'

    def __str__(self):
        return f"{self.nom} ({self.role})"

    def save(self, *args, **kwargs):
        if not self.mot_de_passe.startswith('pbkdf2_sha256$'):
            self.mot_de_passe = make_password(self.mot_de_passe)
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.mot_de_passe)

    @staticmethod
    def validate_password_complexity(password):
        if len(password) < 8:
            raise ValidationError(
                ("Le mot de passe doit contenir au moins 8 caractères."),
                code='password_too_short'
            )


# # models.py
# from django.contrib.auth.models import AbstractUser


# class CustomUser(AbstractUser):
#     ROLE_CHOICES = [
#         ('admin', 'Administrateur'),
#         ('gestion_animaux', 'Gestionnaire des Animaux'),
#         ('gestion_alimentation', 'Responsable Alimentation'),
#         ('gestion_sanitaire', 'Vétérinaire'),
#         ('gestion_production', 'Technicien de Production'),
#         ('gestion_ventes', 'Responsable Commercial'),
#         ('user', 'Utilisateur Standard'),
#     ]
#     role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='user')
    




#Commende par ligne

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

class LigneCommande(models.Model):
    id_ligne = models.AutoField(primary_key=True)
    commande = models.ForeignKey('CommandeDetail', on_delete=models.CASCADE, related_name='lignes')
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, related_name='lignes')
    quantite = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"
        ordering = ['-created_at']

    def __str__(self):
        return f"Ligne {self.id_ligne} - {self.produit.nom} ({self.quantite} {self.produit.get_unite_mesure_display()})"

    def annuler_commande(self):
        """Réintègre les quantités commandées dans le stock"""
        if self.produit.unite_mesure == 'litres':
            productions = Production.objects.filter(id_produit=self.produit).order_by('-date_production')
            
            quantite_a_reintegrer = self.quantite
            
            for production in productions:
                if quantite_a_reintegrer <= 0:
                    break
                    
                production.quantite += quantite_a_reintegrer
                production.save()
                quantite_a_reintegrer = 0
                
        elif self.produit.unite_mesure == 'kg':
            productions = Production.objects.filter(id_produit=self.produit).order_by('-date_production')
            
            poids_a_reintegrer = self.quantite
            
            for production in productions:
                if poids_a_reintegrer <= 0:
                    break
                    
                production.poids_carcasse += poids_a_reintegrer
                production.save()
                poids_a_reintegrer = 0

    @property
    def montant_total(self):
        return self.quantite * self.produit.prix_unitaire

    def clean(self):
        # Vérifier si le produit est expiré
        if self.produit.date_expiration < date.today():
            raise ValidationError("Ce produit est expiré, commande impossible")
        
        # Vérification du stock selon le type de produit
        if self.produit.unite_mesure == 'litres':
            total_stock = Production.objects.filter(id_produit=self.produit).aggregate(total=models.Sum('quantite'))['total'] or 0
            
            if total_stock < self.quantite:
                raise ValidationError(f"Stock insuffisant en litres. Il manque {self.quantite - total_stock} litres")
                
        elif self.produit.unite_mesure == 'kg':
            total_stock = Production.objects.filter(id_produit=self.produit).aggregate(total=models.Sum('poids_carcasse'))['total'] or 0
            
            if total_stock < self.quantite:
                raise ValidationError(f"Stock insuffisant en kg. Il manque {self.quantite - total_stock} kg")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.deduire_stock()
    
    def deduire_stock(self):
        """Déduit la quantité commandée du stock disponible"""
        if self.produit.unite_mesure == 'litres':
            productions = Production.objects.filter(id_produit=self.produit, quantite__gt=0).order_by('date_production')
            
            quantite_a_deduire = self.quantite
            
            for production in productions:
                if quantite_a_deduire <= 0:
                    break
                    
                if production.quantite >= quantite_a_deduire:
                    production.quantite -= quantite_a_deduire
                    production.save()
                    quantite_a_deduire = 0
                else:
                    quantite_a_deduire -= production.quantite
                    production.quantite = 0
                    production.save()
                    
        elif self.produit.unite_mesure == 'kg':
            productions = Production.objects.filter(id_produit=self.produit, poids_carcasse__gt=0).order_by('date_production')
            
            poids_a_deduire = self.quantite
            
            for production in productions:
                if poids_a_deduire <= 0:
                    break
                    
                if production.poids_carcasse >= poids_a_deduire:
                    production.poids_carcasse -= poids_a_deduire
                    production.save()
                    poids_a_deduire = 0
                else:
                    poids_a_deduire -= production.poids_carcasse
                    production.poids_carcasse = 0
                    production.save()

