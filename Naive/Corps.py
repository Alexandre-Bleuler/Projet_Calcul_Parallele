

G = 1.560339 * 10**(-13)


class corps:
    def __init__(self, masse, position, vitesse, couleur):
        self.masse = masse
        self.couleur = couleur
        self.position = position
        self.vitesse = vitesse


    def position_vitesse_update(self, position, vitesse, acceleration, delta_t):
        new_vitesse = vitesse + acceleration * delta_t
        new_position = position + delta_t * vitesse + (delta_t**2) * acceleration / 2

        return new_position, new_vitesse