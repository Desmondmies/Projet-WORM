from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Matrice import generer_matrice_final
from TerrainVertex import gen_terrain_vertex

window_name = "TEST MAILLAGE"
width, height = 750, 750


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

    init_light()

    vertices = [-1.0, 0.0, -1.0, 
                1.0, 0.0, 1.0,
                -1.0, 0.0, 1.0,
                -1.0, 0.0, -1.0,
                1.0, 0.0, -1.0,
                1.0, 0.0, 1.0]

    n = 5
    m = generer_matrice_final(n)
    terrainData = gen_terrain_vertex(m)

    glShadeModel(GL_SMOOTH)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)

def display_terrain():
    glEnableClientState(GL_VERTEX_ARRAY)

    #glColor4f( 1.0, 1.0, 1.0, 1.0 )
    #glVertexPointer(3, GL_FLOAT, 0, vertices) #nbr composante par vertex (x, y, z), type de données, etc 
    glVertexPointer(3, GL_FLOAT, 0, terrainData)
    #glDrawArrays(GL_TRIANGLE_STRIP, 0, 6) #mode, 1er indice, nbr d'indice à afficher
    glDrawArrays(GL_LINE_STRIP, 0, len(terrainData)) #uniquement pour tester

    glDisableClientState(GL_VERTEX_ARRAY)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()
    glTranslatef(0.0, 0.0, cam_MoveZ)
    glRotatef(cam_MoveX, 0.0, 1.0, 0.0)

    glPushMatrix()
    glTranslatef(-7.0, 0.0, -7.0)
    display_terrain()

    glPopMatrix()
    glPopMatrix()
    glutSwapBuffers()

def reshape(width, height):
    ar = float(width / height)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() #remplace la matrice actuel avec la matrice identité

    gluPerspective(70, ar, 1, 100) # (fov Y, aspect ratio, z NearPlane, z FarPlane)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(0.0, 7.0, 15,
    0.0, 0.0, 0.0,
    0.0, 1.0, 0.0)

def keyboard(key, x, y):
    global cam_MoveX, cam_MoveZ

    if key == b'z':
        cam_MoveZ = (cam_MoveZ + 0.1) % 360
    elif key == b's':
        cam_MoveZ = (cam_MoveZ - 0.1) % 360
    if key == b'q':
        cam_MoveX = (cam_MoveX + 1) % 360
    elif key == b'd':
        cam_MoveX = (cam_MoveX - 1) % 360
    
    glutPostRedisplay()


# ---------------------------------------------------

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

glutCreateWindow(window_name)
glutReshapeWindow(width, height)

glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

init()

glutMainLoop()