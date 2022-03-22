import numpy as np

from Matrice import generer_matrice_final
from Dijkstra import dijkstra

#grid_sizeX, grid_sizeY = 20, 20
grid_size = 10
grid_maxValue = 50
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

# -----------------------------------------------------------------------------

def main():
	m = generer_matrice_final()
	#print(m)
	path = dijkstra(m, m[1, 1])
	print(path)


if __name__ == "__main__":
    main()
