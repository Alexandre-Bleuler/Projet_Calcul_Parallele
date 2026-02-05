import numpy as np
import Corps


G = 1.560339 * 10**(-13)

class Ncorps:
    def __init__(self, collection_corps):
        self.collection_corps = collection_corps


    def shape(self):
        return len(self.collection_corps)

    def etoile(self, index):

        return self.collection_corps[index]

    def star_color(self, masse):
        """
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
        """
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

    def acceleration(self, i):
        n = len(self.collection_corps)

        ci = self.collection_corps[i]
        Mi = ci[0]
        Pi = ci[1:4]

        a = np.zeros(3)

        for j in range(n):
            if j != i:
                cj = self.collection_corps[j]
                Mj = cj[0]
                Pj = cj[1:4]
                a += G * (Mi * Mj) * (Pj - Pi) / (np.linalg.norm(Pj - Pi)**3)

        a /= Mi

        return a







