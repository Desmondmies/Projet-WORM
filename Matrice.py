import numpy as np

grid_size = 15
grid_minValue = 0
grid_maxValue = 7
inf_value = 1000

"""
Renvoi la taille n de la matrice carré
"""
def get_taille_matrice(m):
	return len(m) #m.shape[0]

"""
Supprime un élément dans la matrice
Numpy pourri pour ça, obligé de faire la conversion etc

def remove_elmt(m, elmt):
    tmp = m.tolist()
    n = len(tmp)
    #tmp[elmt.X].pop(elmt.Y)
    #tmp.remove(elmt)

    try:
        for i in range(1, n-1):
            for j in range(1, n-1):
                if tmp[i][j] == elmt:
                    tmp[i].pop(j)
                    mat = np.asarray(tmp, dtype=object)
                    return mat
    except IndexError:
        print("index error", elmt)
    #mat = np.asarray(tmp, dtype=object)
    #return mat
    return []
"""

"""
Créer une matrice nxn, rempli d'entier aléatoire de 0 à grid_maxValue
"""
def creer_matrice(n):
	mat = np.empty((n, n), object)

	for i in range(n):
		for j in range(n):
			rand_num = np.random.randint(grid_minValue, grid_maxValue)
			case = rand_num
			mat[i, j] = case

	#print(mat)
	return mat

"""
Renvoi la matrice m avec une bordure de chaque côtés
"""
def creer_bordure(m):
	#m.size contient le nombre total d'élément, pour n = 5, size = 25
	#m.shape contient la forme de la matrice, pour n = 5, shape = (5, 5), puisque c'est une matrice carré
	n = get_taille_matrice(m) + 2 # +2 pour obtenir une bordure de chaque côté
	M = np.random.randint(grid_minValue, grid_maxValue, size=(n, n))

	for i in range(1, n-1):
		for j in range(1, n-1):
			M[i, j] = m[i-1, j-1]
	#print(M)
	return M

"""
Remplace la bordure de la matrice m par la valeur "infini"
"""
def remplacement_bordure(m):
	n = get_taille_matrice(m)
	for i in range(n):
		m[i, 0] = inf_value
		m[0, i] = inf_value
		m[n - i -1, n - 1] = inf_value
		m[n - 1 , n - i -1] = inf_value
	return m

"""
Renvoi les 8 voisins disponibles de la matrice m, à partir de la position x, y
Si 1 voisin est en dehors des dimensions de la matrice carré, il n'est pas pris en compte
"""
def voisins_matrice(m, x, y, get_Indices=False):
	m_size = get_taille_matrice(m)
	voisins = []
	for i in range(-1, 2): #va de -1, 0, 1
		for j in range(-1, 2):
			if i == 0 and j == 0: continue #il s'agit de la case x, y ce n'est pas un voisin.
			v_X = x + i
			v_Y = y + j
			voisins.append(m[v_X, v_Y])
			
	return voisins

def voisins_indices_matrice(m, x, y):
	return voisins_matrice(m, x, y, get_Indices=True)

def num_cases_voisines(numCase, dim_terrain):
	return [numCase - dim_terrain - 1, numCase - dim_terrain, numCase - dim_terrain + 1,
			numCase - 1, numCase + 1,
			numCase + dim_terrain - 1, numCase + dim_terrain, numCase + dim_terrain + 1]

"""
Calcule la moyenne d'une liste
"""
def calc_moyenne(l):
    moy = 0
    n = len(l)
    for elmt in l:
        if isinstance(elmt, int):
            moy += elmt
    moy /= n
    return int(moy)

"""
Renvoi la valeur médian de la liste voisin
"""
def median_voisin(v):
	if len(v)%2 == 0:
		m = v[int(len(v)/2) - 1] + v[int(len(v)/2)]
		return m/2
	return v[int(len(v)/2)]

"""
Renvoi la matrice (carré avec bordure) moyenné?
Itère sur chaque case de la matrice,
Récupère les 8 voisins de la case courante
Calcule la moyenne des voisins
Remplace la valeur de la case courante par la moyenne calculé
"""
def moyenne_matrice(m):
	taille = get_taille_matrice(m)
	for i in range(1, taille - 1):
		for j in range(1, taille - 1):
			v = voisins_matrice(m, i, j)
			moy = calc_moyenne(v)
			m[i, j].Value = moy
	return m

def moyenne_mediane_matrice(m):
	taille = get_taille_matrice(m)
	m_tmp = m.copy()
	for i in range(1, taille - 1):
		for j in range(1, taille - 1):
			v = voisins_matrice(m, i, j)
			v.sort()
			moy = median_voisin(v)
			m_tmp[i, j] = moy
	return m_tmp

def generer_matrice_final(n=None, nbr_Passe_Moyenne=1):
	if n is None:
		n = grid_size
	mat = creer_matrice(n)
	mat = creer_bordure(mat)
	for i in range(nbr_Passe_Moyenne):
		mat = moyenne_mediane_matrice(mat)
	mat = remplacement_bordure(mat)
	return mat

if __name__ == "__main__":
    #m = gen_rand_grid(grid_maxValue, (grid_sizeX, grid_sizeY))

	#ETAPE 1 : créer matrice nxn
	#n = 5
	#creer_matrice(n)  #créer une matrice 5x5
	mat = creer_matrice(grid_size)
	#print("Matrice générée :\n", mat)
	#print("Point départ: {x}, {y} => {valeur}".format(x=0, y=2, valeur=m[0, 2]))

	#ETAPE 2 : bordure n + 1
	M = creer_bordure(mat)
	#print("Bordure générée :\n", M)
	#print("voisins :", voisins_matrice(M, 1, 1))

	#ETAPE 3 : Moyenne Matrice avec bordure
	#M_moy = moyenne_matrice(M)
	M_moy = moyenne_mediane_matrice(M)
	#print("calcul moyenne : ", calc_moyenne([1, 2, 4, 5, 7, 2, 3]))
	#print("Matrice Moyenne :\n", M_moy)

	#ETAPE 4 : Remplacement bordure par infini
	M_final = remplacement_bordure(M_moy)
	print("Matrice Final avec bordure:\n", M_final)
