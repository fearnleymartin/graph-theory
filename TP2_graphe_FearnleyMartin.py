import bibV3
from imp import reload
reload(bibV3)
from bibV3 import *

import itertools
from files import *

g = tgv2005

#################
# GRAPHES 2-COLORIABLES
#################
def couleurDunVoisin(s):
    voisins = listeVoisins(s)
    if len(voisins)>1:
        for voisin in voisins:
            if couleurSommet(voisin) != 'white':
                return couleurSommet(voisin)
    return 'white'

def testCouleurDunVoisin():
    g=tgv2005
    # check that no sommets are colored in tgv2005
    sommets = listeSommets(g)
    sommetParis = sommetNom(g,'Paris')
    print('color: ' +  couleurSommet(sommetParis) + ', color expected: white')
    #color a sommet and check the function works
    sommetNantes = sommetNom(g,'Nantes')
    colorierSommet(sommetNantes,'blue')
    print('color: ' +  couleurSommet(sommetNantes) + ', color expected: blue')

def couleurDesVoisins(s):
    voisins = listeVoisins(s)
    couleurDesVoisinsList = []
    if len(voisins)>1:
        for voisin in voisins:
            couleurDesVoisinsList.append(couleurSommet(voisin))
    return couleurDesVoisinsList

def testCouleurDesVoisins():
    g=tgv2005
    # check that no sommets are colored in tgv2005
    sommetParis = sommetNom(g,'Paris')
    print(couleurDesVoisins(sommetParis))
    print('expected all white')
    sommetNantes = sommetNom(g,'Nantes')
    sommetBordeaux = sommetNom(g, 'Bordeaux')

    colorierSommet(sommetNantes,'blue')
    colorierSommet(sommetBordeaux, 'red')
    print(couleurDesVoisins(sommetParis))
    print('expected one red, one blue, and others white')

def sommetColoriable(G):
    sommets = listeSommets(G)
    for sommet in sommets:
        if couleurSommet(sommet)=='white' and couleurDunVoisin(sommet)!= 'white':
            return sommet
    return None

def testSommetColoriable():
    g=tgv2005
    print(sommetColoriable(g))
    print('expected None')
    sommetParis = sommetNom(g,'Paris')
    colorierSommet(sommetParis,'blue')
    print(sommetColoriable(g))
    print('expected Lille')


def deuxColoriable(G, c1, c2):
    sommets = listeSommets(G)
    if len(sommets) == 0:
        pass
    else:
        sommetInitial=sommets[0]
        colorierSommet(sommetInitial, c1)
        while sommetColoriable(G) is not None:
            currentSommet = sommetColoriable(G)
            voisinsDeCurrentSommet = listeVoisins(currentSommet)
            couleurPremierVoisin = couleurDunVoisin(currentSommet)
            memeColeur=True
            if couleurPremierVoisin != 'white':
                for voisin in voisinsDeCurrentSommet:
                    if couleurSommet(voisin) != couleurPremierVoisin and couleurSommet(voisin) != 'white':
                        memeColeur=False
            if memeColeur:
                if couleurPremierVoisin == c1:
                    colorierSommet(currentSommet, c2)
                else:
                    colorierSommet(currentSommet, c1)
            else:
                break

def testDeuxColoriable():
    g=construireBipartiComplet(4, 4)
    deuxColoriable(g,'blue','red')
    dessiner(g)
    # le graph est bien colore par deux couleurs


# Question 6
# Vu que les deux parties de graphes ne sont pas relies entre elles,
# On ne parviendra jamais a trouver  un sommet non colorie avec un voisin colorie dans la partie de graphe qui ne possede pas le sommet initial
# Du coup, on ne colorera qu'une partie du graphe

# Question 7
# Il faudrait par exemple colorier un sommet initiaux dans chaque partie du graphe connexe
# Cela necessite d' identifier les sous graphes connexes

########################
# LE CENTRE D' UNE GRILLE CARREE
########################

def findCornersAndEdges(G):
    '''
    :param G:
    :return: sommets qui sont au bord de la grille
    '''
    sommets = listeSommets(G)
    corners = []
    edges = []
    for sommet in sommets:
        if len(listeVoisins(sommet)) == 2:
            corners.append(sommet)
        if len(listeVoisins(sommet)) == 3:
            edges.append(sommet)

    return corners + edges

def listeDeVoisinsNonColorie(s):
    '''
    :param s:
    :return: les voisins de s qui ne sont pas colories
    '''
    voisinsNonColories = []
    voisins = listeVoisins(s)
    for voisin in voisins:
        if couleurSommet(voisin) == 'white':
            voisinsNonColories.append(voisin)
    return voisinsNonColories

def findCornersAndEdgesNonColories(G):
    '''
    :param G:
    :return: les sommets qui sont au bord de la grille formee par les sommets non colories
    '''
    sommets= listeSommets(G)
    nonColoredCorners = []
    nonColoredEdges = []
    for sommet in sommets:
        if couleurSommet(sommet) == 'white':
            if len(listeDeVoisinsNonColorie(sommet)) == 2:
                nonColoredCorners.append(sommet)
            if len(listeDeVoisinsNonColorie(sommet)) == 3:
                nonColoredEdges.append(sommet)
    return nonColoredCorners + nonColoredEdges


def colorList(sommets, couleur):
    '''
    colorie chaque sommet d' une liste de sommets
    :param sommets:
    :param couleur:
    :return:
    '''
    for sommet in sommets:
        colorierSommet(sommet, couleur)

def colorGrid(G):
    '''
    colorie la grille couche par couche. Colorie d' abord la couche exterieur en noir, ensuite la prochaine couche en noir
    et ainsi de suite jusqu' a trouver le centre
    :param G: une grille carree
    :return:
    '''
    sommetsExterieurs = findCornersAndEdges(G)
    colorList(sommetsExterieurs, 'black')
    while len(findCornersAndEdgesNonColories(G)) > 0:
        nonColoredSommetsExterieurs = findCornersAndEdgesNonColories(G)
        if len(nonColoredSommetsExterieurs) == 4:
            break
        else:
            colorList(nonColoredSommetsExterieurs, 'black')

def findCenter(G):
    '''
    :param G: une grille carree
    :return: une liste des sommets au centre de la grille
    '''
    colorGrid(G)
    sommets = listeSommets(G)
    center = []
    for sommet in sommets:
        if couleurSommet(sommet) == 'white':
            center.append(sommet)
    return center

def testFindCenter(n):
    '''
    colors grid, and prints the list of center nodes
    :param n: size of square grid
    :return:
    '''
    g = construireGrille(n, n)
    colorGrid(g)
    dessiner(g)
    print(findCenter(g))

#############################
# Stables dans un graphe
#############################
def stable(G):
    '''
    :param G:
    :return: True si les osmmets marques forment un stable, False sinon
    '''
    # on recupere la liste des sommets marques et des sommets non marques
    sommetsMarques = []
    sommetsNonMarques =[]
    sommets = listeSommets(G)
    for sommet in sommets:
        if estMarqueSommet(sommet):
            sommetsMarques.append(sommet)
        else:
            sommetsNonMarques.append(sommet)

    # On verifie la condition (u,v appartient T => {u,v} n' appartient pas a A)
    # On renvoie False si elle n' est pas verifiee
    couplesSommets = itertools.combinations(sommetsMarques, 2)
    for coupleSommets in couplesSommets:
        if coupleSommets[1] in listeVoisins(coupleSommets[0]):
            return False
    # C' est un stable et On colorie les sommets marques
    colorList(sommetsMarques,'blue')
    return True


def stableMaximum(G):
    '''
    :param G:
    :return: True si G est un stable maximum, False sinon
    '''
    # on recupere la liste des sommets marques et des sommets non marques
    sommetsMarques = []
    sommetsNonMarques = []
    sommets = listeSommets(G)
    for sommet in sommets:
        if estMarqueSommet(sommet):
            sommetsMarques.append(sommet)
        else:
            sommetsNonMarques.append(sommet)

    # On verifie la condition (u,v appartient T => {u,v} n' appartient pas a A)
    # On renvoie False si elle n' est pas verifiee
    couplesSommets = itertools.combinations(sommetsMarques, 2)
    for coupleSommets in couplesSommets:
        if coupleSommets[1] in listeVoisins(coupleSommets[0]):
            return False
    # On verifie que le stable est maximum avec la condition:
    # tous les sommets w de T ont au moins un voisin dans T
    # On renvoie False si ce n' est pas le cas
    for sommet in sommetsNonMarques:
        voisinsSommet = listeVoisins(sommet)
        if set(voisinsSommet).isdisjoint(sommetsMarques):
            return False

    # c' est un  stable maximum, on colorie les sommets marques
    colorList(sommetsMarques, 'blue')
    return True

def testStable():
    # create a test graph
    g = construireGraphe (
        [ ['D', 'A', 'B', 'C', 'E'],
          ['A','C']
        ], "testGraph")
    # dessiner(g)
    # (B,D,E) is a stable
    # (A,D,E) is not a stable
    #test 1: (B,D,E)
    marquerSommet(sommetNom(g,'B'))
    marquerSommet(sommetNom(g,'D'))
    marquerSommet(sommetNom(g,'E'))
    print('(B,D,E) is a stable, ' + str(stable(g)))
    #test 2 (A,D,E)
    demarquerSommet(sommetNom(g,'B'))
    marquerSommet(sommetNom(g,'A'))
    print('(A,D,E) is not a stable, ' + str(stable(g)))

def testStableMaximum():
    # same graph as before
    # (B,D,E) is a stable maximum
    # (B,D) is a stable but is not maximum
    g = construireGraphe (
        [ ['D', 'A', 'B', 'C', 'E'],
          ['A','C']
        ], "testGraph")
    #test 1
    marquerSommet(sommetNom(g,'B'))
    marquerSommet(sommetNom(g,'D'))
    marquerSommet(sommetNom(g,'E'))
    print('(B,D,E) is a stable maximum, ' + str(stableMaximum(g)))
    demarquerSommet(sommetNom(g,'B'))
    print('(B,D) is a stable but is not maximum, ' + str(stableMaximum(g)))


#########################
# PARCOURS ET COLORATION
#########################

def isCircular(G):
    '''
    pas encore fini
    :param G: graphe
    :return: True si le graphe est circulaire, False sinon
    '''
    sommets = listeSommets(G)
    initialSommet = sommets[0]
    q = emptyQueue()
    q=enqueue(initialSommet, q)

    while True:
        currentSommet = q[-1]
        voisins = listeVoisins(currentSommet)
        if len(voisins)>2:
            return False
        elif len(voisins)<1:
            return False
        else:
            for voisin in voisins:


def testIsCircular():
    # create circular graph
    g = construireGraphe (
        [ ['A','B'],
          ['B','C'],
          ['C','D'],
          ['D','E'],
          ['E','A']
        ], "circularGraph")
    # dessiner(g)
    return isCircular(g)












