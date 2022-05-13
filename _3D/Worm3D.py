from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Utilitaires.Utils import normalize_vec, substract_list, moyenne_pos_quad
from _3D.Materials import material_rose, material_bleu_a_star, material_vert_dijkstra

class Worm3D:
    def __init__(self, _quadric, terrainData, _worm_len = 7, _IsDijkstra = False) -> None:
        self.quadric = _quadric
        self.terrainQuad = terrainData["Quads"]
        self.terrainLen = len(self.terrainQuad)

        self.worm_len = _worm_len
        self.init_worm_size = 0.5

        self.worm = [[0, 0, 0]] * _worm_len

        self.isDijkstra = _IsDijkstra

        self.headPos = [0, 5, 0]

        self.initPos = [0, 0]
        self.initTerrainPos = [2, 2]

    def dijkstra_or_aStar_Material(self):
        if self.isDijkstra:
            material_vert_dijkstra()
        else:
            material_bleu_a_star()

    def draw_part(self, pos, size):
        glTranslatef(pos[0], pos[1], pos[2])
        gluSphere(self.quadric, size, 30, 20)

    def draw_worm(self):
        """
        Dessine le ver complet, d'abord sa tête à partir de sa position prédéfini
        Il récupère les coordonnées moyennes de la cases du terrain sur laquelle il se situe
        et adapte sa hauteur en fonction

        puis le tracé du corps fera le reste pour ce qui concerne l'aspect ver de terre dans les mouvements du mobile
        """
        glPushMatrix()
        current_worm_size = self.init_worm_size

        pos_X_terrain = self.initPos[0] + self.headPos[0]
        pos_Z_terrain = self.initPos[1] + self.headPos[2]

        if pos_X_terrain < 0:
            pos_X_terrain = 0
        elif pos_X_terrain >= self.terrainLen:
            pos_X_terrain = self.terrainLen - 1

        if pos_Z_terrain < 0:
            pos_Z_terrain = 0
        elif pos_Z_terrain >= self.terrainLen:
            pos_Z_terrain = self.terrainLen - 1

        pos_quad = self.terrainQuad[ int(pos_Z_terrain) ][ int(pos_X_terrain) ]
        moy_pos = moyenne_pos_quad(pos_quad) #récupère à peu près le centre du quad
        moy_pos[0] = self.initTerrainPos[0] + self.headPos[0]*2
        moy_pos[2] = self.initTerrainPos[1] + self.headPos[2]*2
        moy_pos[1] += current_worm_size #remonte la tête du ver au dessus du sol

        self.headPos[1] = moy_pos[1]

        self.worm[0] = moy_pos #remplace la position de la tête

        material_rose()
        self.draw_part( self.worm[0], current_worm_size) #dessine la tête
        self.dijkstra_or_aStar_Material()

        #dessine le corps / queue
        for i in range(1, self.worm_len):
            taille = current_worm_size - 0.05
            dir = substract_list( self.worm[i], self.worm[i-1] )
            vec_unit = normalize_vec( dir )
            pos = [ vec_unit[0] * taille, vec_unit[1] * taille, vec_unit[2] * taille ]
            self.draw_part(pos, taille)
            self.worm[i] = [ self.worm[i-1][0] + pos[0], self.worm[i-1][1] + pos[1], self.worm[i-1][2] + pos[2] ]
            current_worm_size = taille

        glPopMatrix()

    def worm_moveX(self, direction):
        """
        Bouge le ver sur l'axe X vers la direction
        normalement sa tête regarde dans la direction de déplacement
        """
        self.headPos[0] += direction * 0.15 #direction * vitesse

    def worm_moveZ(self, direction):
        """
        Bouge le ver sur l'axe Z vers la direction
        normalement sa tête regarde dans la direction de déplacement
        """
        self.headPos[2] += direction * 0.15

    def set_wormX(self, posX):
        self.headPos[0] = posX

    def set_wormZ(self, posZ):
        self.headPos[2] = posZ

    def set_wormPosition(self, posX, posZ):
        self.set_wormX(posX)
        self.set_wormZ(posZ)

    def getWormPosition(self):
        return (self.initTerrainPos[0] + self.headPos[0] * 2, self.headPos[0], self.initTerrainPos[1] + self.headPos[2] * 2)