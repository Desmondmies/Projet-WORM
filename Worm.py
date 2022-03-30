from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

head_posX = 10
head_posY = 5
head_posZ = 10

head_rotationY = 0

def draw_eyes(quadric, x_off = 1):
    glPushMatrix()
    glTranslatef(x_off, 0, -0.1)
    gluSphere(quadric, 0.1, 30, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x_off, 0, 0.1)
    gluSphere(quadric, 0.1, 30, 20)
    glPopMatrix()

def draw_legs(quadric, size, z_off = 1):
    glPushMatrix()
    glTranslatef(0.05, -0.15, z_off)
    gluSphere(quadric, size, 30, 20)
    glPopMatrix()

def draw_body(quadric, size = 0.75, size_offset = 0.1):
    new_size = size - size_offset
    glTranslatef(-(new_size + 0.15), -(size_offset/2), 0)
    glRotatef(head_rotationY - size_offset, 0, 1, 0) #?
    gluSphere(quadric, new_size, 30, 20)


    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.8, 0.8, 0.5)) #beige patte
    off = (new_size / 2)
    draw_legs(quadric, new_size / 2, off)
    draw_legs(quadric, new_size / 2, -off)
    return new_size

def draw_head(quadric, worm_size):
    glTranslatef(head_posX, head_posY, head_posZ)
    glRotatef(head_rotationY, 0, 1, 0)
    gluSphere(quadric, worm_size, 30, 20)

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.1, 0.1, 0.1)) #noir yeux
    off = (worm_size / 2)
    draw_eyes(quadric, off+0.1)

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.8, 0.8, 0.5)) #beige patte
    draw_legs(quadric, worm_size / 2, off)
    draw_legs(quadric, worm_size / 2, -off)

def draw_worm(quadric, worm_size = 0.35, worm_length = 7):
    glPushMatrix()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.1, 0.8, 0.1)) #vert tête
    draw_head(quadric, worm_size)

    size_off = worm_size / worm_length
    for i in range(worm_length):
        if worm_size < 0.2: break
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.1, 0.8, 0.1)) #vert corps
        worm_size = draw_body(quadric, worm_size, size_off)

    glPopMatrix()

def worm_moveX(direction):
    global head_posX, head_rotationY
    head_posX += direction * 0.3 #direction * vitesse

    #make worm face direction
    #direction => 1 or -1
    #rotation vers la direction

def worm_moveZ(direction):
    global head_posZ, head_rotationY
    head_posZ += direction * 0.3



