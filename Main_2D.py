from _2D.Interface import Interface

if __name__ == "__main__":
    interface = Interface()

    interface.creer_terrain(20)
    interface.creer_menubar()
    
    interface.afficher()

    interface.root.mainloop()