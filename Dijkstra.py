import numpy as np
from heapq import heappop, heapify
from Matrice import voisins_indices_matrice

d = []
t = []
cost_value = 0
taille_mat = 0
d_copy = []

def dijkstra(matrice, point_depart, point_arrive):
	global d,t, cost_value, taille_mat, d_copy

	if point_depart  == point_arrive:
		return [point_depart]

	if point_depart[0] > point_arrive[0]:
		tmp = point_depart
		point_depart = point_arrive
		point_arrive = tmp

	taille_mat = len(matrice)
	d = [None] * (taille_mat*taille_mat)
	t = [None] * (taille_mat*taille_mat)

	for i in range(taille_mat):
		for j in range(taille_mat):
			if [i, j] == point_depart: continue
			key = j * taille_mat + i
			d[key] = [np.inf, key]

	depart_key = point_depart[1] * taille_mat + point_depart[0]
	d[depart_key] = [0, depart_key]
	d_copy = d.copy()
	heapify(d_copy)
	F = matrice.tolist()

	while len(F) > 1:
		si = heappop(d_copy)
		si_X = si[1] % taille_mat
		si_Y = (si[1] - si_X)//taille_mat

		if [si_X, si_Y] == point_arrive:
			break

		if si_Y >= len(F[si_X]):
			si_Y -= (taille_mat - len(F[si_X]))
		try:
			F[si_X].pop(si_Y)
		except IndexError:
			print("INDEX ERR:", [si_X, si_Y])

		#pour tout voisin de si, calcul distance et cout
		voisins = voisins_indices_matrice(matrice, si_X, si_Y)
		for v in voisins:
			relacher([si_X, si_Y], v)

	#traitement chemin T
	key_point_arrive = point_arrive[1] * taille_mat + point_arrive[0]
	path = []
	path.append(point_arrive)
	key = t[key_point_arrive]
	while key != point_depart:
		path.append(key)
		try:
			key_str = key[1] * taille_mat + key[0]
		except TypeError:
			print("key value : ", key)
			break #éviter d'avoir une boucle infini
		
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
