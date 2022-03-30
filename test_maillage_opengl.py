from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Matrice import generer_matrice_final, obstacle_matrice, grid_maxValue
from TerrainVertex import gen_terrain_data
from Worm import draw_worm, worm_moveX, worm_moveZ

window_name = "TEST MAILLAGE"
width, height = 750, 750

taille_matrice = 10
terrain_offset = taille_matrice + (taille_matrice/6)

cam_MoveX, cam_MoveZ = 0, 0

quadric = None

vertices = []
normals = []

terrainData = []
# ---------------------------------------------------

def init_light():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.75, 0.75, 0.75, 0.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 0.0))

def init():
    global quadric, vertices, normals, terrainData
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glEnable(GL_DEPTH_TEST)
    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    init_light()

    vertices = [-1.0, 0.0, -1.0,
                1.0, 0.0, 1.0,
                -1.0, 0.0, 1.0,
                -1.0, 0.0, -1.0,
                1.0, 0.0, -1.0,
                1.0, 0.0, 1.0]

    m = generer_matrice_final(taille_matrice)
    m = obstacle_matrice(m, 4, 3, sizeX=4)
    m = obstacle_matrice(m, 4, 3, sizeY=3)
    terrainData = gen_terrain_data(m)

    glShadeModel(GL_SMOOTH)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)

def material_obstacle():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0, 0, 0))
def material_ocean():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.3, 0.7, 0.7))
def material_sable():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (1, 0.88, 0.5))
def material_herbe():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.3, 1, 0.3))
def material_neige():
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.8, 0.8, 0.8))

def material_hauteur(h):
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
def draw_pts(p):
    material_hauteur(p[1])
    glVertex3f(p[0], p[1], p[2])

def draw_triangle(tr):
    normal_1 = tr[0]
    glNormal(normal_1[0], normal_1[1], normal_1[2])
    draw_pts(tr[1])
    draw_pts(tr[2])
    draw_pts(tr[3])

def display_terrain():
    #terrainData => [ quads, paliers, centres ]
    #quads => [ [quad, quad, quad], [quad, quad, quad]]

    glNormal(0, 1, 0)
    glBegin(GL_QUADS)
    #glColor4f(0.2, 0.8, 0.2, 1.0)
    #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.2, 0.5, 0.2)) #material herbe
    #QUADS
    for ligneQuad in terrainData["Quads"]:
        for quad in ligneQuad:
            draw_quad(quad)

    #PALIERS
    #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.3, 0.3, 0.32)) #material rock
    #glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.2, 0.4, 0.2)) #material herbe2
    for palier in terrainData["Paliers"]:
        normal = palier[0]
        glNormal(normal[0], normal[1], normal[2])
        draw_pts(palier[1])
        draw_pts(palier[2])
        draw_pts(palier[3])
        draw_pts(palier[4])
    glEnd()

    glBegin(GL_TRIANGLES)
    #CENTRES
    for centres in terrainData["Centres"]:
        draw_triangle(centres[0])
        draw_triangle(centres[1])
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glTranslatef(0.0, 0.0, cam_MoveZ)
    glRotatef(cam_MoveX, 0.0, 1.0, 0.0)

    glPushMatrix()
    glTranslatef(- terrain_offset, 0.0, - terrain_offset)
    display_terrain()

    draw_worm(quadric)

    glPopMatrix()
    glPopMatrix()
    glutSwapBuffers()

def reshape(width, height):
    ar = float(width / height)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() #remplace la matrice actuel avec la matrice identité

    gluPerspective(70, ar, 1, 500) # (fov Y, aspect ratio, z NearPlane, z FarPlane)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0.0, taille_matrice + 2, taille_matrice * 2,
    0.0, 0.0, 0.0,
    0.0, 1.0, 0.0)

def keyboard(key, x, y):
    global cam_MoveX, cam_MoveZ

    if key == b'z':
        cam_MoveZ = (cam_MoveZ + 0.5) % 360
    elif key == b's':
        cam_MoveZ = (cam_MoveZ - 0.5) % 360
    if key == b'q':
        cam_MoveX = (cam_MoveX + 2) % 360
    elif key == b'd':
        cam_MoveX = (cam_MoveX - 2) % 360

    glutPostRedisplay()

def special_func(key, x, y):
    if key == GLUT_KEY_UP:
        worm_moveZ(-1)
    elif key == GLUT_KEY_DOWN:
        worm_moveZ(1)
    elif key == GLUT_KEY_LEFT:
        worm_moveX(-1)
    elif key == GLUT_KEY_RIGHT:
        worm_moveX(1)

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
