from math import sqrt
from heapq import heappop, heapify
from numpy import Inf
from Matrice import num_cases_voisines

dim_mat = 0
G_cost = []
H_cost = []
F_cost = []
F_copy = []
matrice = None

trace_chemin = []

pt_depart = []
pt_arrivee = []

open_set = []

def coord_numCase(x, y):
	return y * dim_mat + x

def numCase_coord(numCase):
	coord = []
	coord.append(numCase % dim_mat)
	coord.append(int((numCase - coord[0]) / dim_mat))
	return coord

def a_star(mat, point_depart, point_arrivee):
    global dim_mat, G_cost, H_cost, F_cost, matrice, pt_depart, pt_arrivee, F_copy, trace_chemin, open_set
    open_set = []
    closed_set = []

    pt_depart = point_depart
    pt_arrivee = point_arrivee

    dim_mat = len(mat)
    dim_terrain = dim_mat - 2
    matrice = mat

    G_cost = [Inf] * (dim_mat * dim_mat) #distance / cout vers le point de départ
    H_cost = [Inf] * (dim_mat * dim_mat) #distance / cout vers le point d'arrivée
    F_cost = [Inf] * (dim_mat * dim_mat) #somme de H + G
    for j in range(dim_mat):
        for i in range(dim_mat):
            numCase = coord_numCase(i, j)
            F_cost[numCase] = [Inf, numCase]
    trace_chemin = [None] * (dim_mat * dim_mat) #t de dijkstra

    numCase_pt_depart = coord_numCase(point_depart[0], point_depart[1])
    numCase_pt_arrivee = coord_numCase(point_arrivee[0], point_arrivee[1])
    open_set.append(numCase_pt_depart)
    calc_cost(point_depart)
    #heapify(open_set)

    F_copy = F_cost.copy()

    del F_copy[0:dim_mat]
    del F_copy[len(F_copy) - dim_mat:len(F_copy)]

    #Suppression des colonnes de la bordure
    for i in range(0, dim_terrain * dim_terrain, dim_terrain):
        del F_copy[i]
        del F_copy[i + dim_terrain]

    heapify(F_copy)

    while len(open_set) > 0:
        si = heappop(F_copy) #si => [somme G_cost + H_cost, numCase]
        si_numCase = si[1]

        if si_numCase in open_set:
            open_set.remove(si_numCase)
        closed_set.append(si_numCase)

        if si_numCase == numCase_pt_arrivee:
            return traitement_trace(numCase_pt_depart, numCase_pt_arrivee)

        voisins = num_cases_voisines( si_numCase, dim_mat)
        for v in voisins:
            if v in closed_set: continue
            relacher(si_numCase, v)

    return None

def distance(p1, p2):
    if p1 == p2: return 0
    dX = abs(p1[0] - p2[0])
    dY = abs(p1[1] - p2[1])
    d = sqrt( dX*dX + dY*dY )
    return int( d )

def calc_cost(point):
    global G_cost, H_cost, F_cost, F_copy
    numCase = coord_numCase(point[0], point[1])
    G_cost[numCase] = distance(point, pt_depart)
    H_cost[numCase] = distance(point, pt_arrivee)
    sum_cost = G_cost[numCase] + H_cost[numCase]
    F_cost[numCase][0] = sum_cost

    for case in F_copy:
        if case[1] == F_cost[numCase][1]:
            case[0] = sum_cost
            break

    heapify(F_copy)

def relacher(si_numCase, v):
    global open_set

    si_coord = numCase_coord(si_numCase)
    v_coord = numCase_coord(v)
    move_cost = G_cost[si_numCase] + distance(si_coord, v_coord)
    if move_cost < G_cost[v] or v not in open_set:
        calc_cost(v_coord)
        trace_chemin[v] = si_numCase

        if v not in open_set:
            open_set.append(v)


def traitement_trace(numCase_depart, numCase_arrive):
	path = []
	numCase_prec = numCase_arrive
	while numCase_prec != numCase_depart:
		path.append(numCase_coord(numCase_prec))
		numCase_prec = trace_chemin[numCase_prec]

	path.append(numCase_coord(numCase_depart))

	return path[::-1]
