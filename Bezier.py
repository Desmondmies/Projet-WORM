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

#ATTENTION voir pour éviter de toujourz passer le terrain en arg
def bezier_bernstein_4ptsCtrl(terrain, ptsControle, nbPtsInterpolation = 100):
    polynomes = B3p()
    pas = 1/(nbPtsInterpolation + 1)
    print("ctrl : ", ptsControle)
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

        oval_size = 5
        terrain.canv.create_oval(M[0] - 5, M[1] - 5, M[0] + 5, M[1] + 5,
                                fill = "black",
                                tags = "animation")
        
        u += pas
    return
