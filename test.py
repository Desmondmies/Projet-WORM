import numpy as np

grid_sizeX, grid_sizeY = 20, 20
grid_maxValue = 10
inf_chance = 0.1
inf_value = 1000

def gen_rand_grid(_maxValue, _size):
	mat = np.random.randint(_maxValue, size=_size)
	#rempli aléatoirement la grille de valeur inf (-1)
	for i in range(len(mat)):
		for j in range(len(mat[i])):
			if np.random.rand() <= inf_chance:
				mat[i, j] = inf_value



	return mat

def main():
	m = gen_rand_grid(grid_maxValue, (grid_sizeX, grid_sizeY))
	print(m)
	print("Point départ: {x}, {y} => {valeur}".format(x=0, y=2, valeur=m[0, 2]))

if __name__ == "__main__":
    main()
