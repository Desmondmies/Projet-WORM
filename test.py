import numpy as np

#grid_sizeX, grid_sizeY = 20, 20
grid_maxValue = 20
inf_chance = 0.1
inf_value = 1000

#numpy perlin noise : https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html

"""
test pour créer une matrice nxn avec valeur aléatoire et infini

def gen_rand_grid(_maxValue, _size):
	mat = np.random.randint(_maxValue, size=_size)
	mat = mat.astype(float)
	#rempli aléatoirement la grille de valeur inf (-1)
	for i in range(len(mat)):
		for j in range(len(mat[i])):
			if np.random.rand() <= inf_chance:
				num = np.float32(np.inf)
				mat[i, j] = num
	
	mat = mat.astype(int)

	print(-2147483648 == np.int32(np.inf)) #probleme conversion infini en int, comment garder une matrice d'int avec infini dedans???
	return mat
"""

"""
Renvoi la taille n de la matrice carré
"""
def get_taille_matrice(m):
	return m.shape[0]

"""
Créer une matrice nxn, rempli d'entier aléatoire de 0 à grid_maxValue
"""
def creer_matrice(n):
	mat = np.random.randint(grid_maxValue, size=(n,n))
	return mat

"""
Renvoi la matrice m avec une bordure de chaque côtés
"""
def creer_bordure(m):
	#m.size contient le nombre total d'élément, pour n = 5, size = 25
	#m.shape contient la forme de la matrice, pour n = 5, shape = (5, 5), puisque c'est une matrice carré
	n = get_taille_matrice(m) + 2 # +2 pour obtenir une bordure de chaque côté
	M = np.zeros((n,n), dtype=int)

	for i in range(1, n-1):
		for j in range(1, n-1):
			M[i, j] = m[i-1, j-1]
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
def voisins_matrice(m, x, y):
	m_size = get_taille_matrice(m)
	voisins = []
	for i in range(-1, 2): #va de -1, 0, 1
		for j in range(-1, 2):
			if i == 0 and j == 0: #il s'agit de la case x, y ce n'est pas un voisin.
				continue
			v_X = x + i
			v_Y = y + j

			if v_X >= 0 and v_X < m_size and v_Y >= 0 and v_Y < m_size:
				voisins.append(m[v_X, v_Y])
	return voisins

"""
Calcule la moyenne d'une liste
"""
def calc_moyenne(l):
	moy = 0
	n = len(l)
	for elmt in l:
		moy += elmt
	moy /= n
	return moy

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
			m[i, j] = moy
	return m

# -----------------------------------------------------------------------------

def main():
	#m = gen_rand_grid(grid_maxValue, (grid_sizeX, grid_sizeY))

	#ETAPE 1 : créer matrice nxn
	n = 5
	mat = creer_matrice(n) #créer une matrice 5x5
	#print("Matrice générée :\n", mat)
	#print("Point départ: {x}, {y} => {valeur}".format(x=0, y=2, valeur=m[0, 2]))

	#ETAPE 2 : bordure n + 1
	M = creer_bordure(mat)
	#print("Bordure générée :\n", M)
	#print("voisins :", voisins_matrice(M, 1, 1))

	#ETAPE 3 : Moyenne Matrice avec bordure
	M_moy = moyenne_matrice(M)
	#print("calcul moyenne : ", calc_moyenne([1, 2, 4, 5, 7, 2, 3]))
	#print("Matrice Moyenne :\n", M_moy)

	#ETAPE 4 : Remplacement bordure par infini
	M_final = remplacement_bordure(M_moy)
	print("Matrice Final avec bordure:\n", M_final)

if __name__ == "__main__":
    main()
