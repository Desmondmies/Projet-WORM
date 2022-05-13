# Projet-WORM
###### PROCUREUR Thomas - LAFFAILLE Jason
Projet PyOpenGL de plus court chemin utilisant Dijsktra et A*

*Université de Toulon - Sciences et Technologie 2022 Module Infographie*

Les fichiers exécutables sont le Main_2D.py et Main_3D.py.

Main_2D.py :
    Ce fichier permet de visualiser un terrain 2D avec des nuances de gris que l'on associe à une élévation (coût de passage).
    Le blanc (resp.noir) représente une faible (resp.forte) élévation. 
    Le jaune correspond à des zones infranchissables de coût infini.

    Pour sélectionner un point de départ et un point d'arriver, il suffit d'effectuer un clique gauche sur une case puis un second sur une autre.

    Deux chemins vont apparaître :
        -En vert : Dijkstra
        -En bleu : A*

    Pour lancer une animation (le vers est plus au point sur la version 3D):
        -a : animation du vers sur le chemin A*
        -d : animation du vers sur le chemin Dijkstra

        Envie d'une course de vers ? :
        -c : animation des vers sur les deux chemins


    Raccourcis clavier :
        -Echap : quitter l'application
        -Ctrl + n : permet de générer un nouveau terrain
        -Ctrl + s : permet de sauvegarder les données du terrain, les chemins tracés à l'écran et les coordonnées de béziers pour l'animation du ver (utile pour Main_3D.py)
        -Ctrl + o : permet d'ouvrir un fichier enregistré pour charger les données du terrain et si des chemins ont été dessinés, le système les affiche

Main_3D.py :
    Celui-ci récupère le fichier de sauvegarde "chemins" dans le dossier Saves et modélise un terrain en 3D à partir du contenu.
    Le terrain en 3D est en plusieurs fabriqués en plusieurs "couches" :
        -Quads      => représente les cases de la matrice en plateforme élevé sur l'axe Y
        -Paliers    => représente les jonctions entre chaque Quads, horizontales et verticales
        -Centres    => représente les jonctions entre chaque Paliers
    les couleurs du terrain sont défini selon leur valeur d'élévation
    Les zones infranchissables sont représentés par des trous grisatre dans le terrain
    
    On retrouve en vert le ver de terre effectuant le parcours de Dijkstra et en bleu celui de A*.
    Deux drapeaux représentent respectivement le point de départ et d'arrivée de chacun des vers.

    Raccourcis clavier :
        -Maintenir la barre d'espace : permet d'animer les vers (une fois leur chemin fini il repartiront au point de départ)
        -Flèche Gauche et Droite : tourner la caméra globale à gauche et à droite
        -c : changer le mode de vue de la caméra (passage de caméra globale à caméra embarqué et inversement)
        -a : suivi du ver A* si la caméra est en mode embarqué
        -d : suivi du ver Dijkstra si la caméra est en mode embarqué
    