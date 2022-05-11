import time
from Worm2D import Worm2D
from Utils import horner

"""
Polynomes bernstein pour 4 points de controles.
"""
def B3p():
    B30 = [-1, 3, -3, 1]
    B31 = [3, -6, 3, 0]
    B32 = [-3, 3, 0, 0]
    B33 = [1, 0, 0, 0]
    return [B30, B31, B32, B33]

def bezier_bernstein_4ptsCtrl(ptsControle, worm, nbPtsInterpolation = 50):
    chemin = []
    polynomes = B3p()
    pas = 1/(nbPtsInterpolation + 1)
    u = pas
    while u < 1:
        listePts = []
        for i in range(len(ptsControle)):
            Mi = ptsControle[i]
            Bni = horner(u, polynomes[i])
            x = Mi[0] * Bni
            y = Mi[1] * Bni
            listePts.append([x, y])

        M = [0, 0]
        for pts in listePts:
            M[0] += pts[0]
            M[1] += pts[1]

        chemin.append(M)
        u += pas
    return chemin
