from OpenGL.GL import *

from Matrice.Matrice import grid_maxValue

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
def material_rose():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.9, 0.5, 0.9)) #rose
def material_trunc():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.98, 0.18, 0.18)) #marron
def material_vert_dijkstra():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0, 0.588, 0.098)) #vert
def material_bleu_a_star():
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0, 0.062, 0.639)) #bleu


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