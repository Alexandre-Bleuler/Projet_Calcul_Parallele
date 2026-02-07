import numpy as np
from numpy.linalg import norm
import visualizer3d_vbo as vbo

gravity_constant= 1.560339E-13

class Corps() :

    def __init__(self, mass, color, position, velocity):
        self.mass=mass
        self.color=color
        self.position=position
        self.velocity=velocity

    def update(self, delta_t, acceleration):
        self.position=self.position + delta_t*self.velocity + 1/2*(delta_t**2)*acceleration
        self.velocity=self.velocity + delta_t*acceleration

    def distance(self, other):
        return np.norm(self.position-other.position,2)

class NCorps():
    
    def __init__(self, bodies_list):
        self. bodies_list= bodies_list

    def gravity(self, idx_caller):
        gravity=np.zeros(3)
        for i in range(len(self. bodies_list)):
            caller=self. bodies_list[idx_caller]
            if i==idx_caller:
                pass
            else:
                current=self. bodies_list[i]
                dist_vec=current.position-caller.position
                gravity+=caller.mass*current.mass*dist_vec/(norm(dist_vec,2)**3)
        return gravity_constant*gravity

    def get_points(self):
        bodies_list=self.bodies_list
        number_of_body=len(bodies_list)
        
        points=np.zeros((number_of_body,3))
        for i,body in enumerate(bodies_list):
            points[i,:] = body.position
        return points

    def update(self, delta_t) :
        acceleration=np.zeros((len(self.bodies_list),3))
        for i,body in enumerate(self.bodies_list):
            acceleration[i,:]=self.gravity(i)/body.mass
        for i,body in enumerate(self.bodies_list):
            body.update(delta_t,acceleration[i,:])
        return self.get_points()


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
        return ([150, 180, 255])
    elif mass > 2.0:
        # Étoiles moyennes-massives: blanc
        return ([255, 255, 255])
    elif mass > 1.0:
        # Étoiles comme le Soleil: jaune
        return ([255, 255, 200])
    else:
        # Étoiles de faible masse: rouge-orange
        return ([255, 150, 100])

bodies_list=[]
for i in range(data.shape[0]):
        mass=data[i,0]
        color=generate_star_color(mass)
        position=np.array([data[i,1],data[i,2],data[i,3]])
        velocity=np.array([data[i,4],data[i,5],data[i,6]])
        new_corps= Corps(mass,color,position,velocity)
        bodies_list.append(new_corps)

ncorps=NCorps(bodies_list)

delta_t=1

def test(ncorps, delta_t): 

    bodies_list=ncorps.bodies_list
    number_of_body=len(bodies_list)
    
    points=np.zeros((number_of_body,3))
    for i,body in enumerate(bodies_list):
        points[i,:] = body.position
   
    # Génération de couleurs aléatoires
    colors = np.array([body.color for body in bodies_list])
    
    # Génération de luminosités aléatoires
    luminosities = np.ones(number_of_body).astype(np.float32)
    
    # Définition des limites de l'espace
    bounds = ((-100, 100), (-100, 100), (-100, 100))
    
    # Création et lancement du visualiseur

    visualizer = vbo.Visualizer3D(points, colors, luminosities, bounds)
    visualizer.run(ncorps.update, delta_t)

test(ncorps, delta_t)