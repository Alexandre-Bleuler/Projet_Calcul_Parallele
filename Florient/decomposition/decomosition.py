import numpy as np
import galaxy_generator
import visualizer3d_vbo
import time
import numba

#from Bonaventure.Naive.TESTs2 import bounds


# Taille maximale
@numba.njit(parallel = True)
def distance_max(Position):
    dist_xymax = 0

    x_max = 0
    y_max = 0
    z_max = 0


    # Nombre de ligne
    nb_ligne = np.shape(Position)[0]


    for i in numba.prange(1, nb_ligne):

        current=Position[i,:]

        dist_xy = np.linalg.norm(current[:2])
        dist_z = np.abs(current[2:])

        if dist_xy > dist_xymax:
            dist_xymax = dist_xy
            x_max = current[0]
            y_max = current[1]

        if dist_z > z_max:
            z_max = dist_z

    return np.max(x_max, y_max), z_max


_, Position, _, _ = galaxy_generator.generate_galaxy(10)

Y, Z = distance_max(Position)

print("Y_max = ", Y)
print("Z_max = ", Z)

# Création du cube

Cube = bounds((-Y, Y),(-Y, Y), (-Z, Z))




