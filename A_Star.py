from cmath import sqrt
from heapq import heappush, heappop, heapify
from Matrice import voisins_matrice

def distance(p1, p2):
    dX = abs(p1[0] - p2[0])
    dY = abs(p1[1] - p2[1])
    return int( sqrt( dX*dX + dY*dY ) )

def a_star(matrice, point_depart, point_arrivee):
    open_set = []
    closed_set = []
    open_set.append(point_depart)
    heapify(open_set)

    while len(open_set) > 0:
        si = heappop(open_set)

        closed_set.append(si)

        if si == point_arrivee:
            break

        voisins = voisins_matrice(matrice, si[0], si[1])
        for v in voisins:
            if v in closed_set: continue
            pass
            #move_cost = si.gCost + distance(si, v)

        pass

