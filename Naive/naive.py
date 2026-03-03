import numpy as np
import sdl2
import sdl2.ext
from OpenGL.GL import *
from OpenGL.GLU import *
import ctypes
import visual
from visual import Visualizer3D


import NCorps
from NCorps import Ncorps
import Corps
from Corps import corps


# Pas de temps Fixé
#delta_t = 0.001 * 3.15576e7
delta_t = 1
#delta_t = 1e2
#delta_t = 1e4

# Transformation de données  text en liste de vecteur

collection = np.loadtxt("etoile")
print(len(collection))

# Recharge de la collection de Corps
systeme = Ncorps(collection)

N = systeme.shape()

# Fonction pour mettre à jour le système, la fonction retourne les nouvelles positions

def system_update(systeme, dt):


    # Calcul des accélérations
    A = np.zeros((N, 3))
    for i in range(N):
        A[i] = systeme.acceleration(i)

    # Mis à jour de la position et de la vitesse de chaque coprs

    for i in range(N):

        #Extraire l'état actuel
        masse = systeme.collection_corps[i, 0]
        position = systeme.collection_corps[i, 1:4]
        vitesse = systeme.collection_corps[i, 4:7]

        # Création d'un objet temporaire pour utiliser les méthodes
        star = corps(masse, position.copy(), vitesse.copy(), couleur=(255, 255, 255))

        # Calcul de la nouvelle position et vitesse
        new_position, new_vitesse = star.position_vitesse_update(star.position, star.vitesse, A[i], dt)

        # Mis à jour du système principal
        systeme.collection_corps[i, 1:4] = new_position
        systeme.collection_corps[i, 4:7] = new_vitesse

        #print(new_position)


    return  systeme.collection_corps[:, 1:4].copy()


points = systeme.collection_corps[:, 1:4]


colors = np.array([systeme.star_color(star[0]) for star in systeme.collection_corps])

luminosities = np.ones(systeme.shape())


bounds = (
    (points[:,0].min(), points[:,0].max()),
    (points[:,1].min(), points[:,1].max()),
    (points[:,2].min(), points[:,2].max())
)

visualizer = Visualizer3D(points, colors, luminosities, bounds)

visualizer.run(updater=lambda dt: system_update(systeme, dt), dt=delta_t)




