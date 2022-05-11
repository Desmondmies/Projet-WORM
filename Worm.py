from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Utils import normalize_vec, angle, substract_list, moyenne_pos_quad

quadric = None
terrainQuad = None

worm_len = 0

worm = []

head_posX = 0
head_posY = 5
head_posZ = 0

init_PosX, init_PosZ = 0, 0
init_PosX_Terrain, init_PosZ_Terrain = 2, 2

head_rotationY = 0
rotationSpeed = 0.3

def init_worm(_quadric, terrainData, _worm_len = 7):
	global quadric, worm_len, worm, terrainQuad

	terrainQuad = terrainData["Quads"]
	#init_quad = terrainQuad[head_posZ][head_posX]
	#head_posX, head_posY, head_posZ = 0, 0, 0
	#head_posX, head_posY, head_posZ = moyenne_pos_quad(init_quad)

	quadric = _quadric
	worm_len = _worm_len
	worm = [[0, 0, 0]] * worm_len

def draw_part(pos, rot, size, drawEyes = False):
	if drawEyes is False:
		glTranslatef(pos, 0, 0)
	else:
		glTranslatef(pos[0], pos[1], pos[2])
	#glRotatef(rot, 0, 1, 0)
	gluSphere(quadric, size, 30, 20)

	if drawEyes:
		#glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.1, 0.1, 0.1)) #noir yeux
		#glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (41/255, 43/255, 173/255)) #bleu yeux
		eye_X_pos = (size / 2) + 0.1
		#draw_eyes(eye_X_pos)
		#draw_eyes(-eye_X_pos)

	#glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.8, 0.8, 0.5)) #beige patte
	#glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (224/255, 56/255, 72/255)) #rouge patte
	#draw_legs(-size/2)
	#draw_legs(size/2)

def draw_legs(size):
	glPushMatrix()
	glTranslatef(0.05, -0.15, size)
	gluSphere(quadric, size, 30, 20)
	glPopMatrix()

def draw_eyes(x_off):
	glPushMatrix()
	glTranslatef(x_off, 0, 0.1)
	gluSphere(quadric, 0.1, 30, 20)
	glPopMatrix()

def draw_worm():
	global worm, head_posY
	init_worm_size = 0.5

	glPushMatrix()

	pos_X_terrain = init_PosX + head_posX
	pos_Z_terrain = init_PosZ + head_posZ

	if pos_X_terrain < 0:
		pos_X_terrain = 0
	elif pos_X_terrain >= len(terrainQuad):
		pos_X_terrain = len(terrainQuad) - 1

	if pos_Z_terrain < 0:
		pos_Z_terrain = 0
	elif pos_Z_terrain >= len(terrainQuad):
		pos_Z_terrain = len(terrainQuad) - 1

	pos_quad = terrainQuad[ int(pos_Z_terrain) ][ int(pos_X_terrain) ]
	#worm[0] = [head_posX, head_posY, head_posZ]
	moy_pos = moyenne_pos_quad(pos_quad) #récupère à peu près le centre du quad
	moy_pos[0] = init_PosX_Terrain + head_posX*2
	moy_pos[2] = init_PosZ_Terrain + head_posZ*2
	moy_pos[1] += init_worm_size #remonte la tête du ver au dessus du sol

	head_posY = moy_pos[1]

	worm[0] = moy_pos

	#glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.1, 0.8, 0.1)) #vert tête
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.9, 0.5, 0.9)) #tête rose
	draw_part( worm[0], 0, init_worm_size, drawEyes=True) #dessine la tête

	for i in range(1, worm_len):
		taille = init_worm_size - 0.05
		dir = substract_list( worm[i], worm[i-1] )
		vec_unit = normalize_vec( dir )
		pos = [ vec_unit[0] * taille, vec_unit[1] * taille, vec_unit[2] * taille ]
		glTranslatef( pos[0], pos[1], pos[2] )
		draw_part(0, 0, taille)
		worm[i] = [ worm[i-1][0] + pos[0], worm[i-1][1] + pos[1], worm[i-1][2] + pos[2] ]
		init_worm_size = taille

	glPopMatrix()

def shortest_angle(_from, _to):
    """
    Renvoi l'angle de déplacement le + court pour aller de _from à _to
    """
    angle = ( ( (_to - _from) + 180) % 360) - 180
    return angle

def worm_moveX(direction):
	"""
	Bouge le ver sur l'axe X vers la direction
	normalement sa tête regarde dans la direction de déplacement
	"""
	global head_posX, head_rotationY
	head_posX += direction * 0.15 #direction * vitesse

	#make worm face direction
	#direction => 1 or -1
	#rotation vers la direction
	#if direction > 0:
	#	angle = shortest_angle(head_rotationY, 0)
	#else:
	#	angle = shortest_angle(head_rotationY, 180)
	#head_rotationY += (angle * rotationSpeed)
	#head_rotationY %= 360

def worm_moveZ(direction):
	"""
	Bouge le ver sur l'axe Z vers la direction
	normalement sa tête regarde dans la direction de déplacement
	"""
	global head_posZ, head_rotationY
	head_posZ += direction * 0.15

	#make worm face direction
	#direction => 1 or -1
	#rotation vers la direction
	#if direction > 0:
	#	angle = shortest_angle(head_rotationY, 270)
	#else:
	#	angle = shortest_angle(head_rotationY, 90)
	#head_rotationY += (angle * rotationSpeed)
	#head_rotationY %= 360

def getWormPosition():
	return (init_PosX_Terrain + head_posX*2, head_posY, init_PosZ_Terrain + head_posZ*2)
