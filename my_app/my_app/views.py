from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from django.db.models import Q

from .models import Troupeau, Aliment, StockAliment, Ration,Individu, Produit, Production, Client, Commande,Paiement
from .forms import StockAlimentForm

from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import date
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import date
from .decorators import role_required


# ------------------ Helpers ------------------

def success_response(message, data=None):
    return JsonResponse({
        "success": True,
        "message": message,
        "data": data
    })

def error_response(message, errors=None):
    return JsonResponse({
        "success": False,
        "message": message,
        "errors": errors
    })

def get_messages_json(request):
    message_list = []
    for message in messages.get_messages(request):
        message_list.append({
            'level': message.level,
            'message': message.message,
            'tags': message.tags,
        })
    return json.dumps(message_list)

# ------------------ Pages ------------------

def home(request):
    return render(request, "home.html")

# def bovin(request):
#     return render(request, "bouf/bovin.html")

def troupeauadd(request):
    messages_json = get_messages_json(request)
    return render(request, "bouf/troupeauadd.html", {'messages_json': messages_json})

def troupeauupdate(request):
    return render(request, "bouf/troupeauupdate.html")

# @role_required( 'gestion_animaux')
def troupeautableau(request):
    return render(request, "bouf/troupeautableau.html")

def aliment_tableau(request):
    return render(request, "bouf/Aliment_Tableau.html")

def aliment_add(request):
    return render(request, "bouf/Aliment_Add.html")

def stocktableau(request):
    return render(request, "bouf/Stock_Aliment_Tableau.html")

def stockadd(request):
    return render(request, "bouf/Stock_Aliment_Add.html")

def stockajouterlien(request):
    return render(request, "bouf/Stock_Ajouter.html")


def rationtableau(request):
    return render(request, "bouf/Ration_Tableau.html")

def rationadd(request):
    return render(request, "bouf/Ration_Add.html")


# @role_required('gestion_animaux')
def individutableau(request):
    return render(request, "bouf/Individu_Tableau.html")

def individuadd(request):
    return render(request, "bouf/Individu_Add.html")

def produittableau(request):
    return render(request, "bouf/Produit_Tableau.html")

def produitadd(request):
    return render(request, "bouf/Produit_Add.html")

def productiontableau(request):
    return render(request, "bouf/Production_Tableau.html")

def productionadd(request):
    return render(request, "bouf/Production_Add.html")

def clienttableau(request):
    return render(request, "bouf/Client_Tableau.html")

def clientadd(request):
    return render(request, "bouf/Client_Add.html")

def commandetableau(request):
    return render(request, "bouf/Commande_Tableau.html")

def commandeadd(request):
    return render(request, "bouf/Commande_Add.html")

def paiementtableau(request):
    return render(request, "bouf/Paiement_Tableau.html")

def paiementadd(request):
    return render(request, "bouf/Paiement_Add.html")

def maladietableau(request):
    return render(request, "bouf/Maladie_Tableau.html")

def maladieadd(request):
    return render(request, "bouf/Maladie_Add.html")

def veterinairetableau(request):
    return render(request, "bouf/Veterinaire_Tableau.html")

def veterinaireadd(request):
    return render(request, "bouf/Veterinaire_Add.html")

def vaccintableau(request):
    return render(request, "bouf/Vaccin_Tableau.html")

def vaccinadd(request):
    return render(request, "bouf/Vaccin_Add.html")

def traitementtableau(request):
    return render(request, "bouf/Traitement_Tableau.html")

def traitementadd(request):
    return render(request, "bouf/Traitement_Add.html")

def reproductiontableau(request):
    return render(request, "bouf/Reproduction_Tableau.html")

def reproductionadd(request):
    return render(request, "bouf/Reproduction_Add.html")

def par_ligne(request):
    return render(request, "bouf/par_ligne.html")




#Admin

# def chef(request):
#     return render(request, "admin/chef.html")

def addchef(request):
    return render(request, "admin/add.html")

def affiche(request):
    return render(request, "admin/affiche.html")

def affiche(request):
    return render(request, "admin/affiche.html")



# ------------------ CRUD Troupeau ------------------


@csrf_exempt
def ajouter_troupeau(request):
    if request.method == "POST":
        id_troupeau = request.POST.get("id_troupeau")
        nom = request.POST.get("nom")
        race = request.POST.get("race")
        date_creation = request.POST.get("date_creation")
        type_troupeau = request.POST.get("type")

        try:
            # Vérifiez si un troupeau avec cet id_troupeau existe déjà
            if Troupeau.objects.filter(id_troupeau=id_troupeau).exists():
                messages.error(request, f"Erreur : Le troupeau avec l'ID {id_troupeau} existe déjà.")
                return redirect('troupeauadd') # Rediriger vers le formulaire d'ajout avec l'erreur
            else:
                Troupeau.objects.create(
                    id_troupeau=id_troupeau,
                    nom=nom,
                    race=race,
                    date_creation=date_creation,
                    type=type_troupeau
                )
                messages.success(request, "Troupeau ajouté avec succès.")
                return redirect('troupeauadd') # Rediriger vers le tableau après succès
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout du troupeau : {e}")
            return redirect('troupeauadd') # Rediriger vers le formulaire d'ajout en cas d'autre erreur
    else:
        # Si la requête n'est pas POST, afficher le formulaire d'ajout
        return render(request, 'bouf/troupeauadd.html')

@csrf_exempt
def modifier_troupeau(request, id_troupeau):
    troupeau = get_object_or_404(Troupeau, id_troupeau=id_troupeau)

    if request.method == "POST":
        try:
            troupeau.nom = request.POST.get("nom")
            troupeau.race = request.POST.get("race")
            troupeau.date_creation = request.POST.get("date_creation")
            troupeau.type = request.POST.get("type")
            troupeau.save()
            messages.success(request, "Troupeau modifié avec succès.")
            return redirect('troupeautableau')  # Redirige après la modification
        except Exception as e:
            messages.error(request, f"Erreur : {e}")
            return redirect('troupeautableau')

    else:  # Requête GET : afficher le formulaire pré-rempli
        return render(request, 'bouf/troupeauupdate.html', {'troupeau': troupeau})





@require_POST
def supprimer_troupeau(request, id_troupeau):
    try:
        troupeau = get_object_or_404(Troupeau, id_troupeau=id_troupeau)
        troupeau.delete()
        messages.success(request, f"Le troupeau avec l'ID {id_troupeau} a été supprimé avec succès.")
        return JsonResponse({'status': 'success'})
    except Troupeau.DoesNotExist:
        messages.error(request, f"Erreur : Le troupeau avec l'ID {id_troupeau} n'existe pas.")
        return JsonResponse({'status': 'error', 'message': 'Troupeau non trouvé'}, status=404)
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression du troupeau : {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def liste_troupeaux_json(request):
    troupeaux = Troupeau.objects.all().values()
    return success_response("Liste des troupeaux", list(troupeaux))

def troupeau_tableau(request):
    rechercher = request.GET.get('rechercher')
    if rechercher:
        troupeaux = Troupeau.objects.filter(nom__icontains=rechercher)
    else:
        troupeaux = Troupeau.objects.all()

    return render(request, 'bouf/troupeautableau.html', {'troupeaux': troupeaux})



# ------------------ CRUD Aliment ------------------

@csrf_exempt
def ajouter_aliment(request):
    if request.method == "POST":
        try:
            id_aliment = request.POST.get("id_aliment")
            if Aliment.objects.filter(id_aliment=id_aliment).exists():
                messages.error(request, f"L'aliment avec l'ID {id_aliment} existe déjà")
                return redirect('aliment_add')
            
            aliment = Aliment.objects.create(
                id_aliment=id_aliment,
                nom_aliment=request.POST.get("nom_aliment"),
                type_aliment=request.POST.get("type_aliment"),
                stock_aliment=0  # Initialisation du stock à 0
            )
            messages.success(request, f"Aliment {aliment.nom_aliment} ajouté avec succès")
            return redirect('aliment_tableau')
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout : {str(e)}")
            return redirect('aliment_add')
    return render(request, 'bouf/Aliment_Add.html')

@csrf_exempt
def modifier_aliment(request, id_aliment):
    aliment = get_object_or_404(Aliment, id_aliment=id_aliment)
    if request.method == "POST":
        try:
            aliment.nom_aliment = request.POST.get("nom_aliment")
            aliment.type_aliment = request.POST.get("type_aliment")
            aliment.save()
            messages.success(request, f"Aliment {aliment.nom_aliment} modifié avec succès")
            return redirect('aliment_tableau')
        except Exception as e:
            messages.error(request, f"Erreur lors de la modification : {str(e)}")
            return redirect('modifier_aliment', id_aliment=id_aliment)
    return render(request, 'bouf/Aliment_Update.html', {'aliment': aliment})

@require_POST
def supprimer_aliment(request, id_aliment):
    try:
        aliment = get_object_or_404(Aliment, id_aliment=id_aliment)
        
        # Supprimer les stocks liés à cet aliment
        StockAliment.objects.filter(id_aliment=aliment).delete()
        
        nom = aliment.nom_aliment
        aliment.delete()
        messages.success(request, f"Aliment {nom} supprimé avec succès.")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression : {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def aliment_tableau(request):
    rechercher = request.GET.get('rechercher', '')
    aliments = Aliment.objects.all()
    
    if rechercher:
        aliments = aliments.filter(nom_aliment__icontains=rechercher)
    
    return render(request, 'bouf/Aliment_Tableau.html', {
        'aliments': aliments,
        'rechercher': rechercher
    })


# ------------------ CRUD StockAliment ------------------

@csrf_exempt
def ajouter_stock_aliment(request):
    if request.method == "POST":
        try:
            id_aliment = request.POST.get("id_aliment")
            stock_entree = float(request.POST.get("stock_entree", 0))
            
            # Récupérer l'aliment correspondant
            aliment = get_object_or_404(Aliment, pk=id_aliment)
            
            # Créer le nouveau stock
            stock = StockAliment.objects.create(
                id_aliment=aliment,
                fournisseur_aliment=request.POST.get("fournisseur_aliment"),
                stock_entree=stock_entree,
                date_reception=request.POST.get("date_reception"),
                prix_aliment=request.POST.get("prix_aliment"),
            )
            
            # Mettre à jour le stock total de l'aliment
            aliment.stock_aliment += stock_entree
            aliment.save()
            
            messages.success(request, f"Stock ajouté avec succès. Nouveau stock total: {aliment.stock_aliment} kg")
            return redirect('stocktableau')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de l'ajout du stock: {str(e)}")
            return redirect('stockadd')
    
    # GET request - afficher le formulaire
    aliments = Aliment.objects.all()
    return render(request, 'bouf/Stock_Aliment_Add.html', {'aliments': aliments})

@csrf_exempt
def stocktableau(request):
    # Récupération des stocks avec jointure sur Aliment
    stocks = StockAliment.objects.select_related('id_aliment').all()
    
    # Filtrage par date si paramètre présent
    date_recherche = request.GET.get('rechercher')
    if date_recherche:
        stocks = stocks.filter(date_reception=date_recherche)
    
    return render(request, 'bouf/Stock_Aliment_Tableau.html', {
        'stock_list': stocks,
        'date_recherche': date_recherche
    })

@require_POST
def supprimer_stock(request, id_stock):
    try:
        stock = get_object_or_404(StockAliment, id_stock=id_stock)  # Utilisez id_stock au lieu de id
        aliment = stock.id_aliment
        
        # Mettre à jour le stock de l'aliment avant suppression
        aliment.stock_aliment -= stock.stock_entree
        aliment.save()
        
        stock.delete()
        messages.success(request, "Stock supprimé et stock total mis à jour")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

@csrf_exempt
def modifier_stock(request, id_stock):
    stock = get_object_or_404(StockAliment, id_stock=id_stock)  # correction ici
    
    if request.method == "POST":
        try:
            stock.fournisseur_aliment = request.POST.get("fournisseur_aliment")
            stock.date_reception = request.POST.get("date_reception")
            stock.prix_aliment = request.POST.get("prix_aliment")
            stock.save()

            messages.success(request, "Stock modifié avec succès")
            return redirect('stocktableau')
            
        except Exception as e:
            messages.error(request, f"Erreur lors de la modification: {str(e)}")
            return redirect('modifier_stock', id_stock=id_stock)
    
    return render(request, 'bouf/Stock_Aliment_Update.html', {
        'stock': stock,
        'aliments': Aliment.objects.all()
    })




# ------------------ CRUD Ration ------------------

def rationtableau(request):
    """Affiche la liste des rations avec possibilité de filtrage"""
    date_recherche = request.GET.get('rechercher')
    rations = Ration.objects.select_related('id_troupeau', 'id_aliment').all()
    
    if date_recherche:
        rations = rations.filter(date_ration=date_recherche)
    
    context = {
        'rations': rations,
        'date_recherche': date_recherche
    }
    return render(request, 'bouf/Ration_Tableau.html', context)

def rationadd(request):
    """Affiche le formulaire d'ajout de ration"""
    if request.method == "POST":
        try:
            id_troupeau = request.POST.get("id_troupeau_id")
            id_aliment = request.POST.get("id_aliment_id")
            quantite = int(request.POST.get("quantite_aliment"))
            date_ration = request.POST.get("date_ration")
            
            # Vérifier si l'aliment a suffisamment de stock
            aliment = Aliment.objects.get(id_aliment=id_aliment)
            if aliment.stock_aliment < quantite:
                messages.error(request, f"Stock insuffisant. Stock disponible: {aliment.stock_aliment}")
                return redirect('rationadd')
            
            # Créer la ration
            ration = Ration.objects.create(
                id_troupeau_id=id_troupeau,
                id_aliment_id=id_aliment,
                quantite_aliment=quantite,
                date_ration=date_ration
            )
            
            # Mettre à jour le stock de l'aliment
            aliment.stock_aliment -= quantite
            aliment.save()
            
            messages.success(request, "Ration ajoutée avec succès")
            return redirect('rationtableau')
            
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('rationadd')
    
    # GET request - afficher le formulaire
    troupeaux = Troupeau.objects.all()
    aliments = Aliment.objects.filter(stock_aliment__gt=0)  # Seuls les aliments avec stock > 0
    return render(request, 'bouf/Ration_Add.html', {
        'troupeaux': troupeaux,
        'aliments': aliments
    })

@require_POST
def supprimer_ration(request, id_ration):
    """Supprime une ration et remet le stock"""
    try:
        ration = get_object_or_404(Ration, id_ration=id_ration)
        aliment = ration.id_aliment
        
        # Remettre le stock avant suppression
        aliment.stock_aliment += ration.quantite_aliment
        aliment.save()
        
        ration.delete()
        messages.success(request, "Ration supprimée et stock remis à jour")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def modifier_ration(request, id_ration):
    """Affiche et traite le formulaire de modification"""
    ration = get_object_or_404(Ration, id_ration=id_ration)
    
    if request.method == "POST":
        try:
            ancienne_quantite = ration.quantite_aliment
            nouvelle_quantite = int(request.POST.get("quantite_aliment"))
            aliment = ration.id_aliment
            
            # Calcul de la différence de quantité
            difference = nouvelle_quantite - ancienne_quantite
            
            # Vérifier si le stock est suffisant
            if difference > 0 and aliment.stock_aliment < difference:
                messages.error(request, f"Stock insuffisant pour cette modification. Stock disponible: {aliment.stock_aliment}")
                return redirect('modifier_ration', id_ration=id_ration)
            
            # Mettre à jour la ration
            ration.id_troupeau_id = request.POST.get("id_troupeau_id")
            ration.id_aliment_id = request.POST.get("id_aliment_id")
            ration.quantite_aliment = nouvelle_quantite
            ration.date_ration = request.POST.get("date_ration")
            ration.save()
            
            # Mettre à jour le stock
            aliment.stock_aliment -= difference
            aliment.save()
            
            messages.success(request, "Ration modifiée avec succès")
            return redirect('rationtableau')
            
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
            return redirect('modifier_ration', id_ration=id_ration)
    
    # GET request - afficher le formulaire
    troupeaux = Troupeau.objects.all()
    aliments = Aliment.objects.all()
    return render(request, 'bouf/Ration_Update.html', {
        'ration': ration,
        'troupeaux': troupeaux,
        'aliments': aliments
    })




# ------------------ CRUD Individu ------------------

def individutableau(request):
    rechercher = request.GET.get('rechercher', '')
    individus = Individu.objects.select_related('id_troupeau').all()
    
    if rechercher:
        individus = individus.filter(
            Q(numero_identification__icontains=rechercher) |
            Q(id_troupeau__nom__icontains=rechercher)
        )
    
    return render(request, 'bouf/Individu_Tableau.html', {
        'individus': individus,
        'rechercher': rechercher
    })

def individuadd(request):
    if request.method == "POST":
        try:
            individu = Individu.objects.create(
                id_troupeau_id=request.POST.get("id_troupeau_id"),
                numero_identification=request.POST.get("numero_identification"),
                sexe=request.POST.get("sexe"),
                date_naissance=request.POST.get("date_naissance"),
                poids=request.POST.get("poids"),
                etat_sante=request.POST.get("etat_sante"),
                vaccins=request.POST.get("vaccins"),
                description=request.POST.get("description", "")
            )
            messages.success(request, "Individu ajouté avec succès")
            return redirect('individutableau')
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    troupeaux = Troupeau.objects.all()
    return render(request, 'bouf/Individu_Add.html', {'troupeaux': troupeaux})

def individuupdate(request, id_individu):
    individu = get_object_or_404(Individu, pk=id_individu)
    
    if request.method == "POST":
        try:
            
            individu.numero_identification = request.POST.get("numero_identification")
            individu.sexe = request.POST.get("sexe")
            individu.date_naissance = request.POST.get("date_naissance")
            individu.poids = request.POST.get("poids")
            individu.etat_sante = request.POST.get("etat_sante")
            individu.vaccins = request.POST.get("vaccins")
            individu.description = request.POST.get("description", "")
            individu.save()
            
            messages.success(request, "Individu mis à jour avec succès")
            return redirect('individutableau')
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    troupeaux = Troupeau.objects.all()
    return render(request, 'bouf/Individu_Update.html', {
        'individu': individu,
        'troupeaux': troupeaux
    })

@require_POST
def individudelete(request, id_individu):
    try:
        individu = get_object_or_404(Individu, pk=id_individu)
        individu.delete()
        messages.success(request, "Individu supprimé avec succès")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)




# ------------------ CRUD Produit ------------------

def produittableau(request):
    rechercher = request.GET.get('rechercher', '')
    produits = Produit.objects.all()
    
    if rechercher:
        produits = produits.filter(
            Q(nom__icontains=rechercher) |
            Q(unite_mesure__icontains=rechercher)
        )
    
    return render(request, 'bouf/Produit_Tableau.html', {
        'produits': produits,
        'rechercher': rechercher
    })

def produitadd(request):
    if request.method == "POST":
        try:
            produit = Produit.objects.create(
                nom=request.POST.get("nom"),
                unite_mesure=request.POST.get("unite_mesure"),
                prix_unitaire=request.POST.get("prix_unitaire"),
                date_expiration=request.POST.get("date_expiration")
            )
            messages.success(request, "Produit ajouté avec succès")
            return redirect('produittableau')
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return render(request, 'bouf/Produit_Add.html')

def produitupdate(request, id_produit):
    produit = get_object_or_404(Produit, pk=id_produit)
    
    if request.method == "POST":
        try:
            produit.nom = request.POST.get("nom")
            produit.unite_mesure = request.POST.get("unite_mesure")
            produit.prix_unitaire = request.POST.get("prix_unitaire")
            produit.date_expiration = request.POST.get("date_expiration")
            produit.save()
            
            messages.success(request, "Produit mis à jour avec succès")
            return redirect('produittableau')
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return render(request, 'bouf/Produit_Update.html', {
        'produit': produit
    })

@require_POST
def produitdelete(request, id_produit):
    try:
        produit = get_object_or_404(Produit, pk=id_produit)
        produit.delete()
        messages.success(request, "Produit supprimé avec succès")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)




# ------------------ CRUD Production ------------------

def productiontableau(request):
    rechercher = request.GET.get('rechercher', '')
    productions = Production.objects.select_related('id_produit', 'id_individu').all()
    
    if rechercher:
        productions = productions.filter(
            Q(id_produit__nom__icontains=rechercher) |
            Q(id_produit__id_produit__icontains=rechercher)
        )
    
    return render(request, 'bouf/Production_Tableau.html', {
        'productions': productions,
        'rechercher': rechercher
    })

def productionadd(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Récupération des données
                id_produit = request.POST.get("id_produit")
                id_individu = request.POST.get("id_individu")
                
                # Vérification des conditions avant création
                produit = Produit.objects.get(pk=id_produit)
                individu = Individu.objects.get(pk=id_individu)
                
                if produit.unite_mesure == 'litres':
                    if individu.etat_sante in ['malade', 'traitement']:
                        raise ValidationError("Un individu malade ou en traitement ne peut pas produire du lait")
                    
                    age = (date.today() - individu.date_naissance).days / 365
                    if age < 2:
                        raise ValidationError("Un individu de moins de 2 ans ne peut pas produire du lait")
                        
                    if individu.sexe == 'male':
                        raise ValidationError("Un individu mâle ne peut pas produire du lait")
                
                elif produit.unite_mesure == 'kg':
                    if individu.etat_sante not in ['bon','malade', 'traitement']:
                        raise ValidationError("Seuls les individus malades ou en traitement peuvent être transformés en viande")
                
                # Création de la production
                production = Production.objects.create(
                    id_produit=produit,
                    id_individu=individu,
                    date_production=request.POST.get("date_production"),
                    quantite=request.POST.get("quantite"),
                    poids_carcasse=request.POST.get("poids_carcasse")
                )
                
                messages.success(request, "Production enregistrée avec succès")
                return redirect('productiontableau')
                
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    produits = Produit.objects.all()
    individus = Individu.objects.all()
    return render(request, 'bouf/Production_Add.html', {
        'produits': produits,
        'individus': individus
    })

def productionupdate(request, id_production):
    production = get_object_or_404(Production, pk=id_production)
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Vérification des conditions
                produit = production.id_produit
                individu = production.id_individu
                
                if produit.unite_mesure == 'litres':
                    if individu.etat_sante in ['malade', 'traitement']:
                        raise ValidationError("Un individu malade ou en traitement ne peut pas produire du lait")
                    
                    age = (date.today() - individu.date_naissance).days / 365
                    if age < 2:
                        raise ValidationError("Un individu de moins de 2 ans ne peut pas produire du lait")
                        
                    if individu.sexe == 'male':
                        raise ValidationError("Un individu mâle ne peut pas produire du lait")
                
                elif produit.unite_mesure == 'kg':
                    if individu.etat_sante not in ['bon','malade', 'traitement']:
                        raise ValidationError("Seuls les individus malades ou en traitement peuvent être transformés en viande")
                
                # Mise à jour
                production.date_production = request.POST.get("date_production")
                production.quantite = request.POST.get("quantite")
                production.poids_carcasse = request.POST.get("poids_carcasse")
                production.save()
                
                messages.success(request, "Production mise à jour avec succès")
                return redirect('productiontableau')
                
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    produits = Produit.objects.all()
    individus = Individu.objects.all()
    return render(request, 'bouf/Production_Update.html', {
        'production': production,
        'produits': produits,
        'individus': individus
    })

@require_POST
def productiondelete(request, id_production):
    try:
        production = get_object_or_404(Production, pk=id_production)
        production.delete()
        messages.success(request, "Production supprimée avec succès")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    




from django.http import JsonResponse

def individus_par_produit(request):
    produit_id = request.GET.get('produit_id')
    if not produit_id:
        return JsonResponse({'error': 'Produit ID manquant'}, status=400)
    
    try:
        produit = Produit.objects.get(pk=produit_id)
        individus = Individu.objects.all()
        
        if produit.unite_mesure == 'litres':
            # Pour le lait: femelles en bonne santé de +2 ans
            individus = individus.filter(
                sexe='femelle',
                etat_sante='bon',
                date_naissance__lte=date.today() - timedelta(days=365*2)
            )
        elif produit.unite_mesure == 'kg':
            # Pour la viande: individus malades ou en traitement
            individus = individus.filter(
                etat_sante__in=['bon','malade', 'traitement']
            )
        
        data = {
            'individus': [
                {
                    'id': i.id_individu,
                    'numero': i.numero_identification,
                    'sexe': i.get_sexe_display(),
                    'etat': i.get_etat_sante_display()
                }
                for i in individus
            ]
        }
        return JsonResponse(data)
    
    except Produit.DoesNotExist:
        return JsonResponse({'error': 'Produit non trouvé'}, status=404)
    


from django.core.exceptions import ValidationError
from django.db import transaction

# ------------------ CRUD Client ------------------

def clienttableau(request):
    rechercher = request.GET.get('rechercher', '')
    clients = Client.objects.all()
    
    if rechercher:
        clients = clients.filter(
            Q(nom_client__icontains=rechercher) |
            Q(prenom_client__icontains=rechercher) |
            Q(telephone__icontains=rechercher)
        )
    
    return render(request, 'bouf/Client_Tableau.html', {
        'clients': clients,
        'rechercher': rechercher
    })

def clientadd(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Nettoyer le numéro de téléphone
                telephone = ''.join(filter(str.isdigit, request.POST.get('telephone')))
                
                client = Client(
                    nom_client=request.POST.get('nom_client'),
                    prenom_client=request.POST.get('prenom_client'),
                    adresse=request.POST.get('adresse'),
                    telephone=telephone,
                    email_client=request.POST.get('email_client')
                )
                
                # Validation manuelle
                if len(telephone) != 10:
                    raise ValidationError("Le numéro de téléphone doit contenir 10 chiffres")
                
                client.full_clean()  # Valide tous les champs
                client.save()
                
                messages.success(request, "Client ajouté avec succès")
                return redirect('clienttableau')
                
        except ValidationError as e:
            messages.error(request, f"Erreur de validation: {', '.join(e.messages)}")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return render(request, 'bouf/Client_Add.html')

def clientupdate(request, id_client):
    client = get_object_or_404(Client, pk=id_client)
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Nettoyer le numéro de téléphone
                telephone = ''.join(filter(str.isdigit, request.POST.get('telephone')))
                
                client.nom_client = request.POST.get('nom_client')
                client.prenom_client = request.POST.get('prenom_client')
                client.adresse = request.POST.get('adresse')
                client.telephone = telephone
                client.email_client = request.POST.get('email_client')
                
                # Validation manuelle
                if len(telephone) != 10:
                    raise ValidationError("Le numéro de téléphone doit contenir 10 chiffres")
                
                client.full_clean()
                client.save()
                
                messages.success(request, "Client mis à jour avec succès")
                return redirect('clienttableau')
                
        except ValidationError as e:
            messages.error(request, f"Erreur de validation: {', '.join(e.messages)}")
        except Exception as e:
            messages.error(requefst, f"Erreur: {str(e)}")
    
    return render(request, 'bouf/Client_Update.html', {'client': client})

@require_POST
def clientdelete(request, id_client):
    try:
        client = get_object_or_404(Client, pk=id_client)
        client.delete()
        messages.success(request, "Client supprimé avec succès")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



# ------------------ CRUD Commande ------------------

def commandetableau(request):
    rechercher = request.GET.get('rechercher', '')
    commandes = Commande.objects.select_related('id_client', 'id_produit').all()
    
    if rechercher:
        commandes = commandes.filter(date_commande=rechercher)
    
    return render(request, 'bouf/Commande_Tableau.html', {
        'commandes': commandes,
        'rechercher': rechercher
    })

from django.db import transaction
from django.core.exceptions import ValidationError

def commandeadd(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                produit_id = request.POST.get('id_produit')
                quantite = float(request.POST.get('quantite_commande', 0))
                
                produit = Produit.objects.get(pk=produit_id)
                
                # Vérification spécifique pour les produits en kg
                if produit.unite_mesure == 'kg':
                    quantite = float(request.POST.get('quantite_commande', 0))
                    if quantite <= 0:
                        raise ValidationError("La quantité doit être positive")
                
                commande = Commande(
                    id_client_id=request.POST.get('id_client'),
                    id_produit_id=produit_id,
                    quantite=quantite,
                    date_commande=request.POST.get('date_commande') or date.today()
                )
                
                commande.full_clean()
                commande.save()
                
                messages.success(request, "Commande enregistrée avec succès")
                return redirect('commandetableau')
                
        except ValidationError as e:
            messages.error(request, f"Erreur: {', '.join(e.messages)}")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    clients = Client.objects.all()
    produits = Produit.objects.filter(date_expiration__gte=date.today())
    return render(request, 'bouf/Commande_Add.html', {
        'clients': clients,
        'produits': produits,
        'today': date.today().strftime('%Y-%m-%d')
    })

def commandeupdate(request, id_commande):
    commande = get_object_or_404(Commande, pk=id_commande)
    
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Remettre le stock avant modification
                commande.annuler_commande()
                
                # Mise à jour
                commande.id_client_id = request.POST.get('id_client')
                commande.id_produit_id = request.POST.get('id_produit')
                commande.quantite = int(request.POST.get('quantite_commande'))
                commande.date_commande = request.POST.get('date_commande')
                
                # Validation
                produit = commande.id_produit
                if produit.date_expiration < date.today():
                    raise ValidationError("Ce produit est expiré, commande impossible")
                
                commande.full_clean()
                commande.save()
                
                messages.success(request, "Commande mise à jour avec succès")
                return redirect('commandetableau')
                
        except ValidationError as e:
            messages.error(request, f"Erreur de validation: {', '.join(e.messages)}")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    clients = Client.objects.all()
    produits = Produit.objects.filter(date_expiration__gte=date.today())
    return render(request, 'bouf/Commande_Update.html', {
        'commande': commande,
        'clients': clients,
        'produits': produits
    })

@require_POST
def commandedelete(request, id_commande):
    try:
        commande = get_object_or_404(Commande, pk=id_commande)
        commande.annuler_commande()
        commande.delete()
        messages.success(request, "Commande supprimée avec succès")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

from django.http import JsonResponse
from django.db.models import Sum

def stock_produit(request):
    produit_id = request.GET.get('produit_id')
    if not produit_id:
        return JsonResponse({'error': 'Produit ID manquant'}, status=400)
    
    try:
        produit = Produit.objects.get(pk=produit_id)
        
        if produit.unite_mesure == 'litres':
            stock = Production.objects.filter(id_produit=produit).aggregate(
                total=Sum('quantite')
            )['total'] or 0
        elif produit.unite_mesure == 'kg':
            stock = Production.objects.filter(id_produit=produit).aggregate(
                total=Sum('poids_carcasse')
            )['total'] or 0
        else:
            stock = 0
            
        return JsonResponse({
            'stock': stock,
            'unite': produit.get_unite_mesure_display()
        })
    except Produit.DoesNotExist:
        return JsonResponse({'error': 'Produit non trouvé'}, status=404)
    
from django.db import transaction
from django.core.exceptions import ValidationError

# ------------------ CRUD Paiement ------------------

def paiementtableau(request):
    rechercher = request.GET.get('rechercher', '')
    paiements = Paiement.objects.select_related('id_commandeDetail').all()
    
    if rechercher:
        paiements = paiements.filter(
            Q(id_commande__id_commande__icontains=rechercher) |
            Q(mode_paiement__icontains=rechercher)
        )
    
    return render(request, 'bouf/Paiement_Tableau.html', {
        'paiements': paiements,
        'rechercher': rechercher
    })

def paiementadd(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                paiement = Paiement(
                    id_commandeDetail_id=request.POST.get('id_commandeDetail_id'),
                    mode_paiement=request.POST.get('mode_paiement'),
                    date_paiement=request.POST.get('date_paiement'),
                )
                
                paiement.full_clean()
                paiement.save()
                
                messages.success(request, "Paiement enregistré avec succès")
                return redirect('paiementtableau')
                
        except ValidationError as e:
            messages.error(request, f"Erreur de validation: {', '.join(e.messages)}")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    commandes = CommandeDetail.objects.all()
    return render(request, 'bouf/Paiement_Add.html', {
        'commandes': commandes,
        'today': date.today().strftime('%Y-%m-%d')
    })

# def paiementupdate(request, id_paiement):
#     paiement = get_object_or_404(Paiement, pk=id_paiement)
    
#     if request.method == "POST":
#         try:
#             with transaction.atomic():
#                 # id_commandeDetail_id=request.POST.get('id_commande'),
#                 paiement.mode_paiement = request.POST.get('mode_paiement')
#                 paiement.date_paiement = request.POST.get('date_paiement')
            
                
#                 paiement.full_clean()
#                 paiement.save()
                
#                 messages.success(request, "Paiement mis à jour avec succès")
#                 return redirect('paiementtableau')
                
#         except ValidationError as e:
#             messages.error(request, f"Erreur de validation: {', '.join(e.messages)}")
#         except Exception as e:
#             messages.error(request, f"Erreur: {str(e)}")
    
#     commandes = Commande.objects.all()
#     return render(request, 'bouf/Paiement_Update.html', {
#         'paiement': paiement,
#         'commandes': commandes
#     })

@require_POST
def paiementdelete(request, id_paiement):
    try:
        paiement = get_object_or_404(Paiement, pk=id_paiement)
        paiement.delete()
        messages.success(request, "Paiement supprimé avec succès")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def montant_commande(request):
    commande_id = request.GET.get('commande_id')
    if not commande_id:
        return JsonResponse({'error': 'Commande ID manquant'}, status=400)
    
    try:
        commande = Commande.objects.get(pk=commande_id)
        return JsonResponse({
            'montant': float(commande.montant_total)
        })
    except Commande.DoesNotExist:
        return JsonResponse({'error': 'Commande non trouvée'}, status=404)
    


#------------- CRUD MALADIE ---------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Maladie
from .forms import MaladieForm

def maladietableau(request):
    maladies = Maladie.objects.all()
    
    # Recherche
    if 'rechercher' in request.GET:
        recherche = request.GET['rechercher']
        maladies = maladies.filter(nom_maladie__icontains=recherche)
    
    context = {'maladies': maladies}
    return render(request, 'bouf/Maladie_Tableau.html', context)

def maladieadd(request):
    if request.method == 'POST':
        form = MaladieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Maladie ajoutée avec succès!")
            return redirect('maladietableau')
    else:
        form = MaladieForm()
    
    return render(request, 'bouf/Maladie_Add.html', {'form': form})

def maladieedit(request, id):
    maladie = get_object_or_404(Maladie, id_maladie=id)
    if request.method == 'POST':
        form = MaladieForm(request.POST, instance=maladie)
        if form.is_valid():
            form.save()
            messages.success(request, "Maladie modifiée avec succès!")
            return redirect('maladietableau')
    else:
        form = MaladieForm(instance=maladie)
    
    return render(request, 'bouf/Maladie_Edit.html', {'form': form, 'maladie': maladie})

def maladiesupprimer(request, id):
    if request.method == 'POST':
        maladie = get_object_or_404(Maladie, id_maladie=id)
        maladie.delete()
        return JsonResponse({'status': 'success', 'message': 'Maladie supprimée avec succès!'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)



#-------------CRUD VETERINAIRE -------------------#
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Veterinaire

# Affichage
def veterinairetableau(request):
    query = request.GET.get('rechercher')
    if query:
        veterinaires = Veterinaire.objects.filter(nom_veterinaire__icontains=query)
    else:
        veterinaires = Veterinaire.objects.all()
    return render(request, 'bouf/Veterinaire_Tableau.html', {'veterinaires': veterinaires})

# Ajout
def veterinaireadd(request):
    if request.method == 'POST':
        nom = request.POST.get('nom_veterinaire')
        prenom = request.POST.get('prenom_veterinaire')
        telephone = request.POST.get('telephone_veterinaire')
        adresse = request.POST.get('adresse_veterinaire')

        if nom and prenom:
            Veterinaire.objects.create(
                nom_veterinaire=nom,
                prenom_veterinaire=prenom,
                telephone_veterinaire=telephone,
                adresse_veterinaire=adresse
            )
            messages.success(request, "Vétérinaire ajouté avec succès.")
            return redirect('veterinairetableau')
        else:
            messages.error(request, "Tous les champs sont obligatoires.")
    return render(request, 'bouf/Veterinaire_Add.html')

# Modification
def veterinaireupdate(request, id):
    veterinaire = get_object_or_404(Veterinaire, pk=id)
    if request.method == 'POST':
        try:
            veterinaire.nom_veterinaire = request.POST.get('nom_veterinaire')
            veterinaire.prenom_veterinaire = request.POST.get('prenom_veterinaire')
            veterinaire.telephone_veterinaire = request.POST.get('telephone_veterinaire')
            veterinaire.adresse_veterinaire = request.POST.get('adresse_veterinaire')
            veterinaire.save()
            messages.success(request, "Vétérinaire mis à jour avec succès")
            return redirect('veterinairetableau')
        except Exception as e:
            messages.error(request, f"Erreur lors de la mise à jour: {str(e)}")
            return redirect('veterinaireupdate', id=id)
    
    return render(request, 'bouf/Veterinaire_Update.html', {'veterinaire': veterinaire})

# Suppression (AJAX)
def veterinairesupprimer(request, id):
    if request.method == 'POST':
        veterinaire = get_object_or_404(Veterinaire, pk=id)
        veterinaire.delete()
        return JsonResponse({'status': 'success', 'message': 'Vétérinaire supprimé avec succès.'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})

#-------------- CRUD VACCIN ----------------------------
from .models import Vaccin


def vaccintableau(request):
    rechercher = request.GET.get("rechercher", "")
    if rechercher:
        vaccins = Vaccin.objects.filter(nom_vaccin__icontains=rechercher)
    else:
        vaccins = Vaccin.objects.all()
    return render(request, "bouf/Vaccin_Tableau.html", {"vaccins": vaccins})



def vaccinadd(request):
    if request.method == "POST":
        try:
            Vaccin.objects.create(
                id_individu_id=request.POST.get("id_individu"),
                id_veterinaire_id=request.POST.get("id_veterinaire"),
                nom_vaccin=request.POST.get("nom"),
                description_vaccin=request.POST.get("description"),
                date_vaccin=request.POST.get("date_vaccination")
            )
            messages.success(request, "Vaccin ajouté avec succès")
            return redirect("vaccintableau")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return render(request, "bouf/Vaccin_Add.html", {
        "individus": Individu.objects.all(),
        "veterinaires": Veterinaire.objects.all()
    })


from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def vaccinupdate(request, id):
    vaccin = get_object_or_404(Vaccin, pk=id)
    
    if request.method == "POST":
        try:
            # vaccin.id_individu_id = request.POST.get("id_individu")
            # vaccin.id_veterinaire_id = request.POST.get("id_veterinaire")
            vaccin.nom_vaccin = request.POST.get("nom")
            vaccin.description_vaccin = request.POST.get("description")
            vaccin.date_vaccin = request.POST.get("date_vaccination")
            vaccin.save()
            messages.success(request, "Vaccin mis à jour avec succès")
            return redirect("vaccintableau")
        except Exception as e:
            messages.error(request, f"Erreur lors de la modification: {str(e)}")
    
    return render(request, "bouf/Vaccin_Update.html", {
        "vaccin": vaccin,
        "individus": Individu.objects.all(),
        "veterinaires": Veterinaire.objects.all()
    })


def vaccindelete(request, id):
    if request.method == "POST":
        vaccin = get_object_or_404(Vaccin, pk=id)
        try:
            vaccin.delete()
            messages.success(request, "Vaccin supprimé avec succès.")
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)



#---------------- CRUD TRAITEMENT -------------------#
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Traitement, Individu, Maladie, Veterinaire

def traitementtableau(request):
    traitements = Traitement.objects.select_related('id_individu', 'id_maladie', 'id_veterinaire').all()
    return render(request, "bouf/Traitement_Tableau.html", {"traitements": traitements})

def traitementadd(request):
    if request.method == "POST":
        try:
            Traitement.objects.create(
                id_individu_id=request.POST.get("id_individu"),
                id_maladie_id=request.POST.get("id_maladie"),
                id_veterinaire_id=request.POST.get("id_veterinaire"),
                medicament=request.POST.get("medicament"),
                dose=request.POST.get("dose"),
                date_traitement=request.POST.get("date_traitement")
            )
            messages.success(request, "Traitement ajouté avec succès")
            return redirect("traitementtableau")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return render(request, "bouf/Traitement_Add.html", {
        "individus": Individu.objects.all(),
        "maladies": Maladie.objects.all(),
        "veterinaires": Veterinaire.objects.all()
    })

def traitementupdate(request, id):
    traitement = get_object_or_404(Traitement, pk=id)
    
    if request.method == "POST":
        try:
            traitement.id_individu_id = request.POST.get("id_individu")
            traitement.id_maladie_id = request.POST.get("id_maladie")
            traitement.id_veterinaire_id = request.POST.get("id_veterinaire")
            traitement.medicament = request.POST.get("medicament")
            traitement.dose = request.POST.get("dose")
            traitement.date_traitement = request.POST.get("date_traitement")
            traitement.save()
            messages.success(request, "Traitement mis à jour avec succès")
            return redirect("traitementtableau")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return render(request, "bouf/Traitement_Update.html", {
        "traitement": traitement,
        "individus": Individu.objects.all(),
        "maladies": Maladie.objects.all(),
        "veterinaires": Veterinaire.objects.all()
    })

def traitementdelete(request, id):
    if request.method == "POST":
        traitement = get_object_or_404(Traitement, pk=id)
        try:
            traitement.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=405)



#------ TABLEAU DE BORD ------#



from django.db.models import Sum  # ← TRÈS important à ajouter


def bovin(request):
    nb_clients = Client.objects.count()
    nb_commandes = Commande.objects.count()
    total_stock = StockAliment.objects.aggregate(total=Sum('stock_entree'))['total'] or 0
    nb_troupeaux = Troupeau.objects.count()

    context = {
        "nb_clients": nb_clients,
        "nb_commandes": nb_commandes,
        "total_stock": total_stock,
        "nb_troupeaux": nb_troupeaux,
    }
    return render(request, "bouf/bovin.html", context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Reproduction, Individu, Veterinaire

def reproductiontableau(request):
    reproductions = Reproduction.objects.select_related('id_veterinaire', 'id_femelle', 'id_male').all()
    return render(request, "bouf/Reproduction_Tableau.html", {"reproductions": reproductions})

def reproductionadd(request):
    if request.method == "POST":
        try:
            Reproduction.objects.create(
                id_veterinaire_id=request.POST.get("id_veterinaire"),
                id_femelle_id=request.POST.get("id_femelle"),
                id_male_id=request.POST.get("id_male"),
                date_saillie=request.POST.get("date_saillie"),
                date_diagnostic=request.POST.get("date_Diagnostic"),
                date_prevue=request.POST.get("date_creation"),  # Note: vérifiez le nom du champ
                date_naissance=request.POST.get("date_naissance"),
                etat_veau=request.POST.get("etat_veau")
            )
            messages.success(request, "Reproduction enregistrée avec succès")
            return redirect("reproductiontableau")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return render(request, "bouf/Reproduction_Add.html", {
        "veterinaires": Veterinaire.objects.all(),
        "individus": Individu.objects.all()
    })

def reproductionupdate(request, id):
    reproduction = get_object_or_404(Reproduction, pk=id)
    
    if request.method == "POST":
        try:
            reproduction.id_veterinaire_id = request.POST.get("id_veterinaire")
            reproduction.id_femelle_id = request.POST.get("id_femelle")
            reproduction.id_male_id = request.POST.get("id_male")
            reproduction.date_saillie = request.POST.get("date_saillie")
            reproduction.date_diagnostic = request.POST.get("date_Diagnostic")
            reproduction.date_prevue = request.POST.get("date_creation")
            reproduction.date_naissance = request.POST.get("date_naissance")
            reproduction.etat_veau = request.POST.get("etat_veau")
            reproduction.save()
            messages.success(request, "Reproduction mise à jour avec succès")
            return redirect("reproductiontableau")
        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")
    
    return render(request, "bouf/Reproduction_Update.html", {
        "reproduction": reproduction,
        "veterinaires": Veterinaire.objects.all(),
        "individus": Individu.objects.all()
    })

def reproductiondelete(request, id):
    if request.method == "POST":
        reproduction = get_object_or_404(Reproduction, pk=id)
        try:
            reproduction.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error'}, status=405)


#------------ PDF Passeport de l'Individu   ---------------------
from django.http import HttpResponse
from fpdf import FPDF
from django.templatetags.static import static
from django.conf import settings
import os
from django.contrib.staticfiles import finders
import datetime

def generate_passport_pdf(request, individu_id):
    individu = Individu.objects.select_related('id_troupeau').prefetch_related('vaccinations').get(pk=individu_id)

    # Création du PDF avec des marges personnalisées
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    # Couleurs personnalisées
    pdf.set_draw_color(0, 80, 180)  # Bleu pour les bordures
    pdf.set_fill_color(230, 230, 250)  # Fond bleu clair
    pdf.set_text_color(0, 0, 0)  # Texte noir
    
    # En-tête avec logo et titre
   
    # Trouver le vrai chemin absolu de l'image dans static/
    logo_path = finders.find('images/bovin_4.jpeg')
    if logo_path:  # Assure-toi que le fichier a bien été trouvé
        pdf.image(logo_path, x=10, y=8, w=15)
    else:
        print("Logo non trouvé !")  # Ou lève une exception/log si besoin
    
    # Positionner le texte à droite du logo
    # pdf.set_xy(35, 10)  # Décale un peu à droite et aligne verticalement avec le logo
    # pdf.set_font("Arial", "B", 16)
    # pdf.cell(0, 10, txt="Be-Trafo", ln=False, align='L')  # Texte sur la même ligne

    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, txt="PASSEPORT ANIMAL", ln=True, align='C')
    
    # Ligne de séparation
    pdf.set_draw_color(0, 80, 180)
    pdf.set_line_width(0.5)
    pdf.line(10, 30, 200, 30)
    pdf.ln(15)
    
    # Section Informations de l'individu
    pdf.set_font("Arial", "B", 16)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, txt="INFORMATIONS DE L'ANIMAL", ln=True, fill=True)
    pdf.ln(5)
    
    # Tableau des informations
    pdf.set_font("Arial", size=12)
    col_width = 95
    row_height = 10

    # Ligne 1 : ID & Troupeau
    pdf.cell(col_width, row_height, txt=f"ID: {individu.id_individu}", border=1)
    pdf.cell(col_width, row_height, txt=f"Troupeau: {individu.id_troupeau.nom}", border=1, ln=True)

    # Ligne 2 : Race & Numéro ID
    pdf.cell(col_width, row_height, txt=f"Race: {individu.id_troupeau.race}", border=1)
    pdf.cell(col_width, row_height, txt=f"Numéro ID: {individu.numero_identification}", border=1, ln=True)

    # Ligne 3 : Sexe & Date de naissance
    pdf.cell(col_width, row_height, txt=f"Sexe: {individu.get_sexe_display()}", border=1)
    pdf.cell(col_width, row_height, txt=f"Date naissance: {individu.date_naissance.strftime('%d/%m/%Y')}", border=1, ln=True)

    # Calcul de l’âge
    today = datetime.date.today()
    birth_date = individu.date_naissance

    age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    remaining_months = today.month - birth_date.month - (today.day < birth_date.day)
    if remaining_months < 0:
        remaining_months += 12

    if age_years == 0:
        if remaining_months == 0:
            age_days = (today - birth_date).days
            age_str = f"{age_days} jour(s)"
        else:
            age_str = f"{remaining_months} mois"
    else:
        age_str = f"{age_years} an(s) et {remaining_months} mois"

    # Ligne 4 : Âge & Poids
    pdf.cell(col_width, row_height, txt=f"Âge: {age_str}", border=1)
    pdf.cell(col_width, row_height, txt=f"Poids: {individu.poids} kg", border=1, ln=True)

    # Ligne 5 : État de santé sur toute la ligne
    pdf.cell(0, row_height, txt=f"État santé: {individu.get_etat_sante_display()}", border=1, ln=True)

    # Ligne 6 : Description sur toute la largeur
    pdf.multi_cell(0, row_height, txt=f"Description: {individu.description}", border=1)
    pdf.ln(10)

    
    # Section Vaccinations
    pdf.set_font("Arial", "B", 16)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, txt="VACCINATIONS", ln=True, fill=True)
    pdf.ln(5)
    
    if individu.vaccinations.exists():
        for vaccin in individu.vaccinations.all():
            # Encadré pour chaque vaccination
            pdf.set_fill_color(245, 245, 255)
            pdf.rect(10, pdf.get_y(), 190, 30, style='F')
            pdf.set_xy(15, pdf.get_y() + 5)
            
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, txt=f"Vaccin: {vaccin.nom_vaccin}", ln=True)
            
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 8, txt=f"Date: {vaccin.date_vaccin.strftime('%d/%m/%Y')}", ln=True)
            
            if vaccin.description_vaccin:
                pdf.multi_cell(0, 8, txt=f"Notes: {vaccin.description_vaccin}")
            
            pdf.ln(10)
    else:
        pdf.set_font("Arial", "I", 12)
        pdf.cell(0, 10, txt="Aucune vaccination enregistrée.", ln=True)
    
    # Pied de page
    # pdf.set_y(-20)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, txt=f"Document généré le {datetime.date.today().strftime('%d/%m/%Y')}", align='C')
    
    # Création d'une réponse PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=passeport_individu_{individu.id_individu}.pdf'
    
    # Écriture du PDF dans la réponse
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    response.write(pdf_bytes)

    return response


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import Login  # Remplace par ton modèle si besoin

def add_login(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        identifiant = request.POST.get('identifiant')
        role = request.POST.get('role')
        mot_de_passe = request.POST.get('mot_de_passe')
        verification_mot_de_passe = request.POST.get('verification_mot_de_passe')

        # Vérifications
        if mot_de_passe != verification_mot_de_passe:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('add_login')  # nom de l'url du add

        if len(mot_de_passe) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return redirect('add_login')

        # Vérifier si l'identifiant existe déjà
        if Login.objects.filter(identifiant=identifiant).exists():
            messages.error(request, "Cet identifiant est déjà utilisé. Choisissez-en un autre.")
            return redirect('add_login')

        # Enregistrement
        new_login = Login(
            nom=nom,
            identifiant=identifiant,
            role=role,
            mot_de_passe=make_password(mot_de_passe)  # on hache le mot de passe
        )
        new_login.save()

        messages.success(request, "Utilisateur ajouté avec succès !")
        return redirect('add_login')  # tu peux rediriger ailleurs si tu veux
    else:
        return render(request, 'admin/add.html')
    

from django.shortcuts import render
from .models import Login

def affiche(request):
    utilisateurs = Login.objects.all()
    return render(request, 'admin/affiche.html', {'utilisateurs': utilisateurs})

@require_POST
def supprimer_login(request, id):
    try:
        log = get_object_or_404(Login, pk=id)
        log.delete()
        # messages.success(request, "Login supprimé avec succès")
        return JsonResponse({'status': 'success'})
    except Exception as e:
        messages.error(request, f"Erreur: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

#--------------------- LOGIN ------------------
    
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Login



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # On récupère l'utilisateur avec ce username (peu importe actif ou pas)
            user = Login.objects.get(identifiant=username)
            
            # Ensuite on vérifie s'il est actif
            if not user.est_actif:
                messages.error(request, "Votre compte est inactif. Veuillez contacter l'administrateur.")
                return redirect('login_view')  # Tu rediriges sur la page login
            
            # Si actif, vérifie le mot de passe
            if user.verify_password(password):
                if user.role == 'admin':
                    return redirect('chef')
                elif user.role in ('user', 'gestion_animaux'):
                    return redirect('bovin')

                else:
                    messages.error(request, "Rôle inconnu.")
            else:
                messages.error(request, "Mot de passe incorrect.")
        
        except Login.DoesNotExist:
            messages.error(request, "Identifiant invalide.")
    
    return render(request, 'home.html')


# def admin_chef(request):
#     return render(request, 'admin/chef.html')

# def bovin(request):
#     return render(request, 'bouf/bovin.html')



from django.db.models import F, Sum
from django.db.models.functions import ExtractMonth
import json
from django.utils import timezone

def chef(request):
    nb_client = Client.objects.count()
    nb_commande = CommandeDetail.objects.count()
    nb_indivindu = Individu.objects.count()
    nb_user = Login.objects.count()

    current_year = timezone.now().year  # Ou 2025 pour vos données de test
    
    # Calcul des recettes
    revenue_data = LigneCommande.objects.filter(
        commande__date_commande__year=current_year
    ).annotate(
        month=ExtractMonth('commande__date_commande'),
    ).values('month').annotate(
        total_revenue=Sum(F('quantite') * F('produit__prix_unitaire'))
    ).order_by('month')

    # Calcul des dépenses
    expense_data = StockAliment.objects.filter(
        date_reception__year=current_year
    ).annotate(
        month=ExtractMonth('date_reception'),
    ).values('month').annotate(
        total_expense=Sum(F('stock_entree') * F('prix_aliment'))
    ).order_by('month')

    # Initialisation des tableaux
    monthly_revenue = [0.0] * 12
    monthly_expenses = [0.0] * 12

    # Remplissage des recettes
    for entry in revenue_data:
        monthly_revenue[entry['month'] - 1] = float(entry['total_revenue'] or 0)

    # Remplissage des dépenses
    for entry in expense_data:
        monthly_expenses[entry['month'] - 1] = float(entry['total_expense'] or 0)

    context = {
        "nb_client": nb_client,
        "nb_commande": nb_commande,
        "nb_indivindu": nb_indivindu,
        "nb_user": nb_user,
        "monthly_revenue": json.dumps(monthly_revenue),
        "monthly_expenses": json.dumps(monthly_expenses),
    }
    return render(request, "admin/chef.html", context)

@csrf_exempt
def toggle_actif(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            est_actif = data.get('est_actif')

            utilisateur = Login.objects.get(id=user_id)
            utilisateur.est_actif = est_actif
            utilisateur.save()  # ça met aussi à jour automatiquement date_modification

            status_message = "Utilisateur activé." if est_actif else "Utilisateur désactivé."
            return JsonResponse({'status': 'success', 'message': status_message})
        except Login.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': "Utilisateur introuvable."})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})


from django.shortcuts import render, redirect
from .models import CommandeDetail, Client
from django.contrib import messages
from datetime import date

def commande_detail(request):
    today = date.today().isoformat()
    clients = Client.objects.all()
    
    if request.method == 'POST':
        try:
            client_id = request.POST.get('id_client')
            date_commande = request.POST.get('date_commande')
            
            # Validation
            if not client_id:
                messages.error(request, "Le client est obligatoire")
                return redirect('tableau_commande_detail')
                
            client = Client.objects.get(id_client=client_id)
            
            # Création de la commande
            commande = CommandeDetail.objects.create(
                id_client=client,
                date_commande=date_commande
            )
            
            messages.success(request, "Commande ajoutée avec succès!")
            return redirect('ajouter_ligne_commande')
            
        except Exception as e:
            messages.error(request, f"Une erreur est survenue: {str(e)}")
    
    context = {
        'clients': clients,
        'today': today
    }
    return render(request, "bouf/Command_Delail.html", context)



def tableau_commande_detail(request):
    commandes = CommandeDetail.objects.all().select_related('id_client')
    return render(request, 'bouf/Tableau_CommandeDel.html', {'commandes': commandes})




def commande_detail_delete(request, id_commande):
    if request.method == 'POST':
        commande = get_object_or_404(CommandeDetail, id_commande=id_commande)
        try:
            commande.delete()
            messages.success(request, "La commande a été supprimée avec succès.")
        except Exception as e:
            messages.error(request, f"Erreur lors de la suppression : {str(e)}")
    return redirect('tableau_commande_detail')



#--------------- Ligne de Commande -------------
def tableau_ligne(request):
    return render(request, "bouf/ligne_tableau.html")

def tableau_ligne(request):
    ligne = LigneCommande.objects.all().values()
    return render(request, 'bouf/ligne_tableau.html', {'ligne': ligne})

def ligne_delete(request, id):
    ligne = get_object_or_404(LigneCommande, id_ligne=id)
    if request.method == 'POST':
        ligne.delete()
        messages.success(request, "Ligne supprimée avec succès.")
        return redirect('ligne_tableau')
    return redirect('ligne_tableau')



from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from .models import CommandeDetail, LigneCommande, Produit
from django.conf import settings

def ajouter_ligne_commande(request):
    commandes = CommandeDetail.objects.all().select_related('id_client')
    produits = Produit.objects.filter(date_expiration__gt=timezone.now().date())

    if request.method == 'POST':
        try:
            commande = CommandeDetail.objects.get(pk=request.POST.get('id_commande'))
            client = commande.id_client  # id_client est une instance de Client

            produits_ids = request.POST.getlist('produits[]')
            quantites = request.POST.getlist('quantites[]')

            if not produits_ids or not quantites:
                raise Exception("Veuillez sélectionner au moins un produit et une quantité.")

            lignes_ajoutees = []
            for produit_id, quantite in zip(produits_ids, quantites):
                produit = Produit.objects.get(pk=produit_id)
                quantite_decimal = Decimal(quantite)

                ligne = LigneCommande(
                    commande=commande,
                    produit=produit,
                    quantite=quantite_decimal
                )
                ligne.full_clean()
                ligne.save()
                lignes_ajoutees.append((produit.nom, quantite_decimal, produit.prix_unitaire))

            # Envoi de l'email si l'adresse existe
            if client.email_client:
                total = sum(q * p for _, q, p in lignes_ajoutees)
                contenu = "Bonjour {},\n\nVotre commande a été enregistrée avec succès.\n\n".format(client.nom_client)
                contenu += "Détail de votre commande :\n"
                for nom_produit, qte, prix in lignes_ajoutees:
                    contenu += f"- {nom_produit} : {qte} x {prix} MGA = {qte * prix} MGA\n"
                contenu += f"\nTotal estimé : {total} MGA\n\nMerci pour votre confiance."

                send_mail(
                    subject="Confirmation de votre commande",
                    message=contenu,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email_client],
                    fail_silently=False,
                )

            messages.success(request, "Lignes de commande ajoutées avec succès et email envoyé au client.")
            return redirect('ajouter_ligne_commande')

        except Exception as e:
            messages.error(request, f"Erreur : {str(e)}")

    context = {
        'commandes': commandes,
        'produits': produits
    }
    return render(request, 'bouf/par_ligne.html', context)


from django.http import JsonResponse

def api_stock_produit(request):
    produit_id = request.GET.get('produit_id')
    try:
        produit = Produit.objects.get(pk=produit_id)
        
        if produit.unite_mesure == 'litres':
            stock = Production.objects.filter(id_produit=produit).aggregate(total=Sum('quantite'))['total'] or 0
        elif produit.unite_mesure == 'kg':
            stock = Production.objects.filter(id_produit=produit).aggregate(total=Sum('poids_carcasse'))['total'] or 0
        else:
            return JsonResponse({'error': 'Unité de mesure invalide'})
            
        return JsonResponse({
            'stock': stock,
            'unite': produit.get_unite_mesure_display()
        })
        
    except Produit.DoesNotExist:
        return JsonResponse({'error': 'Produit introuvable'})

def par_ligne(request):
    produits = Produit.objects.all()
    commandes = CommandeDetail.objects.all()
    return render(request, 'bouf/par_ligne.html', {
        'produits': produits,
        'commandes': commandes,
    })

#-------------- Facture ---------------- 
from fpdf import FPDF
from django.http import HttpResponse
from my_app.models import CommandeDetail, LigneCommande, Paiement, Produit
from django.contrib.staticfiles import finders

class PDF(FPDF):
    def header(self):
        # Configuration des couleurs
        self.set_draw_color(34, 139, 34)  # Vert foncé
        self.set_fill_color(245, 245, 245)  # Gris clair
        
        # Logo
        logo_path = finders.find('images/bovin_4.jpeg')
        if logo_path:
            self.image(logo_path, x=10, y=8, w=25)
        
        # En-tête de la société
        self.set_font("Arial", "B", 18)
        self.set_text_color(34, 139, 34)  # Vert foncé
        self.cell(80)
        self.cell(30, 10, "Be-Trafo", 0, 1, "C")
        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 0)  # Noir
        
        # Informations société
        self.set_xy(140, 10)
        self.cell(60, 5, "Adresse: Tulear 601", 0, 2, "R")
        self.cell(60, 5, "Contact: +261 34 00 000 00", 0, 2, "R")
        self.cell(60, 5, "Email: contact@be-trafo.mg", 0, 2, "R")
        self.cell(60, 5, "NIF: 123456789", 0, 2, "R")
        
        # Ligne de séparation
        self.line(10, 40, 200, 40)
        self.ln(15)

    def footer(self):
        self.set_y(-25)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)  # Gris
        self.cell(0, 5, "Merci pour votre confiance !", 0, 1, "C")
        # self.cell(0, 5, "Conditions de paiement: Paiement comptable à la commande", 0, 1, "C")
        self.line(10, 265, 200, 265)
        self.set_y(-15)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def facture_pdf(request, commande_id):
    commande = CommandeDetail.objects.get(pk=commande_id)
    client = commande.id_client
    lignes = LigneCommande.objects.filter(commande_id=commande_id)
    paiement = Paiement.objects.filter(id_commandeDetail_id=commande_id).first()

    pdf = PDF()
    pdf.add_page()
    
    # Section Client
    pdf.set_font("Arial", "B", 12)
    pdf.set_draw_color(34, 139, 34)
    pdf.cell(0, 10, "INFORMATIONS CLIENT", 0, 1)
    
    pdf.set_font("Arial", "", 11)
    pdf.set_fill_color(245, 245, 245)
    pdf.cell(0, 8, f"Nom: {client.nom_client.upper()} {client.prenom_client}", 0, 1, "L", 1)
    pdf.cell(0, 8, f"Adresse: {client.adresse}", 0, 1, "L", 1)
    pdf.cell(0, 8, f"Contact: {client.telephone}", 0, 1, "L", 1)
    pdf.ln(10)

    # Détails Facture
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(34, 139, 34)
    pdf.cell(0, 10, f"FACTURE N°{commande.id_commande}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Date: {commande.date_commande.strftime('%d/%m/%Y')}", 0, 1)
    pdf.ln(8)

    # En-tête du tableau
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(255, 255, 255)  # Texte blanc
    pdf.set_fill_color(34, 139, 34)    # Fond vert
    
    # Colonnes
    pdf.cell(100, 10, "Désignation", 1, 0, "C", 1)
    pdf.cell(30, 10, "Quantité", 1, 0, "C", 1)
    pdf.cell(30, 10, "Prix Unitaire", 1, 0, "C", 1)
    pdf.cell(30, 10, "Total", 1, 1, "C", 1)

    # Contenu du tableau
    pdf.set_text_color(0, 0, 0)  # Réinitialisation texte noir
    pdf.set_fill_color(255, 255, 255)  # Fond blanc
    total_general = 0
    pdf.set_font("Arial", "", 11)
    
    for ligne in lignes:
        produit = Produit.objects.get(pk=ligne.produit_id)
        total = ligne.quantite * produit.prix_unitaire
        total_general += total

        pdf.cell(100, 10, produit.nom, 1)
        pdf.cell(30, 10, f"{ligne.quantite} {produit.unite_mesure}", 1, 0, "C")
        pdf.cell(30, 10, f"{produit.prix_unitaire:,.2f} MGA", 1, 0, "R")
        pdf.cell(30, 10, f"{total:,.2f} MGA", 1, 1, "R")

    # Total général
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(211, 211, 211)  # Gris clair
    pdf.cell(160, 10, "TOTAL GENERAL", 1, 0, "R", 1)
    pdf.cell(30, 10, f"{total_general:,.2f} MGA", 1, 1, "R", 1)
    pdf.ln(15)

    # Paiement
    if paiement:
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(34, 139, 34)
        pdf.cell(0, 10, "INFORMATIONS DE PAIEMENT", 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        
        pdf.cell(40, 8, "Mode de paiement:")
        pdf.cell(0, 8, f"{paiement.get_mode_paiement_display()}", ln=1)
        pdf.cell(40, 8, "Date de paiement:")
        pdf.cell(0, 8, f"{paiement.date_paiement.strftime('%d/%m/%Y')}", ln=1)
        pdf.cell(40, 8, "Montant payé:")
        pdf.cell(0, 8, f"{total_general:,.2f} MGA", ln=1)

    response = HttpResponse(pdf.output(dest='S').encode('latin-1'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=facture_{client.nom_client}_{commande_id}.pdf'
    return response



