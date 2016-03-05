import bibV3
from imp import reload
reload(bibV3)
from bibV3 import *

import itertools

g = tgv2005

def launchAllTests():
    print(testDegreMax())
    print(testDegreMin())
    print(testNbSommetsDegre())
    print(testColorierSommetsDegre())
    print(testExisteIsole())
    print(testGraphesAvecSommetsIsole())
    print(testCubique())

    print(testCompterAretesMarquees())
    print(testToutAretesMarques())
    print(testSommetEstNonMarqueavecAreteMarquee())
    print(testListeSommetsNonMarqueesavecAretesMarquees())
    print(testMemeNombreAreteSommets())
    print(testCouverture())

    print(connectionBordeauxNantes())
    print ('cense etre false')
    print(testListeVoisinsCommuns())
    print(testTrajetCorrespondance())
    print(testExisteBoucle())
    print(testNbBoucles())
    print(testSansboucles())




###################
# DEGRES DE SOMMETS
###################

def degreMax(G):
    sommets = listeSommets(G)
    degres = []
    for sommet in sommets:
        degres.append(degre(sommet))
    return max(degres)

def testDegreMax():
    g=tgv2005
    maxDegre=degreMax(g)
    if maxDegre == 7:
        return True
    else:
        return False

def degreMin(G):
    sommets = listeSommets(G)
    degres = []
    for sommet in sommets:
        degres.append(degre(sommet))
    return min(degres)

def testDegreMin():
    g=tgv2005
    minDegre=degreMin(g)
    if minDegre == 0:
        return True
    else:
        return False

def nbSommetsDegre(G,d):
    sommets = listeSommets(G)
    sommetsDeDegre_d = []
    for sommet in sommets:
        if degre(sommet)==d:
            sommetsDeDegre_d.append(sommet)
    return len(sommetsDeDegre_d)

def colorierSommetsDegre(G,d):
    sommets = listeSommets(G)
    sommetsDeDegre_d = []
    for sommet in sommets:
        if degre(sommet)==d:
            colorierSommet(sommet,'blue')

def testNbSommetsDegre():
    ## test sur sommets de tgv graph
    G=tgv2005
    return nbSommetsDegre(G,7)==2 \
    and nbSommetsDegre(G,0)== 1 \
    and nbSommetsDegre(G,1)==0\
    and nbSommetsDegre(G,2)==0\
    and nbSommetsDegre(G,3)==1\
    and nbSommetsDegre(G,4)==3\
    and nbSommetsDegre(G,5)==1\
    and nbSommetsDegre(G,6)==1\

def testColorierSommetsDegre():
    # verifie si sommets de degre 7 de tgv graph sont bien bleus
    # hypothese que la coloration est bien en bleu
    G=tgv2005
    colorierSommetsDegre(G,7)
    sommets = listeSommets(G)
    sommetsDeDegre_d = []
    test=False
    for sommet in sommets:
        if degre(sommet)==7:
            if sommet.color == 'blue':
                test=True
    return test

def existeIsole(G):
    sommets = listeSommets(G)
    if nbSommetsDegre(G,0)>0:
        return True
    else:
        return False

def testExisteIsole():
    ## verfie si tgv graph a bien un element isole
    G=tgv2005
    return existeIsole(G)==True



def testGraphesAvecSommetsIsole():
    # verfie que graphAvecSommetIsole a bien un sommet isole
    # et que graphSansSommetIsole n'a pas de sommet isole

    # definition of graphs
    graphAvecSommetIsole = construireGraphe (
        [ ['A', 'B'],['C'] ], "graphAvecSommetIsole")

    graphSansSommetIsole = construireGraphe (
        [ ['A', 'B'],
          ['B','C']
        ], "graphSansSommetIsole")

    #boolean tests
    return existeIsole(graphAvecSommetIsole)\
           and (existeIsole(graphSansSommetIsole)==False)

def cubique(G):
    sommets = listeSommets(G)
    for sommet in sommets:
        if degre(sommet)!=3:
            return False
    return True

def testCubique():
    # create cubique graph
    g=tgv2005
    cubiqueGraph = construireGraphe (
        [ ['A', 'B'],
          ['A','C'],
          ['A','D'],
          ['B','C'],
          ['B','D'],
          ['C','D'],
        ], "cubiqueGraph")
    # return boolean test: verifie si cubique est bien cubique et verfie que tgv graph ne l' est pas
    return cubique(cubiqueGraph) and (not cubique(g))


#############
#SOMMETS ET ARETES
#############

def listeAretes(G):
    '''
    Simplistic way of getting list of edges
    by getting all the nodes and then getting their incident edges
    As currently coded, will check over each edge twice, and then the set will get rid of duplicats
    :param G: graphe
    :return: liste des aretes
    '''
    sommets=listeSommets(G)
    aretes = []
    for sommet in sommets:
        aretesSommet = listeAretesIncidentes(sommet)
        for arete in aretesSommet:
            aretes.append(arete)
    return set(aretes)

def compterAreteMarquees(G):
    aretes=listeAretes(G)
    aretesMarques = []
    for arete in aretes:
        if estMarqueeArete(arete):
            aretesMarques.append(arete)
    return len(aretesMarques)

def testCompterAretesMarquees():
    g=tgv2005
    # test for graph with no marked edges
    print('g a '+ str(compterAreteMarquees(g)) + ' aretes marques')
    # mark an edge, should have 1 marked edge
    sommets=listeSommets(g)
    sommet=sommets[0]
    arete = areteNumero(sommet,0)
    marquerArete(arete)
    print('g a '+ str(compterAreteMarquees(g))+ ' aretes marques')
    # mark a different edge, should have 2 edges
    arete2 = areteNumero(sommets[1],1)
    marquerArete(arete2)
    print('g a ' + str(compterAreteMarquees(g)) + ' aretes marques')

def toutAretesMarques(G):
    return len(listeAretes(G)) == compterAreteMarquees(G)

def testToutAretesMarques():
    grapheToutAretesMarques = construireGraphe (
        [ ['A', 'B'],
          ['B','C']
        ], "graphToutAretesMarques")
    sommetB=sommetNom(grapheToutAretesMarques, 'B')
    aretes=listeAretesIncidentes(sommetB)
    for arete in aretes:
        marquerArete(arete)
    return toutAretesMarques(grapheToutAretesMarques)

def sommetEstNonMarqueavecAreteMarquee(s):
    if estMarqueSommet(s):
        return False
    aretesIncidents = listeAretesIncidentes(s)
    IncidentArretMarque = False
    for arete in aretesIncidents:
        if estMarqueeArete(arete):
            IncidentArretMarque = True
    return IncidentArretMarque

def testSommetEstNonMarqueavecAreteMarquee():
    # create such a graph
    grapheAvecSommetNonMarqueEtAvecArretMarque = construireGraphe (
            [ ['A', 'B'],
              ['B','C']
            ], "grapheAvecSommetNonMarqueEtAvecArretMarque")
    sommetB=sommetNom(grapheAvecSommetNonMarqueEtAvecArretMarque,'B')
    sommetC=sommetNom(grapheAvecSommetNonMarqueEtAvecArretMarque,'C')
    arete=areteNumero(sommetB,0)
    marquerArete(arete)
    # verify function: check is the case for sommet B but not for C
    return sommetEstNonMarqueavecAreteMarquee(sommetB)\
    and not sommetEstNonMarqueavecAreteMarquee(sommetC)

def listeSommetsNonMarqueesavecAretesMarquees(G):
    sommets = listeSommets(G)
    # list of Sommets Non Marquees avec Aretes Marquees
    list = []
    for sommet in sommets:
        if sommetEstNonMarqueavecAreteMarquee(sommet):
            list.append(sommet)
    return list

def testListeSommetsNonMarqueesavecAretesMarquees():
    # create a test graph with marked sommets
    grapheAvecSommetNonMarqueEtAvecArretMarque = construireGraphe (
            [ ['A', 'B'],
              ['B', 'C']
            ], "grapheAvecSommetNonMarqueEtAvecArretMarque")
    sommetB=sommetNom(grapheAvecSommetNonMarqueEtAvecArretMarque, 'B')
    arete=areteNumero(sommetB,0)
    marquerArete(arete)
    return listeSommetsNonMarqueesavecAretesMarquees(grapheAvecSommetNonMarqueEtAvecArretMarque)

def memeNomreAreteSommets(G):
    sommets = listeSommets(G)
    aretes = listeAretes(G)
    return len(sommets) == len(aretes)

def testMemeNombreAreteSommets():
    # create a graph with same number of nodes and edges
    grapheAvecMemeNombreSommetEtArrets = construireGraphe (
            [ ['A', 'B'],
              ['B','C'],
              ['A','C']
            ], "grapheAvecMemeNombreSommetEtArrets")
    return memeNomreAreteSommets(grapheAvecMemeNombreSommetEtArrets)


def couverture(G, E):
    '''
    parcourt tous les aretes
    si au moins un des extremites d' un arret n' est pas dans E, res est mis a False
    :param G: graph
    :param E: liste de sommets
    :return:
    '''
    aretes=listeAretes(G)
    res = True
    for arete in aretes:
        start_edge = arete.start
        end_edge = arete.end
        if (start_edge not in E) and (end_edge not in E):
            res = False
    return res

def testCouverture():
    # create some graphes where E is a couverture
    # test 1
    graph1 = construireGraphe (
            [ ['A', 'B'],
              ['B','C'],
              ['A','C']
            ], "graph1")
    E1 = listeSommets(graph1)

    # test 2
    graph2 = construireGraphe (
            [ ['A', 'B'],
              ['C','D'],
              ['E']
            ], "graph2")
    E2 = listeSommets(graph2)

    # test 3
    graph3 = construireGraphe (
            [ ['A', 'B'],
              ['C','D'],
            ], "graph2")
    E3 = listeSommets(graph3)

    return couverture(graph1,E1) \
           and couverture(graph2,E2)\
           and couverture(graph3,E3)


##############
#VOISINS
##############

def printDegreEtVoisins(G):
    sommets = listeSommets(G)
    for sommet in sommets:
        print('Sommet: ' + nomSommet(sommet) + ', degre: '+str(degre(sommet)) + ', voisins: ')
        print(listeVoisins(sommet))

def voisinsDeNantes():
    g = tgv2005
    sommet = sommetNom(g,'Nantes')
    return listeVoisins(sommet)

def sontVoisins(s1,s2):
    voisinsDes1 = listeVoisins(s1)
    return (s2 in voisinsDes1)

def voisinsFig1():
    '''
    test de sontVoisin sur tous les couples de sommets du graphe de figure 1
    :return:
    '''
    g = tgv2005
    sommets = listeSommets(g)
    couples = itertools.combinations(sommets,2)
    for couple in couples:
        print(sontVoisins(couple[0],couple[1]))

def connectionBordeauxNantes():
    '''
    test pour voir s' il y a une connection entre Bordeaux et Nantes
    :return:
    '''
    g=tgv2005
    Bordeaux = sommetNom(g,'Bordeaux')
    Nantes = sommetNom(g,'Nantes')
    return sontVoisins(Bordeaux, Nantes)

def listeVoisinsCommuns(s1,s2):
    voisins_s1 = listeVoisins(s1)
    voisins_s2 = listeVoisins(s2)
    voisinsCommuns = []
    for voisin_s1 in voisins_s1:
        if voisin_s1 in voisins_s2:
            voisinsCommuns.append(voisin_s1)
    return voisinsCommuns

def testListeVoisinsCommuns():
    '''
    verfie que les voisins communs de Lyon et Nantes sont bien Marseille, Paris et Lille
    :return:
    '''
    g = tgv2005
    Lyon = sommetNom(g, 'Lyon')
    Nantes =sommetNom(g, 'Nantes')
    Paris = sommetNom(g,'Paris')
    Marseille = sommetNom(g,'Marseille')
    Lille = sommetNom(g,'Lille')

    resultatAttendu = [Paris,Marseille,Lille]
    # set est utilise pour que l' ordre n' ait pas d' importance
    return set(listeVoisinsCommuns(Lyon, Nantes)) == set(resultatAttendu)

def trajetCorrespondance(s1,s2):
    if len(listeVoisinsCommuns(s1, s2)) > 0:
        return True
    else:
        return False

def testTrajetCorrespondance():
    '''
    Il doit etre possible d' aller de Bordeaux a Nantes avec au plus une correspondance,
    mais pas de Strasbourg a Marseille, par exemple
    :return:
    '''
    g = tgv2005
    Lyon = sommetNom(g, 'Lyon')
    Bordeaux = sommetNom(g,'Bordeaux')
    Nantes =sommetNom(g, 'Nantes')
    Paris = sommetNom(g,'Paris')
    Marseille = sommetNom(g,'Marseille')
    Lille = sommetNom(g,'Lille')
    Strasbourg = sommetNom(g,'Strasbourg')
    return trajetCorrespondance(Bordeaux, Nantes)\
        and not trajetCorrespondance(Strasbourg, Marseille)

def function(sommet):

    '''
    :param G: graph
    :return: function(G)
    '''
    return sommet

def automorphisme(G):
    sommets = listeSommets(G)
    pairs = itertools.combinations(sommets,2)
    for pair in pairs:
        if sontVoisins(pair[0],pair[1]) and (not sontVoisins(function(pair[0]), function(pair[1]))):
            return False
    else:
        return True
    # teste avec la function identite seulement


###########
#BOUCLES
###########

def existeBoucle(s):
    voisins=listeVoisins(s)
    if s in voisins:
        return True
    else:
        return False

def testExisteBoucle():
    '''

    :return: true si B a une boucle et pas A, et false sinon
    '''
    g = fig22
    sommetA = sommetNom(g, 'A')
    sommetB = sommetNom(g, 'B')
    return existeBoucle(sommetB)\
        and not existeBoucle(sommetA)


def nbBoucles(s):
    voisins = listeVoisins(s)
    return voisins.count(s)/2 # division par deux car les boucles sont comptes deux fois ici


def testNbBoucles():
    g = fig22
    sommetB = sommetNom(g, 'B')
    sommetD = sommetNom(g, 'D')
    return nbBoucles(sommetB) == 1 and nbBoucles(sommetD) == 2

def sansboucles(G):
    sommets = listeSommets(G)
    for sommet in sommets:
        if nbBoucles(sommet) > 0:
            return False
    return True

def testSansboucles():
    '''

    :return: true si tgv2005 n' a pas de boucles et fig 22 en a
    '''
    return sansboucles(tgv2005) and not sansboucles(fig22)






