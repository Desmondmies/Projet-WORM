import tkinter as tk
import numpy as np

import sys
if(sys.version_info >= (3,)):
    from tkinter import messagebox
    from tkinter import filedialog
else:
    import tkMessageBox as messagebox
    import tkFileDialog as filedialog

class Menubar:
    interface = None

    def __init__(self, interface):
        Menubar.interface = interface
        self.menubar = tk.Menu(interface.root)

        self.fichier = tk.Menu(self.menubar, tearoff = 0)

        self.menubar_set_fichier(self.fichier)

        self.menubar.add_cascade(label = "Fichier", menu = self.fichier)

    def menubar_set_fichier(self, fichier):
        fichier.add_command(label = "Nouveau", command = self.nouveau)
        fichier.add_command(label = "Ouvrir", command = self.ouvrir)
        fichier.add_command(label = "Enregistrer sous...", command = self.enregistrer)#, state = "disabled")
        fichier.add_command(label = "Quitter", command = self.quitter)

        Menubar.interface.bind('<Control-n>', Menubar.nouveau)
        Menubar.interface.bind('<Control-N>', Menubar.nouveau)
        Menubar.interface.bind('<Control-o>', Menubar.ouvrir)
        Menubar.interface.bind('<Control-O>', Menubar.ouvrir)
        Menubar.interface.bind('<Control-s>', Menubar.enregistrer)
        Menubar.interface.bind('<Control-S>', Menubar.enregistrer)
        Menubar.interface.bind('<Escape>', Menubar.quitter)

    def afficher(self):
        Menubar.interface.root.config(menu = self.menubar)
            

    @staticmethod
    def nouveau(evt = None):
        Menubar.interface.terrain.nouveau_terrain()

    """
    Attention, ne prend pas en compte les différentes valeurs de couts possibles
    entre la matrice sauvée et celle en cours.
    """
    @staticmethod
    def ouvrir(evt = None):
        path = filedialog.askopenfilename(initialdir = "./Saves/", 
                                            title = "Ouvrir", 
                                            filetypes = (("Fichier texte","*.txt"), ))
        if path == '': return False

        fichier = open(path, 'r')
        dico = eval(fichier.read())
        matrice = np.array(dico["matrice"])
        Menubar.interface.charger_terrain(matrice)

        path_a_star = dico["path_a_star"]
        path_dijkstra = dico["path_dijkstra"]

        if(path_a_star is not None):
            Menubar.interface.terrain.path_a_star = path_a_star
            Menubar.interface.terrain.tracer_path_a_star()

        if(path_dijkstra is not None):
            Menubar.interface.terrain.path_dijkstra = path_dijkstra
            Menubar.interface.terrain.tracer_path_dijkstra()


        fichier.close()

        return True

    """
    L'enregistrement d'un terrain se fait par l'écriture d'un dictionnaire dans un fichier texte
    que l'on va ensuite récupérer et exploiter grâce à la fonction "eval()" de python.
    """
    @staticmethod
    def enregistrer(evt = None):
        path = filedialog.asksaveasfilename(initialdir = "./Saves/", 
                                            title = "Enregistrer", 
                                            filetypes = (("Fichier texte","*.txt"), ),
                                            defaultextension = ".txt")
        if path == "": 
            return False

        fichier = open(path, 'w')
        dico = {"matrice" : Menubar.interface.terrain.matrice.tolist(), 
                "path_dijkstra" : Menubar.interface.terrain.path_dijkstra, 
                "path_a_star" : Menubar.interface.terrain.path_a_star}

        fichier.write(str(dico))

        fichier.close()
        return True

    @staticmethod
    def quitter(evt = None):
        reponse = messagebox.askyesno(title = 'Quitter', 
                                      message = 'Voulez-vous quitter ?')
        if(reponse):
            exit(1)