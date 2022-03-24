def get_vertex(i, j):
    v = [ 2*i, 0, 2*j,
          2*i+1, 0, 2*j+1, 
          2*i, 0, 2*j+1,
          2*i, 0, 2*j,
          2*i+1, 0, 2*j,
          2*i+1, 0, 2*j+1]
    return v

def gen_terrain_vertex(matrice):
    n = len(matrice)
    vertex = []

    for i in range(n):
        for j in range(n):
            vertex += get_vertex(i, j)


    return vertex
