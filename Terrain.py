import tkinter as tk
import numpy as np
from Matrice import generer_matrice_final as genMatrice, grid_maxValue
from Dijkstra import dijkstra

class Terrain:
    def __init__(self, canvas, w, h, dim, matrice = None):
        self.canv = canvas
        self.width = w
        self.height = h
        self.dim_terrain = dim
        self.dimCaseX = w/dim
        self.dimCaseY = h/dim

        self.point_a = None
        self.point_b = None
        self.left_click_counter = 0

        #tester matrice is None 
        if isinstance(matrice, np.ndarray) :
            self.matrice = matrice
        else:
            self.matrice = genMatrice(dim)

        print(self.matrice)
        self.dessiner_terrain()

    """
    Dessine le terrain avec des nuances de gris en s'appuyant sur une matrice de dimension n+2 (n cases + bordures)
    """
    def dessiner_terrain(self):
        for i in range(self.dim_terrain):
            for j in range(self.dim_terrain):
                x = j * self.dimCaseX
                y = i * self.dimCaseY
                col_val = grid_maxValue - self.matrice[i+1][j+1]
                couleur = self.remap(col_val, 1, 10, 0, 255)
                self.canv.create_rectangle(x, y, x + self.dimCaseX, y + self.dimCaseY,
                                      fill = self._from_rgb((couleur, couleur, couleur)),
                                      activefill = "red")

    """
    Permet de redéfinir un intervale entre deux nouvelles bornes
    """
    def remap(self, valeur, min1, max1, min2, max2):
        return int(min2 + (valeur - min1) * (max2 - min2) / (max1 - min1))

    """
    Conversion d'un tuple rgb en gormat hexadécimal
    """
    def _from_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb

    def bind_terrain(self):
        self.canv.bind("<Button-1>", self.left_click)

    """
    Renvoie le numéro de la case en x et en y.
    """
    def getCoordCase(self, event):
        x = int(event.x / (self.width/self.dim_terrain))
        y = int(event.y / (self.height/self.dim_terrain))
        return [x, y]

    def left_click(self, event):
        self.left_click_counter = (self.left_click_counter + 1) % 2
        if self.left_click_counter == 0:
            self.point_a = self.getCoordCase(event)
        elif self.left_click_counter == 1:
            self.point_b = self.getCoordCase(event)
        self.update_path()
    
    def update_path(self):
        if self.point_a is None or self.point_b is None: return
        self.draw_path()
        self.point_a = None
        self.point_b = None

    def draw_oval_point(self, p, color="green"):
        x_a = (p[0]-1) * self.dimCaseX + int(self.dimCaseX/2)
        y_a = (p[1]-1) * self.dimCaseY + int(self.dimCaseY/2)
        oval_size = 5
        self.canv.create_oval(x_a - oval_size, y_a - oval_size, x_a + oval_size, y_a + oval_size,
                                fill = color,
                                tags = "path")

    def draw_path(self):
        self.canv.delete("path")
        #Coordonnées de pa et pb en tenant compte de la bordure
        pa = [self.point_a[0] + 1, self.point_a[1] + 1]
        pb = [self.point_b[0] + 1, self.point_b[1] + 1]
        path = dijkstra(self.matrice, pa, pb)
        
        #print(path)
        
        for point in path:
            self.draw_oval_point(point)
        
    def nouveau_terrain(self):
        self.canv.delete("all")
        self.matrice = genMatrice(self.dim_terrain)
        self.dessiner_terrain()
        

