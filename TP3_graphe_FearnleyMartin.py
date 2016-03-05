import bibV3
from imp import reload
reload(bibV3)
from bibV3 import *
from tgv2005_min import tgv2005_min
g=tgv2005_min

#####################
# PLUS COURT CHEMIN
#####################

def argmin(dict, temporaire):
    '''
    :param dict: le dict des distances {'sommet':distance}
    :param temporaire:
    :return: le sommet dont la distance est le plus petit (et qui est compris dans temporaire)
    '''
    min=10000000000
    sommet_associe = None
    for el in dict:
        if (dict[el] < min) and (el in temporaire):
            min = dict[el]
            sommet_associe = el
    return sommet_associe

def testargmin():
    dict = {'s1':3,'s2':2,'s3':4}
    ## should return s2
    return argmin(dict)

def Dijkstra(G, start, end=None):
    '''
    :param G: graphe
    :param start: sommet de depart
    :param end: sommet de fin (facultatif)
    :return: dictionnaire distance {'sommet':distance} et dictionnaire aretesEmpruntesParSommet
    {'sommet':[liste des aretes pour aller a ce sommet[]}
    '''
    # initialiser le tableau distance de taille n
    distance = {}
    # distance[i] = infinity
    X = listeSommets(G)
    for s in X:
        distance[s]=1000000
    distance[start]=0
    # initialiser tableau qui stocke les aretes empruntes pour le plus court chemin jusqua chaque sommet
    aretesEmpruntesParSommet={}
    for s in X:
        aretesEmpruntesParSommet[s]=[]
    # initialiser la liste temporaire
    temporaire =[]
    # poser temporaire = X
    for s in X:
        temporaire.append(s)
    # tant que temporaire 6= ; faire
    while temporaire != []:
        # chercher i = argmin { distance[j] : j appartient a temporaire}
        i = argmin(distance, temporaire)
        # poser temporaire = temporaire prive de i
        temporaire.remove(i)
        # pour tout j 2 V+(i) tel que j 2 temporaire faire
        successeurs = listeVoisins(i)
        for j in successeurs:
            if j in temporaire:
                # si distance[j] > distance[i] + cij
                # recuperation de l'arete ij et de la distance cij
                aretesDe_i =listeAretesIncidentes(i)
                for arete in aretesDe_i:
                    end = arete.end
                    start = arete.start
                    if arete.end == j or arete.start == j:
                        ij = arete
                        cij = int(nomArete(arete))
                if distance[j] > distance[i] + cij:
                    distance[j] = distance[i]+cij
                    aretesEmpruntesParSommet[j]=aretesEmpruntesParSommet[i]+[ij]
    return (distance, aretesEmpruntesParSommet)

def testDijkstra():
    g=tgv2005_min
    Bordeaux = sommetNom(g,'Bordeaux')
    for ville in Dijkstra(g,Bordeaux)[0].keys():
        print('Shortest distance to ' + nomSommet(ville) + ' is ' + str(Dijkstra(g,Bordeaux)[0][ville]))
    # print(Dijkstra(g,Bordeaux)[0])
    for ville in Dijkstra(g,Bordeaux)[1].keys():
        print('The shortest path to ' + nomSommet(ville) + ' is: ')
        for arete in Dijkstra(g,Bordeaux)[1][ville]:
            print(arete)

def shortestPath(G, start, end):
    '''

    :param G: graphe
    :param start: sommet de depart
    :param end: sommet de fin
    :return: la distance du plus court chemin entre start et end, et une liste des aretes empruntes pour y arriver
    '''
    # initialiser le tableau distance de taille n
    distance = {}
    # distance[i]   = infinity
    X = listeSommets(G)
    for s in X:
        distance[s]=1000000
    distance[start]=0
    # initialiser tableau qui stocke les aretes empruntes pour le plus court chemin jusqua chaque sommet
    aretesEmpruntesParSommet={}
    for s in X:
        aretesEmpruntesParSommet[s]=[]
    # initialiser la liste temporaire
    temporaire =[]
    # poser temporaire = X
    for s in X:
        temporaire.append(s)
    # tant que temporaire 6= ; faire
    while temporaire != []:
        # chercher i = argmin { distance[j] : j appartient a temporaire}
        i = argmin(distance, temporaire)
        # poser temporaire = temporaire prive de i
        temporaire.remove(i)
        # pour tout j 2 V+(i) tel que j 2 temporaire faire
        successeurs = listeVoisins(i)
        for j in successeurs:
            if j in temporaire:
                # si distance[j] > distance[i] + cij
                aretesDe_i =listeAretesIncidentes(i)
                for arete in aretesDe_i:
                    if arete.end ==j or arete.start == j:
                        ij = arete
                        cij = int(nomArete(arete))
                if distance[j] > distance[i] + cij:
                    distance[j] = distance[i]+cij
                    aretesEmpruntesParSommet[j]=aretesEmpruntesParSommet[i]+[ij]

    for arete in aretesEmpruntesParSommet[end]:
        marquerArete(arete)

    return (distance[end], aretesEmpruntesParSommet[end])

def testShortestPath():
    g = tgv2005_min
    # Bordeaux = sommetNom(g,'Bordeaux')
    # Montpellier = sommetNom(g,'Montpellier')
    # print(shortestPath(g,Bordeaux,Montpellier))
    # dessinerGraphe(g,True)

    Marseille = sommetNom(g,'Marseille')
    Nantes = sommetNom(g,'Nantes')
    print(shortestPath(g,Marseille,Nantes))
    dessinerGraphe(g,True)

### 3: c' est plus rapide de passer par Paris

######################
# MESURES DE DISTANCE
######################

def excentricite(g,v):
    '''
    :param g: graphe
    :param v: sommet initial
    :return: excentricite de v (distance maximale du noeud v a tous les autres sommets)
    '''
    max=0
    for el in Dijkstra(g,v)[0]:
        if Dijkstra(g,v)[0][el] > max:
            max = Dijkstra(g,v)[0][el]
    return max

def testExcentricite():
    g=tgv2005_min
    Bordeaux = sommetNom(g,'Bordeaux')
    print (excentricite(g,Bordeaux))

def rayon(g):
    '''
    :param g: graphe
    :return: plus petite distance a laquelle puisse se trouver un sommet de tous les autres
    '''
    sommets = listeSommets(g)
    res = sommets[0]
    for s in sommets:
        if excentricite(g,s) < excentricite(g,res):
            res = s
    return excentricite(g,res)

def testRayon():
    g = tgv2005_min
    print(rayon(g))

def centre(g):
    '''
    :param g: graphe
    :return: ensemble de sommets d' excentricite minimale
    '''
    sommets=listeSommets(g)
    res = [sommets[0]]
    for s in sommets:
        if excentricite(g,s) < excentricite(g,res[0]):
            res = [s]
        elif excentricite(g,s) == excentricite(g,res[0]):
            res.append(s)
    return res

def testCentre():
    g = tgv2005_min
    print(centre(g))


##########################################
# HEURISTIQUE DE COLORATION D'UN GRAPHE
##########################################

def coloration(g):
    sommets = listeSommets(g)
    sommetsNonMarques = []
    sommetsEcartes = []
    for s in sommets:
        if not estMarqueSommet(s):
            sommetsNonMarques.append(s)
    while sommetsNonMarques != []:
        sommetDeDegreMin = sommetsNonMarques[0]
        for s in sommetsNonMarques:
            if (degre(s) < degre(sommetDeDegreMin)) and (not estMarqueSommet(s)):
                sommetDeDegreMin = s
        marquerSommet(sommetDeDegreMin)
        sommetsEcartes.append(sommetDeDegreMin)






