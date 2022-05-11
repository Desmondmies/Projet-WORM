from Utils import calc_vec, normalize_vec, produit_vec
from Matrice import inf_value

"""
def get_vertex(i, j):
    v = [ 2*i, 0, 2*j,
          2*(i+1), 0, 2*(j+1),
          2*i, 0, 2*(j+1),
          2*i, 0, 2*j,
          2*(i+1), 0, 2*j,
          2*(i+1), 0, 2*(j+1)]
    return v
"""

"""
Renvoi les 4 coordonnées nécéssaires à la définition d'1 quadrilatère
"""
def get_quad(i, y, j):
	v = [ [2*i, y, 2*j],
		  [2*i+1, y, 2*j],
          [2*i+1, y, 2*j+1],
		  [2*i, y, 2*j+1]
		]
	return v

"""
Renvoi les composantes nécéssaires pour définir 1 palier droit, avec 1 composante de Normale
Défini entre 2 quadrilatère
"""
def get_palier_droite(quad1, quad2):
	VecX = calc_vec(quad1[2], quad2[3])
	VecZ = calc_vec(quad1[2], quad1[1])
	normal = produit_vec(VecX, VecZ)
	normal = normalize_vec(normal)
	v = [ normal,
	 	  quad1[2],
		  quad1[1],
		  quad2[0],
		  quad2[3]
		]
	return v

"""
Renvoi les composantes nécéssaires pour définir 1 palier vers le bas, avec 1 composante de Normal
Défini entre 2 quadrilatère
"""
def get_palier_bas(quad1, quad2):
	VecX = calc_vec(quad1[0], quad1[1])
	VecZ = calc_vec(quad1[0], quad2[3])
	normal = produit_vec(VecX, VecZ)
	normal = normalize_vec(normal)
	v = [ normal,
		  quad1[1],
		  quad1[0],
		  quad2[3],
		  quad2[2] ]
	return v

"""
Renvoi les composantes nécéssaires pour définir 1 centre situé au milieu de 4 quadrilatères, avec les composantes de normal
"""
def get_centre(quad1, quad2, quad3, quad4):
	#quad1 quad4
	#quad2 quad3
	pts2_vecX = calc_vec(quad2[2], quad3[3])
	pts2_vecZ = calc_vec(quad1[1], quad2[2])
	pts2_normal = produit_vec(pts2_vecZ, pts2_vecX)
	pts2_normal = normalize_vec(pts2_normal)

	pts4_vecX = calc_vec(quad4[0], quad1[1])
	pts4_vecZ = calc_vec(quad4[0], quad3[3])
	pts4_normal = produit_vec(pts4_vecX, pts4_vecZ)
	pts4_normal = normalize_vec(pts4_normal)

	v = [ [ pts2_normal,
		    quad1[2],
			quad2[1],
			quad3[0] ],
		  [ pts4_normal,
		  	quad1[2],
			quad3[0],
			quad4[3] ]
		]
	return v

"""
Génère les données du terrain,
Etape 1 : les quadrilatères
Etape 2 : les paliers entre quadrilatères (droite et bas)
Etape 3 : les centres entre 4 quadrilatères (diagonales de chaque quadrilatères)
"""
def gen_terrain_data(matrice):
	quads = gen_terrain_quad(matrice)
	paliers = gen_terrain_palier(quads)
	centres = gen_terrain_centre(quads)

	terrainData = {"Quads": quads,
					"Paliers": paliers,
					"Centres": centres}
	return terrainData

"""
Génère pour toute la matrice les quadrilatères espacés d'1 case, en prenant compte de la hauteur depuis la matrice donnée en paramètre
"""
def gen_terrain_quad(matrice):
	n = len(matrice)
	lignesQuads = []

	for i in range(1, n-1):
		ligne = []
		for j in range(1, n-1):
			if matrice[i][j] != inf_value:
				y = matrice[i][j] / 2
			else:
				y = -1
			quad = get_quad(j, y, i)
			ligne.append(quad)
		lignesQuads.append(ligne)
	#print(vertex)
	return lignesQuads

"""
Génère tout les paliers entre quadrilatères
"""
def gen_terrain_palier(lignesQuads):
	n = len(lignesQuads)
	paliers = []

	for i in range(n):
		for j in range(n):
			if j < n-1:
				#palier de droite
				palierDroite = get_palier_droite(lignesQuads[i][j], lignesQuads[i][j + 1])
				paliers.append(palierDroite)
			if i < n-1:
				#palier du bas
				palierBas = get_palier_bas(lignesQuads[i + 1][j], lignesQuads[i][j])
				paliers.append(palierBas)
	return paliers

"""
Génère tout les centres entre chaque diagonale de quadrilatère
"""
def gen_terrain_centre(lignesQuads):
	n = len(lignesQuads)
	centres = []

	for i in range(n):
		for j in range(n):
			if j < n-1 and i < n-1:
				centreDiag = get_centre(lignesQuads[i][j], lignesQuads[i+1][j],
										lignesQuads[i+1][j+1], lignesQuads[i][j+1])
				centres.append(centreDiag)
	return centres
