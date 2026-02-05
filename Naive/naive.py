import numpy as np
import sdl2
import sdl2.ext
from OpenGL.GL import *
from OpenGL.GLU import *
import ctypes

import numpy as np
import NCorps
from NCorps import Ncorps
import Corps
from Corps import corps


# Pas de temps Fixé
delta_t = 0.001 * 3.15576e7

# Transformation de données  text en liste de vecteur

collection = np.loadtxt("etoile")
print(len(collection))
# print(collection)

# Recharge de la collection de Corps
systeme = Ncorps(collection)

N = systeme.shape()
print(N)


# Calcul de l'accélération des corps
A = np.zeros((N, 3))

for i in range(N):
    Acceleration = systeme.acceleration(i)
    A [i] = Acceleration

print(A)


# Mis à jour de la position et de la vitesse de chaque coprs

for i in range(N):
    Etoile = systeme.etoile(i)
    # État de depart

    couleur = systeme.star_color(Etoile[0])  # Couleur de l'étoile

    star = corps(Etoile[0], Etoile[1:4], Etoile[4:7], couleur)
    print(star)
    print("Position : ", star.position)
    print("Vitesse : ", star.vitesse)

    # Mis à jour
    Acceleration = systeme.acceleration(i)
    n_star = star.position_vitesse_update(star.position, star.vitesse, Acceleration, delta_t)

    # Nouvel État

    print("Nouvelle Position : ", n_star[0])
    print("Nouvelle Vitesse : ", n_star[1])

