class EmptyQueue(Exception): pass

def emptyQueue():
    """ Cree une file vide """
    return []

def isEmpty(F):
    """ Teste si une file est vide """
    return F==[]

def enqueue(e, F):
    """ Met un element à la fin de la file F """
    return F + [e]

def dequeue(F):
    """Supprimer le premier element de la file F """
    if isEmpty(F):
        raise EmptyQueue
    else:
        return F[1:]

def first(F):
    """ Retourne le premier element de la file F """
    if isEmpty(F):
        raise EmptyQueue
    else:
        return F[0]

