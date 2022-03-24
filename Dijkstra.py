import numpy as np
from heapq import heappop, heapify
from Matrice import voisins_indices_matrice

d = []
t = {}
cost_value = 0
taille_mat = 0
d_copy = []

def swap(p1, p2):
	return p2, p1

def dijkstra(matrice, point_depart, point_arrive):
	global d,t, cost_value, taille_mat, d_copy

	#si le point de départ est le même que l'arrivé, le chemin est tout trouvé
	if point_depart  == point_arrive:
		return [point_depart]

	taille_mat = len(matrice)
	taille_dim = taille_mat * taille_mat
	d = [None] * (taille_mat*taille_mat)
	t = {}

	#initialisation d à np.inf
	for i in range(taille_mat):
		for j in range(taille_mat):
			if [i, j] == point_depart: continue
			key = j * taille_mat + i
			d[key] = [np.inf, key]

	depart_key = point_depart[1] * taille_mat + point_depart[0]
	d[depart_key] = [0, depart_key]
	
	#copie obligatoire, car heappop, modifie le heap, donc les indices calculés y*n+x ne sont pas conservés
	#donc solution, une copie de d, d est modifie mais reste inchangé pour obtenir les valeurs de distances grâce aux indices calculés
	#et la copie se voit modifier le bon indice à chaque modification de d, pour garder les distances à jour
	#tout en enlevant les valeurs de distance minimales déjà explorés, et donc heappop les nouvelles distances minimale pour le bon fonctionnement de l'algo
	d_copy = d.copy()
	heapify(d_copy)

	E = []

	while len(E) < taille_dim:
		si = heappop(d_copy)
		si_X = si[1] % taille_mat
		si_Y = (si[1] - si_X)//taille_mat

		#si le point courant est le point d'arrivé, stop
		if [si_X, si_Y] == point_arrive:
			break

		#ajoute le point courant à la liste des "explorés"
		if si not in E:
			E.append(si)

		#pour tout voisin de si, calcul distance et cout
		voisins = voisins_indices_matrice(matrice, si_X, si_Y)
		for v in voisins:
			relacher([si_X, si_Y], v)

	if len(E) == taille_dim:
		return [] #aucun chemin

	#traitement chemin T
	key_point_arrive = point_arrive[1] * taille_mat + point_arrive[0]
	path = []
	path.append(point_arrive)

	key = t[key_point_arrive]
	while key != point_depart:
		path.append(key)
		key_str = key[1] * taille_mat + key[0]
		key = t[key_str]
	path.append(point_depart)

	return path[::-1]

def relacher(si, sj):
	global d, t
	si_index = si[1] * taille_mat + si[0]
	sj_index = sj[1][1] * taille_mat + sj[1][0]
	move_cost = d[si_index][0] + sj[0] + 1

	if d[sj_index][0] > move_cost:
		d[sj_index][0] = move_cost
		t[sj_index] = si
		#update des distances de la copy
		for i in range(len(d_copy)):
			if d_copy[i][1] == sj_index:
				d_copy[i][0] = move_cost
				break
		heapify(d_copy)
