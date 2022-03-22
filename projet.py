import tkinter as tk
from Matrice import generer_matrice_final as genMatrice

class Grille:
    def __init__(self, canvas, w, h, n):
        self.canv = canvas
        self.width = w
        self.height = h
        self.nbCase = n
        self.dimCaseX = self.width/self.nbCase
        self.dimCaseY = self.height/self.nbCase

        self.matrice = genMatrice(nbCase)
        self.dessiner_terrain()
        return

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
        return

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
        self.canv.bind("<Button-1>", self.getNumCase)
        return

    def getNumCase(self, event):
        print(int(event.x / (width/nbCase)), int(event.y / (height/nbCase)))
        return

if __name__ == "__main__":
    width = 900
    height = 900
    nbCase = 30
    root = tk.Tk()
    root.geometry(str(width) + "x" + str(height) + "+0+0")
    canv = tk.Canvas()

    #nbCase : nombre de cases sur une ligne et une colonne
    terrain = Grille(canv, width, height, nbCase)
    terrain.bind_terrain()

    canv.pack(expand = True, fill = "both")
    root.mainloop()
