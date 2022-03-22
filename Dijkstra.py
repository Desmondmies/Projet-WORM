import numpy as np
from heapq import heappop, heapify
from Matrice import voisins_indices_matrice

d = []
t = {}
cost_value = 0

def dijkstra(matrice, point_depart, point_arrive):
	global d,t, cost_value

	for i in range(len(matrice)):
		for j in range(len(matrice)):
			if [i, j] == point_depart: continue
			d.append( [np.inf, [i, j]] )
			key = str(i) + "," + str(j)
			t[key] = None

	d.append( [0, point_depart] )
	d_local = d.copy()
	heapify(d_local)
	E = []
	F = matrice.tolist()

	while len(F) > 1:
		si = heappop(d_local)
		if si in F:
			F[si[1][0]].pop(si[1][1])
		E.append(si)
		cost_value = matrice[si[1][0], si[1][1]]

		if si[1] == point_arrive:
			break

		#pour tout voisin de si, calcul distance et cout
		voisins = voisins_indices_matrice(matrice, si[1][0], si[1][1])
		for v in voisins:
			relacher(si, v)

	#traitement chemin T
	key_point_arrive = str(point_arrive[0]) + "," + str(point_arrive[1])
	path = []
	key = t[key_point_arrive]
	while key != point_depart:
		path.append(key)
		key_str = str(key[0]) + "," + str(key[1])
		key = t[key_str]
	path.append(point_depart)

	return path[::-1]

def indexOf(l, elmt):
	for i in range(len(l)):
		if l[i][1] == elmt[1]:
			return i
	return -1

def relacher(si, sj):
	global d, t
	si_index = indexOf(d, si)
	sj_index = indexOf(d, sj)
	#retrouver dans d la valeur de distance, à partir de coordonnées si
	move_cost = d[si_index][0] + cout(si, sj)
	if d[sj_index][0] > move_cost:
		d[sj_index][0] = move_cost
		key = str(sj[1][0]) + "," + str(sj[1][1])
		t[key] = si[1]

def cout(si, sj):
    dist_X = abs(si[1][0] - sj[1][0])
    dist_Y = abs(si[1][1] - sj[1][1])

    if dist_X > dist_Y:
        return 14 * dist_Y + 10 * (dist_X - dist_Y) + cost_value
    return 14 * dist_X + 10 * (dist_Y - dist_X) + cost_value
