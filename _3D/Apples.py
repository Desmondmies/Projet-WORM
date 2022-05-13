from OpenGL.GL import *
from OpenGL.GLU import *

from _3D.Materials import material_bleu_a_star, material_vert_dijkstra, material_trunc

def draw_trunc(quadric):
    glPushMatrix()
    glTranslatef(0, 0.15, 0)
    glRotatef(-90, 1, 0, 0)

    glRotatef(-75, 0.3, 0, 1)

    material_trunc()
    gluCylinder(quadric, 0.001, 0.03, 0.23, 10, 5)
    glPopMatrix()

def draw_applebody(quadric):
    glPushMatrix()
    glTranslatef(-0.1, 0, 0)
    glScalef(0.7, 1, 1)
    gluSphere(quadric, 0.2, 30, 10)
    glTranslatef(0.2, 0, 0)
    gluSphere(quadric, 0.2, 30, 10)

    glPopMatrix()

def draw_apple(quadric, pos, isDijkstra = True):
    glPushMatrix()
    glTranslatef(pos[0], pos[1]+0.3, pos[2])

    if isDijkstra == True:
        material_vert_dijkstra()
    else:
        material_bleu_a_star()

    draw_applebody(quadric)
    draw_trunc(quadric)

    glPopMatrix()