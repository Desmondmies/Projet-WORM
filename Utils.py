from math import sqrt, acos

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

def angle(u, v):
	prod = produit_vec(u, v)
	norm_U = normalize_vec(u)
	norm_V = normalize_vec(v)
	value = prod[1] / (norm_U[1] * norm_V[1])
	if value < -1:
		value = -1
	elif value > 1:
		value = 1
	angle = acos( value )
	return angle

def substract_list(a, b):
	tmp = [ a[0] - b[0], a[1] - b[1], a[2] - b[2] ]
	return tmp