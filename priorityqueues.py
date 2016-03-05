#Implementation of a priority queue
#with a heap
#we use python's list to implement the heap

#the solution is not the best but one of the most understandable

# author: J-P Poli

#mod EG 03/2014 :
#suppressions des solutions alternatives pour TP Graphes

class EmptyQueue(Exception): pass

def emptyPriorityQueue():
    """Creates a new priority queue."""
    return []

def size(q):
    """Gets the size of the queue"""
    return len(q)

def isEmpty(q):
    """Indicates if the priority queue q is empty"""
    return size(q)==0

#iterative solution
def enqueue(q, e, p):
    """Adds an element e to the priority queue q, regarding the priority p. Returns the new queue."""
    #Adding the tuple (p, e) at the end of the list
    #i.e. at the last leaf of the heap
    queue = q + [(p,e)]

    #Now, we have to move upward if necessary
    current = len(queue) - 1 #current position of the new leaf
    while current > 0:
        parent = (current-1)//2 #parent
        if queue[parent][0] <= queue[current][0]: #if parent is lower than new leaf, we stop
            break
        queue[parent], queue[current] = queue[current], queue[parent] #else swap parent and new leaf
        current = parent
    return queue
        

def first(q):
    """Returns the next element in q."""
    if q==[]:
        raise EmptyQueue
    else:
        return q[0][1]

#iterative solution
def dequeue(q):
    """Returns a queue without the maximum priority element of q."""
    if len(q)<=1:
        return []
    else:
        #first step we replace the root by the last leaf
        queue = q[:-1]
        queue[0] = q[-1]
        
        #next step we move down the new root
        current = 0
        while current<len(queue):
            leftpos  = 2*current+1 #this is the position of left child
            rightpos = 2*current+2 #this is the position of right child
            if rightpos<len(queue) and leftpos<len(queue):
                #we have at least the root and 2 children
                if queue[current][0]<=queue[rightpos][0] and queue[current][0]<=queue[leftpos][0]:
                    #job's done, the node at pos is correctly placed
                    break
                elif queue[rightpos][0]<queue[leftpos][0]:
                    #swap the node at pos and at rightpos
                    queue[current], queue[rightpos] = queue[rightpos], queue[current]
                    current = rightpos
                else:
                    #swap the node at pos and at rightpos
                    queue[current], queue[leftpos] = queue[leftpos], queue[current]
                    current = leftpos
            else:
                #we have either only a right child or a left child
                if rightpos<len(queue) and queue[rightpos][0]<queue[current][0]:
                    queue[rightpos],queue[current] = queue[current], queue[rightpos]
                    current = rightpos
                elif leftpos<len(queue) and queue[leftpos][0]<queue[current][0]:
                    queue[leftpos],queue[current] = queue[current], queue[leftpos]
                    current = leftpos
                else:
                    #this is a leaf
                    break
        return queue
