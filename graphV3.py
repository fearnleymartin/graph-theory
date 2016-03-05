import os, platform, subprocess, random, glob, sys
#from random import randrange

#EG :
#modif de mon path dot.exe pour windows
#incrémentation du nom du fichier créé pour éviter écrasement
#windows : création du graphe en png, plus de passage par un fichier .txt,
#et remplacement des '/' en '\\' pour éviter pb à l'ouverture
#linux : création au choix en dot ou png, associé aux appli dotty (fourni avec graphviz)
#ou xdot (à faire installer par les élèves) pour les dot ou eog (Visionneuse Eye of Gnome, par défaut sous Ubuntu) pour les png

# Attention, eviter que les deux noms globaux qui suivent
# aient meme prefixe que les noms "publics"
# proposes par Idle (completion de nom);
# on pourrait evidemment ajouter un _ en tete

plateforme = platform.system ()

pathGraphviz = 'C:/Program Files (x86)/Graphviz2.38/bin/dot.exe'

if plateforme == 'Windows':
    #Attention mettre le chemin sur votre ordinateur
    ########### EG ###########
    l = glob.glob('C:/Program Files (x86)/Graphviz2.38/bin/dot.exe')
    #l = glob.glob('C:/Users/Emmanuelle/Documents/graphviz-2.36/bin/dot.exe')
    ##########################
    if l == []:
        print("Graphviz non trouve, veuillez l'installer")
        sys.exit(1)
    path = l[0]
    pathGraphviz = path[0:-7]
if plateforme == 'Darwin': # pour mac
    pathGraphviz = '/usr/local/bin/'


################ PRIMITIVES GENERIQUES SUR LES LISTES   ##############

def melange (u):
    v = u[:] # v est une copie de u, Python c'est fun
    random.shuffle (v)
    return v

def elementAleatoireListe(u):
  # u est une liste
  # La fonction renvoie un element pris au hasard de la liste u si 
  # elle est non-vide. Si u est vide, la fonction renvoie une 
  # erreur (exception IndexError)
    return random.choice(u)



################ PRIMITIVES GRAPHE   #################################

def nomGraphe(G):
    verif_type_graphe(G)
    return G.label

def listeSommets(G):
    verif_type_graphe(G)
    return G.nodes

def nbSommets(G):
    return len(listeSommets(G))

def sommetNom(G, etiquette):
    for s in listeSommets(G):
        if s.label == etiquette:
            return s
    return None

def sommetNumero(G, i):
    return listeSommets(G)[i]

################# PRIMITIVES SOMMET   ###################################

def nomSommet(s):
    verif_type_sommet(s)
    return s.label

def marquerSommet(s):
    verif_type_sommet(s)
    s.mark = True

def demarquerSommet(s):
    verif_type_sommet(s)
    s.mark = False

def estMarqueSommet(s):
    verif_type_sommet(s)
    return s.mark

def colorierSommet(s, c):
    verif_type_sommet(s)
    verif_type_chaine(c)
    s.color = c

def couleurSommet(s):
    verif_type_sommet(s)
    return s.color

##Dans cette version on ne colorie pas les aretes
##colorier = colorierSommet
##couleur = couleurSommet
    
# Ici les choses serieuses
def listeAretesIncidentes(s):
    verif_type_sommet(s)
    return s.edges

def areteNumero(s, i):
    return listeAretesIncidentes(s)[i]

def degre(s) :
    return len(listeAretesIncidentes(s)) 

def listeVoisins(s):
    inc = listeAretesIncidentes(s)
    v = []
    for a in inc:
        if a.start == s:
            v.append (a.end)
        elif a.end == s:
            v.append (a.start)
    return v

def voisinNumero(s, i):
    return listeVoisins(s)[i]

def sommetVoisin(s, a):
    verif_type_sommet(s)
    verif_type_arete(a)
    if a.start == s:
        return a.end
    if a.end == s:
        return a.start
    return None

################ PRIMITIVES arete ########################

def nomArete(a):
    verif_type_arete(a)
    return a.label

def marquerArete(a):
    verif_type_arete(a)
    a.mark = True

def demarquerArete(a):
    verif_type_arete(a)
    a.mark = False

def estMarqueeArete(a):
    verif_type_arete(a)
    return a.mark

def numeroterArete(a, n):
    verif_type_arete(a)
    a.label = str(n)

################ Classes ########################

class c_graph:
    def __init__(self, label = '', drawopts = ''):
        self.nodes = []
        self.label = label
        self.drawopts = drawopts    # pour Graphviz
    def __repr__(self):
        return "<graphe: '%s'>" % self.label

class c_node:
    def __init__(self, label = '', color = 'white', mark = False, drawopts = ''):
        self.label = label
        self.color = color
        self.mark = mark
        self.edges = []
        self.drawopts = drawopts    # pour Graphviz
    def __repr__(self):
        c = "'" + self.color + "'"
        return "<sommet: '%s', %s, %s>" % (self.label, c, self.mark)

class c_edge:
    def __init__(self, label = '', start = None, end = None, mark = False, drawopts = ''):
        self.label = label
        self.start = start
        self.end = end
        self.mark = mark
        self.drawopts = drawopts    # pour Graphviz
    def __repr__(self):
        return "<arete: '%s' %s--%s>" % (self.label, self.start.label, self.end.label)

################ Verifications de types ########################

def verif_type_graphe(G):
    if type (G) != c_graph:
        raise ErreurParametre(G, "un graphe")
    
def verif_type_sommet(s):
    if type (s) != c_node:
        raise ErreurParametre(s, "un sommet")

def verif_type_arete(a):
    if type (a) != c_edge:
        raise ErreurParametre(a, "une arete")

def verif_type_chaine(s):
    if type(s) != str:
        raise ErreurParametre(s, "une chaine de caracteres")

class ErreurParametre (Exception):
    def __init__(self, arg, param):
        self.arg = arg
        self.param = param
    def __str__(self):
        # affichage discutable
        if type (self.arg) == str:
            strArg = "'" + self.arg + "'"
        else:
            strArg = str (self.arg)
        return strArg + " n'est pas " + self.param

############### Construction de graphes  #####################
    
def _add_edge (G, label, i, j):
    a = c_edge(label, G.nodes[i], G.nodes[j])
    G.nodes[i].edges.append(a)
    G.nodes[j].edges.append(a)
    return a

# retourne le numero du sommet
def _find_add_node (G, nom):
    i = 0
    for s in G.nodes:
        if s.label == nom:
            return i
        i = i + 1
    G.nodes.append (c_node (nom))
    return i

# Un chemin p est une liste de noms de sommets ['A', 'B', 'C', ...]
# Le parametre booleen 'chemins' indique si les aretes sont:
#   A-B, B-C, etc. (chemin classique)
#   A-B, A-C, etc. (etoile: le sommet initial est suivi de ses voisins)
# B, C, etc. peuvent aussi etre des couples [nom de sommet, nom d'arete]
# lorsqu'on veut etiqueter explicitement les aretes
# (etiquetees par defaut 'e0', 'e1', etc. dans l'ordre de leur creation)

# Attention: l'etiquette d'un graphe (label) sert aussi de nom de fichier
# pour les dessins, eviter les blancs, etc

def construireGraphe (paths, label, chemins = True):
    G = c_graph(label)
    
    # Numeroter les aretes a partir de 0 ou 1 en l'absence
    # d'etiquette explicite?
    # On choisit 1 car les dessins d 'exemples adoptent cette convention
    # mais ce choix est incoherent avec celui pour les sommets:
    # la fonction sommetNumero impose que les sommets des graphes
    # generiques (grilles, etc) soient etiquetes 's0', 's1', etc.
    # Voir bibV3
    
    nba = 1
    for p in paths:
        labelsource = p[0]
        i = _find_add_node (G, labelsource);
        
        # ne pas utiliser 'for a in p' car il faut maintenant ignorer p[0]  
        for k in range (1, len(p)):
            a = p[k]
            edge_with_label = type(a) == type([])
            if edge_with_label:
                labeldestination = a[0]
                labeledge = a[1]
            else:
                labeldestination = a
                labeledge = 'e' + str(nba)
                nba = nba + 1
            j = _find_add_node(G, labeldestination)
            _add_edge(G, labeledge, i, j)
            if chemins:
                i = j
    return G

############### Dessin du graphe  #####################

# fonction necessaire a cause par exemple des 'Pays Bas' (blanc dans label)
def _proteger (label):
    return '"' + label + '"'

# La fonction 'dotify' transforme le graphe en un fichier texte
# qui servira de source (suffixe .dot) pour les programmes de Graphviz.
# Cette fonction ne depend pas du systeme d'exploitation.

def dotify (G, etiquettesAretes = True, colormark = 'Black', suffixe = 'dot'):

    # graphe non oriente, il faut eviter de traiter chaque arete deux fois
    for s in G.nodes:
        for a in s.edges:
            a.ecrite = False
            
    if G.label == '':
        nom_graphe = 'G'
    else:
        nom_graphe = G.label

    graph_dot = 'tmp/' + nom_graphe + '.' + suffixe
    ########### EG ###########
    i = 1
    while os.path.isfile(graph_dot):
        #le fichier existe déjà, incrémentation :
        graph_dot = 'tmp/' + nom_graphe + "_" + str(i) + '.' + suffixe
        i = i + 1
    ##########################
        
    try:
        f = open (graph_dot, 'w')
    except IOError:
        os.mkdir ('tmp')
        f = open (graph_dot, 'w')
        
    f.write ('graph ' + nom_graphe + '{\n' + G.drawopts + '\n')

    for s in G.nodes:
        d = len (s.edges)
        snom = _proteger (s.label)
        for a in s.edges:
            if not a.ecrite:
                a.ecrite = True
                if a.start == s:
                    t = a.end
                else:
                    t = a.start
                f.write ('  ' + snom + ' -- ' + _proteger (t.label))
                if etiquettesAretes:
                    f.write (' [label = ' + _proteger (a.label) + ']')
                if a.mark:
                    f.write (' [style = bold, color = orange]')
                # Semicolons aid readability but are not required (dotguide.pdf)
                f.write (a.drawopts + ';\n')
        bord = 'black'
        if s.mark:
            entoure = 2
            bord = colormark
        else:
            entoure = 1
        if s.color:
            f.write ('  %s [style = filled, peripheries = %s, fillcolor = %s, color = %s] %s;\n' %
                     (snom, entoure, s.color, bord, s.drawopts))
        elif s.mark:
##            f.write ('  ' + snom + ' [peripheries = 2, color = ' + bord + ']' +
##                     s.drawopts + ';\n');
            f.write ('  %s [peripheries = 2, color = %s] %s;\n' %
                     (snom, bord, s.drawopts))
        elif d == 0 or s.drawopts:
            f.write ('  ' + snom + s.drawopts + ';\n')
            
    f.write ('}\n')
    f.close ()
    return graph_dot

# La fonction 'Graphviz' lance l'execution d'un programme
# de la distribution Graphviz (dot, neato, twopi, circo, fdp)
# pour transformer un fichier texte source de nom 'racine.suffixe'
# en une image de nom 'racine.format' (peut-etre un fichier PostScript)

def Graphviz (source, algo = 'dot', format = 'dot', suffixe = 'dot'):
    image = source.replace ('.' + suffixe, '.' + format)
    algo = pathGraphviz + algo
    if plateforme == 'Windows':
        algo = algo + '.exe'
    subprocess.call ([algo, '-T' + format, source, '-o', image])
    return image

# Enchaine dotify et Graphviz avec des arguments standard adaptes au systeme
# et lance le programme ad hoc pour afficher l'image

def dessinerGraphe (G, etiquettesAretes = False, algo = 'dot', colormark = 'Black'):
    verif_type_graphe (G)
    sys = platform.system ()

    if plateforme == 'Windows':
        graph_dot = dotify (G, etiquettesAretes, colormark)
        image = Graphviz (graph_dot, algo,'png')
        image = image.replace ('/', '\\')
        os.startfile(image)
        return
    
    if plateforme == 'Windows':
        # eviter toute embrouille avec les modeles de document de MS Word
        ########### EG ###########
        #graph_dot = dotify (G, etiquettesAretes, colormark, 'txt')
        #image = Graphviz (graph_dot, algo, suffixe = 'txt')
        graph_dot = dotify (G, etiquettesAretes, colormark)
        image = Graphviz (graph_dot, algo,'png')
        image = image.replace ('/', '\\')
        ##########################
        os.startfile (image)
        return

    #graph_dot = dotify (G, etiquettesAretes, colormark)
    #image = Graphviz (graph_dot, algo)
    if plateforme == 'Linux':
        graph_dot = dotify (G, etiquettesAretes, colormark)
        ########### EG ###########
        outFormat = 'png'
        if outFormat == 'png':
            image = Graphviz (graph_dot, algo, outFormat)
            subprocess.Popen (['eog ' + image + ' &'], shell=True)
        elif outFormat == 'dot':
            #subprocess.Popen (['dotty ' + graph_dot + ' &'], shell=True)
            subprocess.Popen (['xdot ' + graph_dot + ' &'], shell=True)
        else:
            print('Spécifier application pour ouvrir ce format :', format)
        #subprocess.call (['firefox', image])
        ##########################
    elif plateforme == 'Darwin':
        graph_dot = dotify (G, etiquettesAretes, colormark)
        image = Graphviz (graph_dot, algo)
        subprocess.call (['open', image])
        #os.system('open' + image)
    else:
        print("Systeme " + plateforme + " imprevu, abandon du dessin")
##        
dessiner = dessinerGraphe

#print("graphV3.py")
