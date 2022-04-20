from math import sqrt

def produit_vec(u, v):
	if len(u) != len(v):
		return None

	uv0 = u[1] * v[2] - u[2] * v[1]
	uv1 = u[2] * v[0] - u[0] * v[2]
	uv2 = u[0] * v[1] - u[1] * v[0]
	return [uv0, uv1, uv2]

def normalize_vec(v):
	norme = sqrt( v[0]*v[0] + v[1]*v[1] + v[2]*v[2] )
	return [ v[0]/norme, v[1]/norme, v[2]/norme ]

def calc_vec(pts1, pts2):
	return [pts2[0] - pts1[0], pts2[1] - pts1[1], pts2[2] - pts1[2]]

def coord_numCase(x, y, dim_mat):
	return y * dim_mat + x

def numCase_coord(numCase, dim_mat):
	coord = []
	coord.append(numCase % dim_mat)
	coord.append(int((numCase - coord[0]) / dim_mat))
	return coord 

def horner(x, p):
    res = 0
    for coeff in p:
        res *= x
        res += coeff
    return res
