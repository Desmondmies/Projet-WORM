import tkinter as tk
from Matrice import generer_matrice_final as genMatrice
from Dijkstra import dijkstra

class Grille:
    def __init__(self, canvas, w, h, n):
        self.canv = canvas
        self.width = w
        self.height = h
        self.nbCase = n
        self.dimCaseX = self.width/self.nbCase
        self.dimCaseY = self.height/self.nbCase

        self.point_a = None
        self.point_b = None

        self.matrice = genMatrice(nbCase)
        self.dessiner_terrain()

    """
    Dessine le terrain avec des nuances de gris en s'appuyant sur une matrice dimension n+2 (n cases + les bordures)
    """
    def dessiner_terrain(self):
        for i in range(self.nbCase):
            for j in range(self.nbCase):
                x = j * self.dimCaseX
                y = i * self.dimCaseY
                couleur = self.remap(self.matrice[i + 1][j + 1], 1, 10, 0, 255)
                self.canv.create_rectangle(x, y, x + self.dimCaseX, y + self.dimCaseY,
                                      fill = self._from_rgb((couleur, couleur, couleur)),
                                      activefill = "red")

    """
    Permet de
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

    def getNumCase(self, event):
        x = int(event.x / (width/nbCase))
        y = int(event.y / (height/nbCase))
        return [x, y]

    def left_click(self, event):
        #select point A
        self.select_point(event)
    
    def select_point(self, event):
        if self.point_a is None:
            self.point_a = self.getNumCase(event)
        else:
            self.point_b = self.getNumCase(event)

        if self.point_a is not None and self.point_b is not None:
            self.draw_path()
            self.point_a = None
            self.point_b = None

    def draw_oval_point(self, p, color="green"):
        x_a = (p[0]-1) * self.dimCaseX + int(self.dimCaseX/2)
        y_a = (p[1]-1) * self.dimCaseY + int(self.dimCaseY/2)
        self.canv.create_oval(x_a - 5, y_a - 5, x_a + 5, y_a + 5,
                                fill = color,
                                tags = "path")

    def draw_path(self):
        self.canv.delete("path")
        pa = [self.point_a[0] + 1, self.point_a[1] + 1]
        pb = [self.point_b[0] + 1, self.point_b[1] + 1]
        path = dijkstra(self.matrice, pa, pb)
        #self.draw_oval_point(pointA)
        #self.draw_oval_point(pointB)

        for point in path:
            self.draw_oval_point(point)
        

if __name__ == "__main__":
    width = 500
    height = 500
    nbCase = 30
    root = tk.Tk()
    root.geometry(str(width) + "x" + str(height) + "+0+0")
    canv = tk.Canvas()

    #nbCase : nombre de cases sur une ligne et une colonne
    terrain = Grille(canv, width, height, nbCase)
    terrain.bind_terrain()

    print("test git")
    canv.pack(expand = True, fill = "both")
    root.mainloop()
