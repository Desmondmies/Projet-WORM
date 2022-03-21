import numpy as np
from heapq import heappush, heappop, heapify
from Matrice import voisins_matrice, remove_elmt

d = []
t = {}

def dijkstra(matrice, point_depart):
    global d,t

    for i in range(len(matrice)):
        for j in range(len(matrice)):
            #d[liste[i]] = np.inf
            if matrice[i, j] == point_depart: continue
            #d[matrice[i, j]] = np.inf
            d.append( [np.inf, matrice[i, j]] )
            t[matrice[i, j]] = None
    
    #d[point_depart] = 0
    d.append( [0, point_depart] )
    #reverse_d = {v: k for k, v in d.items()}
    #reverse_d = list(reverse_d.items())
    #d = reverse_d
    d_local = d.copy()
    heapify(d_local)
    E = []
    #heapify(liste)
    F = matrice
    while len(F) > 1:
        si = heappop(d_local)
        #F.remove(si[1])
        F = remove_elmt(F, si[1])
        E.append(si)

        #pour tout voisin de si, calcul distance et cout
        voisins = voisins_matrice(matrice, si[1].X, si[1].Y)
        for v in voisins:
            relacher(si[1], v)
    return t

def indexOf(l, elmt):
    for i in range(len(l)):
        if l[i][1] == elmt:
            return i
    return -1
 
def relacher(si, sj):
    global d, t
    #si_index = d.index(si)
    #sj_index = d.index(sj)
    si_index = indexOf(d, si)
    sj_index = indexOf(d, sj)
    move_cost = d[si_index][0] + cout(si, sj)
    if d[sj_index][0] > move_cost:
        d[sj_index][0] = move_cost
        t[sj] = si

def cout(si, sj):
    dist_X = abs(si.X - sj.X)
    dist_Y = abs(si.Y - sj.Y)

    if dist_X > dist_Y:
        return 14 * dist_Y + 10 * (dist_X - dist_Y)
    return 14 * dist_X + 10 * (dist_Y - dist_X)