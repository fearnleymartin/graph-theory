from graphV3 import *
import sys

if sys.hexversion < 3 << 24:
    print("bibV3 ne fonctionne qu'avec python 3, pas avec python 2")
    sys.exit(1)

fig22 = construireGraphe (
    [ ['A', 'B', 'A', 'C', 'D'],
      ['B', 'B'], # boucle
      ['D', 'D', 'D'] # boucles
    ], "fig22")

# Construction ad hoc pour indiquer a Graphviz (algo 'neato')
# les longueurs des aretes
def _makePetersen ():
    g = construireGraphe (
        [ ['A', 'B', 'C', 'D', 'E', 'A'],
          ['a', 'c', 'e', 'b', 'd', 'a'],
          ['A', 'a'],
          ['B', 'b'],
          ['C', 'c'],
          ['D', 'd'],
          ['E', 'e']
        ], "Petersen")
    # Semicolons aid readability but are not required (dotguide.pdf)
    # start = germe du generateur aleatoire pour le placement initial des sommets
    # valeurs OK au CREMI [0, 12, 16, 18, 23, 24, 30, 33]
    # start = 4 interessant aussi
    if plateforme == 'Windows':
        g.drawopts = 'edge [len = 2]'
    else:
        g.drawopts = 'start = 23; edge [len = 2]'
    for i in range (5):
        s = sommetNumero (g, i)
        a = areteNumero (s, 2)
        a.drawopts = '[len = 1]'
    return g

Petersen = _makePetersen ()
#print(petersen)

Koenigsberg = construireGraphe (
    [ ['A', 'B', 'C', 'D', 'B', 'A', 'D'],
      ['B', 'C']
    ], "Koenigsberg")
Koenigsberg.drawopts = 'rankdir=LR'





# Construction en etoile: Paris, Nantes, Lyon, etc. sont les voisins de Lille
# -> dernier parametre = False
# Les etiquettes des aretes ne servent a rien mais ne mangent pas de pain
tgv2005 = construireGraphe (
    [["Lille",
      ["Paris", "1h00"], ["Nantes", "4h10"], ["Lyon", "2h50"],
      ["Bordeaux", "5h00"], ["Toulouse", "8h20"],
      ["Marseille", "4h30"], ["Montpellier", "4h40"]],
     ["Paris",
      ["Nantes", "2h00"], ["Lyon", "1h55"], ["Bordeaux", "2h55"],
      ["Marseille", "2h56"], ["Montpellier", "3h15"],
      ["Toulouse", "5h14"]],
     ["Nantes", ["Lyon", "4h20"], ["Marseille", "6h20"]],
     ["Lyon",
      ["Toulouse", "4h30"], ["Marseille", "1h20"],
      ["Montpellier", "1h45"]],
     ["Bordeaux", ["Toulouse", "2h10"]],
     ["Toulouse", ["Montpellier", "2h16"]],
     ["Strasbourg"]
    ], "tgv2005", chemins = False)


hypercubeDim3 = construireGraphe (
    [['v0', 'v1', 'v3', 'v2', 'v0', 'v4', 'v5', 'v6', 'v7', 'v4'],
    ['v1', 'v5'],
    ['v3', 'v6'],
    ['v2', 'v7']], "hypercubeDim3")


# hypercubeDim3 = construireGraphe ([
#  ["v0", "v1"]
#  ["v0", "v2"]
#  ["v0", "v4"]
#  ["v1", "v5"]
#  ["v1", "v3"]
#  ["v2", "v3"]
#  ["v2", "v7"]
#  ["v3", "v6"]
#  ["v6", "v5"]
#  ["v5", "v4"]
#  ["v4", "v7"]
#  ["v7", "v6"]],
# "hypercubeDim3", chemins = False)



# Construction en etoile: Espagne, Belgique, etc. sont les voisins de France
# -> dernier parametre = False
# Attention: Graphviz ne supporte pas les lettres accentuees !
# Les numeros des couches font reference a l'algorithme 'dot'
Europe = construireGraphe ( [
    ["Portugal","Espagne"],     # couches 0 et 1
    ["France", "Espagne"],      # couche 2
    ["Belgique", "France"],     # couche 3
    ["Pays Bas", "Belgique"],   # couche 4
    ["Allemagne", "France", "Belgique", "Pays Bas"],    # couche 5
    ["Danemark", "Allemagne"],  # couche 6
    ["Pologne", "Allemagne"],   # couche 6
    ["Italie", "France"],       # couche 3
    ["Autriche", "Allemagne", "Italie"],    #couche 6
    ["Tchequie", "Pologne", "Allemagne", "Autriche"],   # couche 7
    # ce qui suit est la verite, mais 'dot' fait alors plonger
    # le Danemark au milieu du graphe, too bad
    ["Slovaquie", "Tchequie", "Autriche", "Pologne"],   # couche 8
    ["Hongrie", "Autriche", "Slovaquie"],   # couche 9
    ["Ukraine", "Pologne", "Slovaquie", "Hongrie"], # couche 10
    ["Roumanie", "Hongrie", "Ukraine"],     # couche 11
    ["Angleterre", "Pays de Galles", "Ecosse"],
    ["Irlande"],
    ["Finlande", "Suede", "Norvege"],
    ["Suede", "Norvege"] ], "Europe", chemins = False)

Europe.drawopts = 'rankdir=LR ratio=.5 node[shape=box style=rounded]'

graphes = [tgv2005, fig22, Europe, Koenigsberg, Petersen, hypercubeDim3]

############# A partir d'ici graphes graphes parametres ###########
#############   construits sur des modeles reguliers    ###########

# Exemple: prefixer ([0, 1, 2, ...], 's') = ['s0', 's1', 's2', ...]
# Fonctionne aussi bien pour les listes de listes

# Attention: le premier sommet doit etre 's0'
# a cause de la fonction sommetNumero

def prefixer (paths, prefix):
    e = []
    for p in paths:
        if type (p) == type ([]):
            e.append (prefixer (p, prefix))
        else:
            e.append (prefix + str (p))
    return e

# Graphes complets

def _complet (n):
    a = []
    for i in range (1, n):
        a.append (list (range (i, -1, -1)))
    return a

def construireComplet (n):
    g = prefixer (_complet (n), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'K' + str (n)
    g = construireGraphe (g, nom, chemins = False)
    # pour l'algo 'neato' (mais le bon algo ici est 'circo')
    g.drawopts = 'edge [len = 2]'
    return g

# Graphes bipartis complets
def _biclique (m, n):
    a = []
    for i in range (m):
        a.append ([i] + list(range (m, m + n)))
    return a

def construireBipartiComplet (m, n):
    g = prefixer (_biclique (m, n), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'K' + str (m) + 'x' + str(n)
    g = construireGraphe (g, nom, chemins = False)
    # pour l'algo 'neato'
    g.drawopts = 'edge [len = 2]'
    return g

# Grilles

def _grille (m, n):
    lignes = []
    debut = 0
    for i in range (m):
        fin = debut + n
        lignes.append (list(range (debut, fin)))
        debut = fin
    for j in range (n):
        lignes.append (list(range (j, fin, n)))
    return lignes

def construireGrille (m, n):
    g = prefixer (_grille (m, n), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'grille' + str (m) + 'x' + str(n)
    g = construireGraphe (g, nom)
    return g

# Triangles

def _triangle (n):
    lignes = []
    debut = 0
    for i in range (n):
        fin = debut + i + 1
        u = list (range (debut, fin))
        lignes.append (u)
        debut = fin
    debut = -1
    for i in range (n - 1):
        u = []
        debut = debut + i + 1
        k = debut
        for j in range (i, n):
            u.append (k)
            k = k + j + 1
        lignes.append (u)
    debut = 0
    for i in range (n - 1):
        u = []
        debut = debut + i
        k = debut
        for j in range (i, n):
            u.append (k)
            k = k + j + 2
        lignes.append (u)
    return lignes

def construireTriangle (n):
    g = prefixer (_triangle (n), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'triangle' + str (n)
    g = construireGraphe (g, nom)
    # specifier le rapport hauteur / largeur pour l'algo 'dot'
    # perturbe legerement l'algo 'neato' 
    g.drawopts = "ratio=1.155"  # 2 / sqrt(3)
    return g

# Arbres (complets)

def _arbre (degre, hauteur, origine = 0):
    a = []
    if hauteur == 0:
        return []
    d = degre ** hauteur
    d = (d - 1) // (degre - 1)
    j = origine + 1
    for i in range (degre):
        a.append ([origine, j])
        a = a + _arbre (degre, hauteur - 1, j)
        j = j + d
    return a

def construireArbre (degre, hauteur):
    g = prefixer (_arbre (degre, hauteur), 's')
    # le 'nom' d'un graphe (label) sert aussi de nom de fichier
    # pour les dessins, eviter les blancs, etc
    nom = 'arbre' + str (degre) + 'x' + str(hauteur)
    g = construireGraphe (g, nom)
    return g

# Solides platoniciens

# autre description de K4
tetraedre = construireGraphe (
    [ ['A', 'B', 'C', 'A', 'D', 'B'], ['C', 'D'] ],
    'tetraedre')

# 6 faces, 8 sommets et 12 aretes
cube = construireGraphe (
    [ ['A', 'B', 'C', 'D', 'A'],
      ['a', 'b', 'c', 'd', 'a'],
      ['A', 'a'],
      ['B', 'b'],
      ['C', 'c'],
      ['D', 'd']
    ], 'cube')
cube.drawopts = 'edge [len = 2]'

octaedre = construireGraphe (
    [ ['A', 'B', 'C', 'D', 'A'],
      ['A', 'E', 'C', 'F', 'A'],
      ['B', 'E', 'D', 'F', 'B']
    ], 'octaedre')
octaedre.drawopts = 'edge [len = 2]'

# 12 faces, 20 sommets et 30 aretes
def _dodecaedre ():
    u = [list (range (20))]
    u = u + [[1, 9], [2, 11], [3, 13], [4, 0, 7]]
    u = u + [[5, 14], [6, 16], [8, 17], [10, 18], [12, 19, 15]]
    return u

dodecaedre = construireGraphe (
    prefixer (_dodecaedre (), 's'), 'dodecaedre')
dodecaedre.drawopts = 'edge [len = 2]'

def _icosaedre ():
    u = [list (range (12))]
    u.append ([2, 0, 3, 8, 11, 6, 1, 5, 0, 4, 9, 3])
    u = u + [[1, 7, 2, 8], [4, 10, 5], [6, 10], [7, 11, 9]]
    return u

icosaedre = construireGraphe (
    prefixer (_icosaedre (), 's'), 'icosaedre')
icosaedre.drawopts = 'edge [len = 2]'

graphesPlanairesReguliers = [tetraedre, cube, octaedre, dodecaedre, icosaedre]

#dessinerGraphe(tgv2005)

#print ("bibV3.py")

