
import numpy as np
import sdl2
import sdl2.ext
from OpenGL.GL import *
from OpenGL.GLU import *
import ctypes

G = 1.560339 * 10**(-13)


class corps:
    def __init__(self, masse, position, vitesse, couleur):
        self.masse = masse
        self.couleur = couleur
        self.position = position
        self.vitesse = vitesse


    def position_vitesse_update(self, position, vitesse, acceleration, delta_t):
        self.vitesse = vitesse + acceleration * delta_t
        self.position = position + delta_t * vitesse + (delta_t**2) * acceleration / 2

        return position, vitesse

"""
    def star_color(self, masse):
    
        Génère une couleur pour une étoile en fonction de sa masse.
        Les étoiles massives sont bleues, les moyennes sont jaunes, les petites sont rouges.

        Parameters:
        -----------
        mass : float
            Masse de l'étoile en masses solaires

        Returns:
        --------
        color : tuple
            Couleur RGB (R, G, B) avec des valeurs entre 0 et 255
    
        if masse > 5.0:
            # Étoiles massives: bleu-blanc
            return (150, 180, 255)
        elif masse > 2.0:
            # Étoiles moyennes-massives: blanc
            return (255, 255, 255)
        elif masse > 1.0:
            # Étoiles comme le Soleil: jaune
            return (255, 255, 200)
        else:
            # Étoiles de faible masse: rouge-orange
            return (255, 150, 100)


"""


