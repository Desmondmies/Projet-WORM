import numpy as np
from heapq import heappop, heapify
from Matrice.Matrice import num_cases_voisines
from Utilitaires.Utils import coord_numCase, numCase_coord

d = []
t = []
dim_mat = 0
F = []
matrice = None

def dijkstra(mat, point_depart, point_arrive):
	global d, t, dim_mat, F, matrice

	#Initialisation des variables
	matrice = mat
	dim_mat = len(matrice)
	dim_terrain = dim_mat - 2

	#Numéros des cases dans la MATRICE (en tenant compte des bordures)
	numCase_depart = coord_numCase(point_depart[0], point_depart[1], dim_mat)
	numCase_arrive = coord_numCase(point_arrive[0], point_arrive[1], dim_mat)

	t = [None] * (dim_mat * dim_mat)

	d = [None] * (dim_mat * dim_mat)
	for y in range(dim_mat):
		for x in range(dim_mat):
			numCase = coord_numCase(x, y, dim_mat)
			d[numCase] = [np.inf, numCase] #Lorsque d sera converti en tas, on perdra le numéro de la case associée à ce coût
	d[numCase_depart][0] = 0

	#On a d sous forme de liste pour récupérer le cout d'une case (d[numCase] = [coutCumulé, numCase]).
	#On a F sous la forme d'un tas pour récupérer la case du chemin avec un cout minimale plus efficacement.
	F = d.copy()
	#F ne contient que les cases accessibles sur le terrain (donc la matrice sans la bordure).

		#Suppression des bordures horizontales
	del F[0:dim_mat]
	del F[len(F) - dim_mat:len(F)]

		#Suppression des colonnes de la bordure
	for i in range(0, dim_terrain * dim_terrain, dim_terrain):
		del F[i]
		del F[i + dim_terrain]

	heapify(F)

	while len(F) :
		s0 = heappop(F) #s0 = [cout cumulé, numCase dans la MATRICE]

		if s0[1] == numCase_arrive:
			return traitement_trace(numCase_depart, numCase_arrive)

		#pour tout voisin de s0, calcul distance et cout
		liste_numVoisins = num_cases_voisines(s0[1], dim_mat)

		for numVoisin in liste_numVoisins:
			s1 = d[numVoisin] #s1 = [cout cumulé, numCase dans la MATRICE]
			relacher(s0, s1)

	return None

def relacher(s0, s1):
	global d, t

	coord_s1 = numCase_coord(s1[1], dim_mat)
	#matrice [ coord_s1[1], coord_s1[0] ] => matrice [ ligne, colonne ]
	#cout_deplacement = s0[0] + matrice[coord_s1[1], coord_s1[0]] + cout(s0, s1)
	cout_deplacement = cout(s0, s1)

	if s1[0] > cout_deplacement:
		d[s1[1]][0] = cout_deplacement
		t[s1[1]] = s0[1]

		#Mise à jour des distances dans F
		for case in F:
			if case[1] == s1[1]:
				case[0] = cout_deplacement
				break

		heapify(F)

def cout(s0, s1):
	coord_s0 = numCase_coord(s0[1], dim_mat)
	coord_s1 = numCase_coord(s1[1], dim_mat)

	distX = abs(coord_s1[0] - coord_s0[0])
	distY = abs(coord_s1[1] - coord_s0[1])

	if(distX == distY):
		return s0[0] + matrice[coord_s1[1], coord_s1[0]] * 14
	return s0[0] + matrice[coord_s1[1], coord_s1[0]] * 10


def traitement_trace(numCase_depart, numCase_arrive):
	path = []
	numCase_prec = numCase_arrive
	while numCase_prec != numCase_depart:
		path.append(numCase_coord(numCase_prec, dim_mat))
		numCase_prec = t[numCase_prec]

	path.append(numCase_coord(numCase_depart, dim_mat))

	return path[::-1]
