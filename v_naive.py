import numpy as np
from numpy.linalg import norm
import visualizer3d_vbo as vbo

class Corps() :

    def __init__(self, mass, color, position, velocity):
        self.mass=mass
        self.color=color
        self.position=position
        self.velocity=velocity

    def update(self, delta_t, acceleration):
        new_velocity=self.velocity + delta_t*acceleration
        self.position=self.position + delta_t*self.velocity + 1/2*(delta_t**2)*acceleration
        self.velocity=new_velocity

    def distance(self, other):
        return np.norm(self.position-other.position,2)

gravity_constant= 1.560339E-13

class NCorps():
    
    def __init__(self, list_corps):
        self.list_corps=list_corps

    def gravity(self, idx_caller):
        gravity_vector=np.zeros(3)
        for i,corps in enumerate(list_corps):
            caller=self.list_corps[idx_caller]
            if i==idx_caller:
                pass
            else:
                current=self.list_corps[i]
                dist_vec=current.position-caller.position
                gravity+=caller.mass*current.mass*dist_vec/(norm(dist_vec,2)**3)
        return gravity_constant*gravity



## Tests

data= np.loadtxt('test_v_naive', dtype=np.double)

#print(data)

def generate_star_color(mass):
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
    if mass > 5.0:
        # Étoiles massives: bleu-blanc
        return (150, 180, 255)
    elif mass > 2.0:
        # Étoiles moyennes-massives: blanc
        return (255, 255, 255)
    elif mass > 1.0:
        # Étoiles comme le Soleil: jaune
        return (255, 255, 200)
    else:
        # Étoiles de faible masse: rouge-orange
        return (255, 150, 100)

corps_list=[]
for i in range(data.shape[0]):
        mass=data[i,0]
        color=generate_star_color(mass)
        position=np.array([data[i,1],data[i,2],data[i,3]])
        velocity=np.array([data[i,4],data[i,5],data[i,6]])
        new_corps= Corps(mass,color,position,velocity)
        corps_list.append(new_corps)

ncorps=NCorps(corps_list)

def test(ncorps): 

   
    points = np.zeros((corps_list.shape[0], 3), dtype=np.float32)
   
    # Génération de couleurs aléatoires
    colors = np.array([body.color for body in NCorps.corps_list])
    
    # Génération de luminosités aléatoires
    luminosities = np.zeros(1, corps_list.shape[0]).astype(np.float32)
    
    # Définition des limites de l'espace
    bounds = ((-100, 100), (-100, 100), (-100, 100))
    
    # Création et lancement du visualiseur
    visualizer = Visualizer3D(points, colors, luminosities, bounds)
    visualizer.run()