import numpy as np
from math import sqrt
from heapq import heappop, heapify
from Matrice import num_cases_voisines

d = []
t = []
dim_mat = 0
F = []
matrice = None

pt_arrivee = []

def coord_numCase(x, y):
	return y * dim_mat + x

def numCase_coord(numCase):
	coord = []
	coord.append(numCase % dim_mat)
	coord.append(int((numCase - coord[0]) / dim_mat))
	return coord

def a_star(mat, point_depart, point_arrive):
    global d, t, dim_mat, F, matrice, pt_arrivee

    #Initialisation des variables
    matrice = mat
    dim_mat = len(matrice)
    dim_terrain = dim_mat - 2

    pt_arrivee = point_arrive

    #Numéros des cases dans la MATRICE (en tenant compte des bordures)
    numCase_depart = coord_numCase(point_depart[0], point_depart[1])
    numCase_arrive = coord_numCase(point_arrive[0], point_arrive[1])

    #print("depart : ", numCase_depart)
    #print("arrive : ", numCase_arrive)

    t = [None] * (dim_mat * dim_mat)

    d = [None] * (dim_mat * dim_mat)
    for y in range(dim_mat):
        for x in range(dim_mat):
            numCase = coord_numCase(x, y)
            d[numCase] = [np.inf, numCase] #Lorsque d sera converti en tas, on perdra le numéro de la case associée à ce coût	
    d[numCase_depart][0] = 0

    #print("d :\n", d)
    #print("-" * 100)

    #On a d sous forme de liste pour récupérer le cout d'une case (d[numCase] = [coutCumulé, numCase]).
    #On a F sous la forme d'un tas pour récupérer la case du chemin avec un cout minimale plus efficacement.
    F = d.copy()
    #F ne contient que les cases accessibles sur le terrain (donc la matrice sans la bordure).
		
    #Suppression des bordures horizontales
    del F[0:dim_mat]
    del F[len(F) - dim_mat:len(F)]

    #print(" F supp lignes :\n", F)
    #print("-" * 100)

    #Suppression des colonnes de la bordure
    for i in range(0, dim_terrain * dim_terrain, dim_terrain):
        del F[i]
        del F[i + dim_terrain]

    #print(" F final :\n", F)
    #print("-" * 100)

    heapify(F)
	
    while len(F) :
        s0 = heappop(F) #s0 = [cout cumulé, numCase dans la MATRICE]

        if s0[1] == numCase_arrive:
            return traitement_trace(numCase_depart, numCase_arrive)

        #print("s0[1] :", s0[1])

        #pour tout voisin de s0, calcul distance et cout
        liste_numVoisins = num_cases_voisines(s0[1], dim_mat)

        #print("voisins de", s0[1], ":", liste_numVoisins)
        #print("-" * 100)

        for numVoisin in liste_numVoisins:
            s1 = d[numVoisin] #s1 = [cout cumulé, numCase dans la MATRICE]
            relacher(s0, s1)

    return None

def distance(p1, p2):
    if p1 == p2: return 0
    dX = p2[0] - p1[0]
    dY = p2[1] - p1[1]
    d = sqrt( dX*dX + dY*dY )
    #print(p1, p2, "dist : ", d)
    return int( d )

def relacher(s0, s1):
    global d, t

    coord_s1 = numCase_coord(s1[1])
    cout_deplacement = matrice[coord_s1[1], coord_s1[0]] + distance(coord_s1, pt_arrivee)

    #print("cout :", cout_deplacement)

    if s1[0] > cout_deplacement:
        d[s1[1]][0] = cout_deplacement
        t[s1[1]] = s0[1]

        #Mise à jour des distances dans F
        for case in F:
            if case[1] == s1[1]:
                case[0] = cout_deplacement
                break

        heapify(F)

def traitement_trace(numCase_depart, numCase_arrive):
	path = []
	numCase_prec = numCase_arrive
	while numCase_prec != numCase_depart:
		path.append(numCase_coord(numCase_prec))
		numCase_prec = t[numCase_prec]

	path.append(numCase_coord(numCase_depart))

	return path[::-1]