from graphV3 import *

#importez ce fichier comme vous le faisiez avec bibV3
#ou copiez la ligne de construction du graphe dans votre fichier
#(dans ce dernier cas, ajouter l'import de graphV3 dans votre fichier)


#graphe construit automatiquement à partir de TGV2005 de bibV3,
#en modifiant les arêtes pour avoir des temps en minutes (caster en int pour récupérer la valeur à partir de nomSommet())
#et en le rendant connexe (suppression de Strasbourg)
tgv2005_min = construireGraphe( [['Lille', ['Paris', '60'], ['Nantes', '250'], ['Lyon', '170'], ['Bordeaux', '300'], ['Toulouse', '500'], ['Marseille', '270'], ['Montpellier', '280']], ['Paris', ['Nantes', '120'], ['Lyon', '115'], ['Bordeaux', '175'], ['Marseille', '176'], ['Montpellier', '195'], ['Toulouse', '314']], ['Nantes', ['Lyon', '260'], ['Marseille', '380']], ['Lyon', ['Toulouse', '270'], ['Marseille', '80'], ['Montpellier', '105']], ['Bordeaux', ['Toulouse', '130']], ['Toulouse', ['Montpellier', '136']]] , "tgv2005_min", chemins = False)

