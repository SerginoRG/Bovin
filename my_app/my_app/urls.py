"""
URL configuration for my_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from .views import (
    bovin,
    troupeauadd, troupeautableau, ajouter_troupeau, troupeau_tableau,
    modifier_troupeau, supprimer_troupeau,
    aliment_add, ajouter_aliment, aliment_tableau, modifier_aliment, supprimer_aliment,
    stocktableau, stockadd, ajouter_stock_aliment,supprimer_stock,modifier_stock,rationtableau,
    rationadd,supprimer_ration,modifier_ration, individutableau,individuadd,individuupdate,
    individudelete,produittableau,produitadd,produitupdate,produitdelete,productiontableau,
    productionadd , productionupdate , productiondelete, individus_par_produit,clienttableau,
    clientadd ,  clientupdate, clientdelete, commandetableau ,commandeadd,
    commandeupdate, commandedelete, stock_produit,paiementtableau,paiementadd, paiementdelete,maladietableau,maladieadd, maladieedit, maladiesupprimer,veterinairetableau,veterinaireadd,
    veterinaireupdate,veterinairesupprimer,vaccintableau,vaccinadd,vaccinupdate,vaccindelete,
    traitementtableau,traitementadd,traitementupdate,traitementdelete,reproductiontableau
    ,reproductionadd,reproductionupdate,reproductiondelete,generate_passport_pdf, chef,addchef,add_login,affiche,
    supprimer_login,login_view,toggle_actif,commande_detail,tableau_commande_detail,commande_detail_delete,
    par_ligne,ajouter_ligne_commande,facture_pdf,tableau_ligne,ligne_delete
)

urlpatterns = [
    # Accueil
    # path("", home, name="home"),
    path('', login_view, name='login_view'),  # Page de connexion
    # path('admin/chef/', admin_chef, name='admin_chef'),  # Page admin
    # path('bouef/bovin/', bouef_bovin, name='bouef_bovin'),  # Page utilisateu

    # Page bovin
    # path("bouf/bovin", bovin, name="bovin"),
    path("bouf/bovin/", bovin, name="bovin"),

    #Page chef
   
    path("admin/chef/", chef, name="chef"),


    path("admin/chef/add/", addchef, name="addchef"),
    path("admin/login/add/", add_login, name="add_login"),

    path("admin/affiche/", affiche, name="affiche"),
    path('toggle-actif/', toggle_actif, name='toggle_actif'),
    path("admin/affiche/<int:id>/", supprimer_login, name="supprimer_login"),

    
    

    


    # -------------------- TROUPEAU --------------------
    # Formulaire ajout
    path("bouf/troupeauadd", troupeauadd, name="troupeauadd"),
    # Formulaire de traitement
    path('ajouter-troupeau/', ajouter_troupeau, name='ajouter_troupeau'),
    # Affichage tableau
    path("bouf/troupeautableau", troupeautableau, name="troupeautableau"),
    path('troupeaux/', troupeau_tableau, name='troupeautableau'),

    # Modifier
    re_path(r"bouf/troupeauupdate/(?P<id_troupeau>[-\w]+)/", modifier_troupeau, name="modifier_troupeau"),
    # Supprimer
    re_path(r"supprimer/(?P<id_troupeau>[-\w]+)/", supprimer_troupeau, name='supprimer_troupeau'),

    # -------------------- ALIMENT --------------------

    path("bouf/aliments/", aliment_tableau, name="aliment_tableau"),
    path("bouf/aliment/add/", aliment_add, name="aliment_add"),
    path("bouf/aliment/ajouter/", ajouter_aliment, name="ajouter_aliment"),
    path("bouf/aliment/update/<str:id_aliment>/", modifier_aliment, name="modifier_aliment"),
    path("bouf/aliment/delete/<str:id_aliment>/", supprimer_aliment, name="supprimer_aliment"),

    # -------------------- STOCK ALIMENT --------------------
    path("bouf/stocks/", stocktableau, name="stocktableau"),
    path("bouf/stock/add/", stockadd, name="stockadd"),
    path("bouf/stock/ajouter/", ajouter_stock_aliment, name="ajouter_stock_aliment"),
    path("bouf/stock/delete/<int:id_stock>/", supprimer_stock, name="supprimer_stock"),
    path("bouf/stock/update/<int:id_stock>/", modifier_stock, name="modifier_stock"),

    #--------------------- RATION ALIMENT ---------------------- 
    
    path("bouf/rations/", rationtableau, name="rationtableau"),
    path("bouf/rations/add", rationadd, name="rationadd"),
    path('rations/<int:id_ration>/delete/', supprimer_ration, name='supprimer_ration'),
    path('rations/<int:id_ration>/edit/', modifier_ration, name='modifier_ration'),


    #-------------------- INDIVIDU ------------------------
    
    path("bouf/individus/", individutableau, name="individutableau"),
    path("bouf/individus/add", individuadd, name="individuadd"),
    path("bouf/individus/update/<int:id_individu>/", individuupdate, name="individuupdate"),
    path("bouf/individus/delete/<int:id_individu>/", individudelete, name="individudelete"),

    #-------------------- PRODUIT ----------------------
    path("bouf/produits/", produittableau, name="produittableau"),
    path("bouf/produits/add", produitadd, name="produitadd"),
    path("bouf/produits/update/<int:id_produit>/", produitupdate, name="produitupdate"),
    path("bouf/produits/delete/<int:id_produit>/", produitdelete, name="produitdelete"),

    #------------------ PRODUCTION -----------------
    path("bouf/productions/", productiontableau, name="productiontableau"),
    path("bouf/productions/add", productionadd, name="productionadd"),
    path("bouf/productions/update/<int:id_production>/", productionupdate, name="productionupdate"),
    path("bouf/productions/delete/<int:id_production>/", productiondelete, name="productiondelete"),
    path("bouf/api/individus-par-produit/", individus_par_produit, name="individus_par_produit"),

    #------------------------ CLIENT -------------------------
    path("bouf/clients/", clienttableau, name="clienttableau"),
    path("bouf/clients/add/", clientadd, name="clientadd"),
    path("bouf/clients/update/<int:id_client>/", clientupdate, name="clientupdate"),
    path("bouf/clients/delete/<int:id_client>/", clientdelete, name="clientdelete"),

    #--------------------- COMMANDE ---------------------------
    path("bouf/commandes/", commandetableau, name="commandetableau"),
    path("bouf/commandes/add/", commandeadd, name="commandeadd"),
    path("bouf/commandes/update/<int:id_commande>/", commandeupdate, name="commandeupdate"),
    path("bouf/commandes/delete/<int:id_commande>/", commandedelete, name="commandedelete"),
    path("bouf/api/stock-produit/", stock_produit, name="stock_produit"),

    #-------------------- PAIEMENT -------------------------------
    path("bouf/paiements/", paiementtableau, name="paiementtableau"),
    path("bouf/paiements/add/", paiementadd, name="paiementadd"),
    # path("bouf/paiements/update/<int:id_paiement>/", paiementupdate, name="paiementupdate"),
    path("bouf/paiements/delete/<int:id_paiement>/", paiementdelete, name="paiementdelete"),
    

      #---------Facture ----------
    path('bouf/facture/<int:commande_id>/', facture_pdf, name='facture_pdf'),

    #------------------------MALADIE ---------------------------
    path("bouf/maladies/", maladietableau, name="maladietableau"),
    path("bouf/maladies/add/", maladieadd, name="maladieadd"),
    path("bouf/maladies/edit/<int:id>/", maladieedit, name="maladieedit"),
    path("bouf/maladies/delete/<int:id>/", maladiesupprimer, name="maladiesupprimer"),

    #---------------------VETERINAIRE ---------------------------
    path("bouf/veterinaires/", veterinairetableau, name="veterinairetableau"),
    path("bouf/veterinaires/add/", veterinaireadd, name="veterinaireadd"),
    path("bouf/veterinaires/update/<int:id>/", veterinaireupdate, name="veterinaireupdate"),
    path("bouf/veterinaires/delete/<int:id>/", veterinairesupprimer, name="veterinairesupprimer"),

    #---------------------- VACCIN ---------------------------
    path("bouf/vaccins/", vaccintableau, name="vaccintableau"),
    path("bouf/vaccins/add/", vaccinadd, name="vaccinadd"),
    path("bouf/vaccins/update/<int:id>/", vaccinupdate, name="update_vaccin"),
    path("bouf/vaccins/delete/<int:id>/", vaccindelete, name="delete_vaccin"),

    #--------------------- TRAITEMENT ---------------------------
    path("bouf/traitements/", traitementtableau, name="traitementtableau"),
    path("bouf/traitements/add/", traitementadd, name="traitementadd"),
    path("bouf/traitements/update/<int:id>/", traitementupdate, name="traitementupdate"),
    path("bouf/traitements/delete/<int:id>/", traitementdelete, name="traitementdelete"),

    #---------------- REPRODUCTION ---------------------------
    path("bouf/reproductions/", reproductiontableau, name="reproductiontableau"),
    path("bouf/reproductions/add/", reproductionadd, name="reproductionadd"),
    path("bouf/reproductions/update/<int:id>/", reproductionupdate, name="reproductionupdate"),
    path("bouf/reproductions/delete/<int:id>/", reproductiondelete, name="reproductiondelete"),
    
  
    #------------- PDF Passort Individu ----------
    path('pdf/individu/<int:individu_id>/', generate_passport_pdf, name='generate_passport_pdf'),


    #--------------- Commande Delail -------
    path("bouf/Commande-Detail/", commande_detail, name="commande_detail"),
    path('bouf/commandes-detail/', tableau_commande_detail, name='tableau_commande_detail'),
    path('commandes-detail/delete/<int:id_commande>/', commande_detail_delete, name='commande_detail_delete'),
    
    #--------PAR ligne -----------
    path("bouf/par-ligne/", par_ligne , name="par_ligne"),
    # path("par-ligne/add/", ajouter_ligne_commande , name="ajouter_ligne_commande"),
    path('bouf/ajouter-ligne/', ajouter_ligne_commande, name='ajouter_ligne_commande'),
    path('bouf/ligne/', tableau_ligne, name='ligne_tableau'),
    path('bouf/ligne/delete/<int:id>/', ligne_delete, name='ligne_delete'),


  



    




]
