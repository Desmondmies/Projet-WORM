import os

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Matrice import grid_maxValue
from TerrainVertex import gen_terrain_data
from Camera3D import cam_lookAt, switch_cam, getCameraMode
from Utils import moyenne_pos_quad, convert_FromPixel_to_Terrain
from Worm3D import Worm3D

window_name = "TEST MAILLAGE"
width, height = 750, 750

taille_matrice = 15
terrain_offset = taille_matrice + (taille_matrice/6)

cam_MoveX, cam_MoveZ = 0, 0

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
	#gluQuadricDrawStyle(quadric, GLU_LINE)

def material_obstacle():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0, 0, 0)) #noir
def material_ocean():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.3, 0.7, 0.7)) #bleu
def material_sable():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (1, 0.88, 0.5)) #couleur sable?
def material_herbe():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.3, 1, 0.3)) #vert
def material_neige():
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.8, 0.8, 0.8)) #blanc
def material_poteau():
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.44, 0.45, 0.5)) #gris
def material_drapeau_pointDepart():
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.38, 0.92, 0.98)) #cyan
def material_drapeau_pointArrivee():
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.98, 0.18, 0.18)) #rouge

def material_hauteur(h):
    """
    Renvoi le materiel nécéssaire selon la hauteur Y du point
    """
    hauteur_ratio = h / grid_maxValue
    if hauteur_ratio < 0:
        material_obstacle()
    elif hauteur_ratio <= 0.15:
        material_ocean()
    elif hauteur_ratio <= 0.23:
        material_sable()
    elif hauteur_ratio <= 0.35:
        material_herbe()
    else:
        material_neige()

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
		glTranslatef(0.0, 0.0, cam_MoveZ)
		glRotatef(cam_MoveX, 0.0, 1.0, 0.0)
	else:
		# pos = getWormPosition()
		pos = worm_D.getWormPosition()
		glTranslatef(-(pos[0] - terrain_offset), 0, -(pos[2] - terrain_offset))


def display_point_depart():
	glPushMatrix()
	pos = convert_FromPixel_to_Terrain( bezier_dijkstra[0], len(terrainData["Quads"]) )
	pt_depart = moyenne_pos_quad(terrainData["Quads"][int(pos[0])][int(pos[1])])
	glTranslatef(pt_depart[2], pt_depart[1]+0.5, pt_depart[0])
	glRotatef(-90, 1, 0, 0)

	material_poteau()
	gluCylinder(quadric, 0.1, 0.1, 5, 10, 5)
	glPopMatrix()

	glPushMatrix()
	glTranslatef(pt_depart[2], pt_depart[1]+3.9, pt_depart[0])
	material_drapeau_pointDepart()

	glBegin(GL_TRIANGLES)
	draw_triangle(drapeau_vertex, _colorOverride=False) #dessine le drapeau
	glEnd()
	glPopMatrix()

def display_point_arrivee():
	glPushMatrix()
	pos = convert_FromPixel_to_Terrain( bezier_dijkstra[-1], len(terrainData["Quads"]) )
	pt_depart = moyenne_pos_quad(terrainData["Quads"][int(pos[0])][int(pos[1])])
	glTranslatef(pt_depart[2], pt_depart[1]+0.5, pt_depart[0])
	glRotatef(-90, 1, 0, 0)

	material_poteau()
	gluCylinder(quadric, 0.1, 0.1, 5, 10, 5)
	glPopMatrix()

	glPushMatrix()
	glTranslatef(pt_depart[2], pt_depart[1]+3.9, pt_depart[0])
	material_drapeau_pointArrivee()

	glBegin(GL_TRIANGLES)
	draw_triangle(drapeau_vertex, _colorOverride=False) #dessine le drapeau
	glEnd()
	glPopMatrix()


def display():
	global worm_animation_frame
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glPushMatrix()

	display_camera()

	glPushMatrix()
	glTranslatef(- terrain_offset, 0.0, - terrain_offset) #décale le terrain au milieu de l'écran

	display_terrain() #dessine le terrain

	display_point_depart()
	display_point_arrivee()

	if worm_animation_frame < len(bezier_dijkstra)-1:
		new_d_pos = convert_FromPixel_to_Terrain( bezier_dijkstra[ int(worm_animation_frame) ], len(terrainData["Quads"]) )
		worm_D.set_wormPosition(new_d_pos[0]-0.1, new_d_pos[1]-0.1)
	if worm_animation_frame < len(bezier_a_star)-1:
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
	cam_lookAt( (0, taille_matrice+2, taille_matrice*2), (0, 0, 0), (0, 1, 0) )

def keyboard(key, x, y):
	global cam_MoveX, cam_MoveZ, worm_animation_frame

	if key == b'z':
		cam_MoveZ = (cam_MoveZ + 0.5) % 360
	elif key == b's':
		cam_MoveZ = (cam_MoveZ - 0.5) % 360
	if key == b'q':
		cam_MoveX = (cam_MoveX + 2) % 360
	elif key == b'd':
		cam_MoveX = (cam_MoveX - 2) % 360
	elif key == b' ':
		worm_animation_frame += 0.5

	if key == b'c':
		switch_cam(width, height)

	glutPostRedisplay()

# def special_func(key, x, y):
#     """
#     Special Func prend en compte "autres" touches du clavier? dont les flèches
#     """
#     # if key == GLUT_KEY_UP:
#     #     worm_moveZ(-1)
#     # elif key == GLUT_KEY_DOWN:
#     #     worm_moveZ(1)
#     # elif key == GLUT_KEY_LEFT:
#     #     worm_moveX(-1)
#     # elif key == GLUT_KEY_RIGHT:
#     #     worm_moveX(1)

#     glutPostRedisplay()


# ---------------------------------------------------

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

glutCreateWindow(window_name)
glutReshapeWindow(width, height)

glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
# glutSpecialFunc(special_func)

init()

glutMainLoop()
