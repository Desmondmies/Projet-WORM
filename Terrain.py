import tkinter as tk
from Matrice import generer_matrice_final as genMatrice, obstacle_matrice, grid_maxValue, grid_minValue, inf_value
from Dijkstra import dijkstra
from A_Star import a_star
from Bezier import bezier_bernstein_4ptsCtrl


class Terrain:
    interface = None

    def __init__(self, interface, w, h, dim, matrice = None):
        self.interface = interface
        self.canv = interface.canv
        self.width = w
        self.height = h
        self.dim_terrain = dim
        self.dimCaseX = w/dim
        self.dimCaseY = h/dim

        self.point_a = None
        self.point_b = None
        self.path_dijkstra = None
        self.path_a_star = None
        self.path_animated = None
        self.left_click_counter = 0

        if matrice is None:
            self.matrice = genMatrice(dim)
        else:
            self.matrice = matrice

        #self.matrice = obstacle_matrice(self.matrice, 2, 5, sizeX=7)
        #self.matrice = obstacle_matrice(self.matrice, 2, 5, sizeY=3)

        #print(self.matrice)
        self.dessiner_terrain()

    """
    Dessine le terrain avec des nuances de gris en s'appuyant sur une matrice de dimension n+2 (n cases + bordures)
    """
    def dessiner_terrain(self):
        for i in range(self.dim_terrain):
            for j in range(self.dim_terrain):
                x = j * self.dimCaseX
                y = i * self.dimCaseY
                if self.matrice[i+1][j+1] == inf_value:
                    self.canv.create_rectangle(x, y, x + self.dimCaseX, y + self.dimCaseY,
                                                fill = self._from_rgb((247, 234, 43)) )
                else:
                    col_val = grid_maxValue - self.matrice[i+1][j+1]
                    couleur = self.remap(col_val, grid_minValue, grid_maxValue, 0, 255)
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
        self.interface.bind("<Control-A>", lambda event : self.animation())
        self.interface.bind("<Control-a>", lambda event : self.animation())
        self.interface.bind("<Control-d>", lambda event : self.animation(True))
        self.interface.bind("<Control-D>", lambda event : self.animation(True))
            

    def getCoordCase(self, event):
        x = int(event.x / (self.width/self.dim_terrain))
        y = int(event.y / (self.height/self.dim_terrain))
        return [x, y]

    def coordCase_coordCanv(self, x, y):
        coordX = x * self.dimCaseX - int(self.dimCaseX/2)
        coordY = y * self.dimCaseY - int(self.dimCaseY/2)
        return [coordX, coordY]

    def left_click(self, event):
        pt_coord = self.getCoordCase(event)
        if self.matrice[pt_coord[1]+1, pt_coord[0]+1] == inf_value: return

        if self.left_click_counter == 0:
            self.point_a = pt_coord
        else:
            self.point_b = pt_coord

        self.left_click_counter = (self.left_click_counter + 1) % 2
        self.update_path()

    def update_path(self):
        if self.point_a is None or self.point_b is None: return
        self.canv.delete("path")
        self.canv.delete("animation")
        self.cherche_path_a_star()
        self.cherche_path_dijkstra()
        self.point_a = None
        self.point_b = None

    """
    Affichage des points de passages des algos A* et Dijkstra
    """
    def draw_oval_point(self, p, color="green", size_offset = 0):
        coord = self.coordCase_coordCanv(p[0], p[1])
        oval_size = int(self.dimCaseX/4) + size_offset
        self.canv.create_oval(coord[0] - oval_size, coord[1] - oval_size, coord[0] + oval_size, coord[1] + oval_size,
                                fill = color,
                                tags = "path")

    def cherche_path_dijkstra(self):
        #Coordonnées de pa et pb en tenant compte de la bordure
        pa = [self.point_a[0] + 1, self.point_a[1] + 1]
        pb = [self.point_b[0] + 1, self.point_b[1] + 1]
        self.path_dijkstra = dijkstra(self.matrice, pa, pb)
        self.tracer_path_dijkstra()

    def tracer_path_dijkstra(self):
        if self.path_dijkstra is None: return
        #print(path)
        for point in self.path_dijkstra:
            self.draw_oval_point(point)

    def cherche_path_a_star(self):
        #Coordonnées de pa et pb en tenant compte de la bordure
        pa = [self.point_a[0] + 1, self.point_a[1] + 1]
        pb = [self.point_b[0] + 1, self.point_b[1] + 1]
        self.path_a_star = a_star(self.matrice, pa, pb)
        self.tracer_path_a_star()

    def tracer_path_a_star(self):
        if self.path_a_star is None: return
        #print(path)
        for point in self.path_a_star:
            self.draw_oval_point(point, color="blue", size_offset=2)
    
    def animation(self, dijkstra = False):
        if self.path_animated is not None : 
            self.canv.delete("animation") #On efface l'ancien chemin dessiné
            self.path_animated = None

        #On regarde quelle animation est lancée
        if dijkstra :
            if self.path_dijkstra is None : return
            self.path_animated = self.path_dijkstra
        else:
            if self.path_a_star is None : return
            self.path_animated = self.path_a_star
        
        n = len(self.path_animated)
        coordCanv_fin = self.coordCase_coordCanv(self.path_animated[n-1][0], self.path_animated[n-1][1]) #Coordonnées du point d'arrivée

        i = 0
        while i < n:
            lst_pts_ctrl = [coordCanv_fin] * 4 #Permet de régler le problème du nombre de pts de controle < 4 : 
                                            #Soit la liste est modifiée dans la boucle d'après
                                            #Soit les points de controlent sont tous à la fin
            j = 0
            while j < 4 and i + j < n: #4 points de controles pour tracer la courbe de Bézier
                coordCanv = self.coordCase_coordCanv(self.path_animated[i + j][0], self.path_animated[i + j][1])
                lst_pts_ctrl[j] = coordCanv
                j += 1
            bezier_bernstein_4ptsCtrl(self, lst_pts_ctrl)
            i += 3 #On incrémente de 3 afin que le dernier point de controle devienne le premier à l'itération suivante
    
        return

    """
    Permet de renouveler la matrice de couts liée au terrain
    """
    def nouveau_terrain(self):
        self.canv.delete("all")
        self.point_a = None #Permet d'éviter de sélectionner 2 points sur des terrains différents
        self.point_b = None
        self.path_dijkstra = None
        self.path_a_star = None
        self.path_animated = None
        self.matrice = genMatrice(self.dim_terrain)
        self.dessiner_terrain()
