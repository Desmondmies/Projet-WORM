import tkinter as tk
from Terrain import Terrain
from Menubar import Menubar

class Interface:
    def __init__(self, width = 500, height = 500):
        self.width = width
        self.height = height

        self.root = tk.Tk()
        self.root.geometry(str(width) + "x" + str(height) + "+0+0")
        self.root.resizable(False, False)

        self.canv = tk.Canvas(self.root)

    def creer_menubar(self):
        self.menubar = Menubar(self)
        self.menubar.afficher()

    def creer_terrain(self, dim_terrain):
        self.terrain = Terrain(self, self.width, self.height, dim_terrain)
        self.terrain.bind_terrain()

    def charger_terrain(self, matrice):
        self.canv.delete("all")
        self.terrain = Terrain(self, self.width, self.height, len(matrice) - 2, matrice)
        self.terrain.bind_terrain() #Nécessaire sinon on manipule toujours l'ancienne matrice

    def afficher(self):
        self.terrain.dessiner_terrain()
        self.canv.pack(expand = True, fill = "both")

    def bind(self, action, fct):
        self.root.bind(action, fct)

    def unbind(self, action, fct = None):
        if fct == None:
            self.root.unbind(action)
        else:
            self.root.unbind(action, fct)

    def boucle_principale(self):
        self.root.mainloop()

if __name__ == "__main__":
    interface = Interface()

    interface.creer_menubar()
    interface.creer_terrain(30)

    interface.afficher()

    interface.root.mainloop()
