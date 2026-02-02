import numpy as np
from numpy.linalg import norm

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

