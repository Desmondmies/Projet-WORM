from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

head_posX = 10
head_posY = 5
head_posZ = 10

head_rotationY = 0
rotationSpeed = 0.3

last_dirX, last_dirZ = 0, 0
lerpTimeX, lerpTimeZ = 0, 0

def draw_eyes(quadric, x_off = 1):
    """
    Dessine les deux yeux de l'asticot
    """
    glPushMatrix()
    glTranslatef(x_off, 0, -0.1)
    gluSphere(quadric, 0.1, 30, 20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x_off, 0, 0.1)
    gluSphere(quadric, 0.1, 30, 20)
    glPopMatrix()

def draw_legs(quadric, size, z_off = 1):
    """
    Dessine 1 jambes de l'asticot
    """
    glPushMatrix()
    glTranslatef(0.05, -0.15, z_off)
    gluSphere(quadric, size, 30, 20)
    glPopMatrix()

def draw_body(quadric, size = 0.75, size_offset = 0.1, rotationOffset = 0):
    """
    Dessine le corps, rotation incorrect
    puis dessine les 2 jambes
    """
    new_size = size - size_offset
    glTranslatef(-(new_size + 0.15), -(size_offset/2), 0)
    glRotatef(rotationOffset, 0, 1, 0) #?
    gluSphere(quadric, new_size, 30, 20)

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.8, 0.8, 0.5)) #beige patte
    off = (new_size / 2)
    draw_legs(quadric, new_size / 2, off)
    draw_legs(quadric, new_size / 2, -off)
    return new_size

def draw_head(quadric, worm_size):
    """
    dessine la tête et les yeux + jambes
    """
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
    """
    Dessine tout le ver
    """
    glPushMatrix()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.1, 0.8, 0.1)) #vert tête
    draw_head(quadric, worm_size)

    size_off = worm_size / worm_length
    for i in range(worm_length):
        if worm_size < 0.2: break
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.1, 0.8, 0.1)) #vert corps
        worm_size = draw_body(quadric, worm_size, size_off, (i+2 * head_rotationY) / 360)

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
    head_posX += direction * 0.3 #direction * vitesse

    #make worm face direction
    #direction => 1 or -1
    #rotation vers la direction
    if direction > 0:
        angle = shortest_angle(head_rotationY, 0)
        head_rotationY += (angle * rotationSpeed) % 360
    else:
        angle = shortest_angle(head_rotationY, 180)
        head_rotationY += (angle * rotationSpeed) % 360

def worm_moveZ(direction):
    """
    Bouge le ver sur l'axe Z vers la direction
    normalement sa tête regarde dans la direction de déplacement
    """
    global head_posZ, head_rotationY
    head_posZ += direction * 0.3

    #make worm face direction
    #direction => 1 or -1
    #rotation vers la direction
    if direction > 0:
        angle = shortest_angle(head_rotationY, 270)
        head_rotationY += (angle * rotationSpeed) % 360
    else:
        angle = shortest_angle(head_rotationY, 90)
        head_rotationY += (angle * rotationSpeed) % 360