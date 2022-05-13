import os

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from _3D.TerrainVertex import gen_terrain_data
from _3D.Camera3D import cam_lookAt, switch_cam, getCameraMode
from _3D.Worm3D import Worm3D
from _3D.Materials import material_hauteur, material_drapeau_pointDepart, material_drapeau_pointArrivee, material_poteau
from _3D.Apples import draw_apple

from Utilitaires.Utils import moyenne_pos_quad, convert_FromPixel_to_Terrain

window_name = "Projet WORM - 3D Edition"
width, height = 750, 750

taille_matrice = 15
terrain_offset = taille_matrice *1.45

cam_MoveX = 0

quadric = None

worm_animation_frame = 0

vertices = []
normals = []

drapeau_vertex = [ [0, 0, -1],
					[0, 0, 0],
					[1.5, 0.75, 0],
					[0, 1.5, 0]]

terrainData = []
bezier_dijkstra = []
bezier_a_star = []

worm_D = None
worm_A = None

focus_WormD = True
# ---------------------------------------------------

def open_chemin_file():
	path = "./Saves/chemins.txt"
	abs_path = os.path.abspath(path)
	f = open(abs_path, 'r')
	data = eval(f.read())
	return data

def init_light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.75, 0.75, 0.75, 0.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 0.0))

def init():
	global quadric, vertices, normals, terrainData, bezier_dijkstra, bezier_a_star, worm_A, worm_D
	glClearColor(12 / 255, 31 / 255, 50 / 255, 0.0) #20 53 85
	glEnable(GL_DEPTH_TEST)

	init_light()

	data_chemin = open_chemin_file()
	m = data_chemin["matrice"]
	terrainData = gen_terrain_data(m) #génère les données du terrain 3D à partir de la matrice

	bezier_dijkstra = data_chemin["bezier_dijkstra"]
	bezier_a_star = data_chemin["bezier_a_star"]

	glShadeModel(GL_SMOOTH)
	quadric = gluNewQuadric()

	worm_A = Worm3D(quadric, terrainData)
	worm_D = Worm3D(quadric, terrainData, _IsDijkstra=True)

# --------------------------------------------------- 

def draw_quad(quad):
    for vert in quad:
        material_hauteur(vert[1])
        glVertex3f(vert[0], vert[1], vert[2])

def draw_pts(p, _color = True):
	if _color:
		material_hauteur(p[1])
	glVertex3f(p[0], p[1], p[2])

def draw_triangle(tr, _colorOverride = True):
    normal_1 = tr[0]
    glNormal(normal_1[0], normal_1[1], normal_1[2])
    draw_pts(tr[1], _colorOverride)
    draw_pts(tr[2], _colorOverride)
    draw_pts(tr[3], _colorOverride)

# --------------------------------------------------- 

def display_terrain():
	#terrainData => [ quads, paliers, centres ]
	#quads => [ [quad, quad, quad], [quad, quad, quad]]

	glBegin(GL_QUADS)

	#dessine tout les QUADS
	glNormal(0, 1, 0) #normal de 1 sur l'axe y pour chaque quad
	for ligneQuad in terrainData["Quads"]:
		for quad in ligneQuad:
			draw_quad(quad)

	#dessine tout les PALIERS
	for palier in terrainData["Paliers"]:
		normal = palier[0]
		glNormal(normal[0], normal[1], normal[2])
		draw_pts(palier[1])
		draw_pts(palier[2])
		draw_pts(palier[3])
		draw_pts(palier[4])
	glEnd()

	glBegin(GL_TRIANGLES)
	#dessine tout les CENTRES
	for centres in terrainData["Centres"]:
		draw_triangle(centres[0])
		draw_triangle(centres[1])
	glEnd()

def display_camera():
	if getCameraMode() == False:
		glTranslatef(0.0, 0.0, 0.0)
		glRotatef(cam_MoveX, 0.0, 1.0, 0.0)
	else:
		if focus_WormD == True:
			pos = worm_D.getWormPosition()
		else:
			pos = worm_A.getWormPosition()
		glTranslatef(-(pos[0] - terrain_offset), terrain_offset, -(pos[2] - terrain_offset - 30))

def display_flag(isStartFlag = True):
	glPushMatrix()
	if isStartFlag == True:
		pos = convert_FromPixel_to_Terrain( bezier_dijkstra[0], len(terrainData["Quads"]) )
	else:
		pos = convert_FromPixel_to_Terrain( bezier_dijkstra[-1], len(terrainData["Quads"]) )
	pt_depart = moyenne_pos_quad(terrainData["Quads"][int(pos[0])][int(pos[1])])
	glTranslatef(pt_depart[2], pt_depart[1]+0.5, pt_depart[0])
	glRotatef(-90, 1, 0, 0)
	
	material_poteau()
	gluCylinder(quadric, 0.1, 0.1, 5, 10, 5)
	glPopMatrix()

	glPushMatrix()
	glTranslatef(pt_depart[2], pt_depart[1]+3.9, pt_depart[0])

	if isStartFlag == True:
		material_drapeau_pointDepart()
	else:
		material_drapeau_pointArrivee()

	glBegin(GL_TRIANGLES)
	draw_triangle(drapeau_vertex, _colorOverride=False) #dessine le drapeau
	glEnd()
	glPopMatrix()

def display_apples():
	max_idx = len(bezier_dijkstra) if len(bezier_dijkstra) >= len(bezier_a_star) else len(bezier_a_star)

	for i in range(14, max_idx, 20):
		if i < len(bezier_dijkstra):
			new_d_pos = convert_FromPixel_to_Terrain( bezier_dijkstra[ i ], len(terrainData["Quads"]) )
			pos_quad = terrainData["Quads"][ int( new_d_pos[1] ) ][ int( new_d_pos[0] ) ]
			moy_pos = moyenne_pos_quad(pos_quad)
			draw_apple( quadric, moy_pos )
		if i < len(bezier_a_star):
			new_a_pos = convert_FromPixel_to_Terrain( bezier_a_star[ i ], len(terrainData["Quads"]) )
			pos_quad = terrainData["Quads"][ int( new_a_pos[1] ) ][ int( new_a_pos[0] ) ]
			moy_pos = moyenne_pos_quad(pos_quad)
			draw_apple( quadric, moy_pos, isDijkstra=False )

# --------------------------------------------------- 

def display():
	global worm_animation_frame
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glPushMatrix()

	display_camera()

	glPushMatrix()
	glTranslatef(- terrain_offset, 0.0, - terrain_offset) #décale le terrain au milieu de l'écran

	display_terrain() #dessine le terrain

	display_flag()
	display_flag(isStartFlag=False)

	display_apples()

	if worm_animation_frame < len(bezier_dijkstra):
		new_d_pos = convert_FromPixel_to_Terrain( bezier_dijkstra[ int(worm_animation_frame) ], len(terrainData["Quads"]) )
		worm_D.set_wormPosition(new_d_pos[0]-0.1, new_d_pos[1]-0.1)
	if worm_animation_frame < len(bezier_a_star):
		new_a_pos = convert_FromPixel_to_Terrain( bezier_a_star[ int(worm_animation_frame) ], len(terrainData["Quads"]) )
		worm_A.set_wormPosition(new_a_pos[0]-0.1, new_a_pos[1]-0.1)

	worm_D.draw_worm()
	worm_A.draw_worm()

	#reset l'animation si les deux chemins sont finis
	if worm_animation_frame >= len(bezier_dijkstra) and worm_animation_frame >= len(bezier_a_star):
		worm_animation_frame = 0

	glPopMatrix()
	glPopMatrix()
	glutSwapBuffers()

# ---------------------------------------------------

def reshape(width, height):
	ar = float(width / height)
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity() #remplace la matrice actuel avec la matrice identité

	gluPerspective(70, ar, 1, 1000) # (fov Y, aspect ratio, z NearPlane, z FarPlane)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	# Positionne la caméra assez loin et un peu plus haut pour regarder le terrain

	#gluLookAt ( Position Caméra X Y Z, Caméra Target X Y Z, Vecteur vers le haut X Y Z )
	#gluLookAt(0.0, taille_matrice + 2, taille_matrice * 2,
	#0.0, 0.0, 0.0,
	#0.0, 1.0, 0.0)
	cam_lookAt( (0, taille_matrice+15, (taille_matrice*2)+5), (0, 0, 0), (0, 1, 0) )

# ---------------------------------------------------

def keyboard(key, x, y):
	global cam_MoveX, worm_animation_frame, focus_WormD

	if key == b' ':
		worm_animation_frame += 1.5

	if key == b'c':
		switch_cam(width, height)
	elif key == b'a':
		focus_WormD = False
	elif key == b'd':
		focus_WormD = True

	glutPostRedisplay()

def special_func(key, x, y):
	global cam_MoveX
	"""
	Special Func prend en compte "autres" touches du clavier? dont les flèches
	"""
	if key == GLUT_KEY_LEFT:
		cam_MoveX = (cam_MoveX + 2) % 360
	elif key == GLUT_KEY_RIGHT:
		cam_MoveX = (cam_MoveX - 2) % 360

	glutPostRedisplay()

# ---------------------------------------------------

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

glutCreateWindow(window_name)
glutReshapeWindow(width, height)

glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_func)

init()

glutMainLoop()
