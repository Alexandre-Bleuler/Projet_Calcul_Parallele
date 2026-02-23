import sys
import os
sys.path.append(os.getcwd())

import time
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt

import visualizer3d_vbo_stats as vbos
import galaxy_generator as gg


method_name = sys.argv[1]

# For exemple :
# output_name="Bonaventure_Naive"


import Bonaventure.Naive.naive as bon_naive

def test(ncorps, delta_t): 
    """Run the visualizer on an NBodies instance.

    
    Args:
        ncorps: Instance containing the bodies to visualize.
        delta_t: Time step passed to the visualizer's update callback.

    Returns:
        None
    """

    bodies_list=ncorps.bodies_list
    number_of_body=len(bodies_list)
    
    points=np.zeros((number_of_body,3))
    for i,body in enumerate(bodies_list):
        points[i,:] = body.position
   
    colors = np.array([body.color for body in bodies_list])
    
    luminosities = np.ones(number_of_body).astype(np.float32)
    
    bounds = ((-100, 100), (-100, 100), (-100, 100))
    
    
    visualizer = vbo.Visualizer3D(points, colors, luminosities, bounds)
    visualizer.run(ncorps.update, delta_t)


def run_with_stats(update_func, delta_t, steps=10):
    """Execute the simulation without visualization for benchmarking.

    Args:
        update_func (function): The function that update the system.
        delta_t (float): Time step to pass to ncorps.update.
        steps (int): Represents the number of iterations that the simulation performs during the test phase

    Returns:
        tuple: (elapsed_seconds, fps) where fps is the measured 'frames per second".
    """

    t0 = time.time()
    for _ in range(steps):
        update_func(delta_t)
    elapsed = time.time() - t0
    fps = steps / elapsed if elapsed > 0 else float('inf')
    return elapsed, fps

def get_data_file_names(max_number_of_bodies=1000):
    """
    A function that get the file name in DATA/galaxies_data

    Args :
    max_number_of_bodies : The maximum number of bodies considered 
    compatible with files of DATA/galaxies_data

    Return : 

    The list of the file names in increasing order of the number of bodies 
    """
    name_list=[]
    current_name=""
    for i in range(1,max_number_of_bodies+1):
        name_list.append=f"galaxy_{i*50}"
    return name_list

def test_stats(update_func, delta_t, data_file_name): 
    """
    A function to test the naive N-bodies simulation 
    
    Args:
        ncorps: the NBody object containing the bodies to be studied
        delta_t: the time step of the study

    Return: 
        The average time used to update the system. 
    """

    data= np.loadtxt(data_file_name, dtype=np.double)
    for i in range(data.shape[0]):
        mass=data[i,0]
        color=gg.generate_star_color(mass)
        position=np.array([data[i,1],data[i,2],data[i,3]])
        velocity=np.array([data[i,4],data[i,5],data[i,6]])

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

    visualizer = vbos.Visualizer3D(points, colors, luminosities, bounds)
    average_time=visualizer.run(update_func, delta_t)
    return average_time


if __name__ == "__main__":
    
    max_number_of_bodies=1000
    number_of_bodies=np.arange(50,max_number_of_bodies+50,50)
    data_file_names=get_data_file_names(max_number_of_bodies)
    average_stats=np.array(number_of_bodies,3)
    average_stats[:,0]=number_of_bodies
    
    for i,name in enumerate(data_file_names):

    
    
    """plt.figure()
    plt.plot(stars_list, avg_fps_list)
    plt.xlabel("Nombre d'étoiles")
    plt.ylabel("FPS moyen")
    plt.title("Evolution des perfomances")
    plt.show()"""



### OLD main
 """repeats = 3 # number of times a series of tests will be repeated
    steps = 10 # represents the number of iterations that the simulation performs during the test phase
    delta_t = 0.1
    stars_list = []
    avg_fps_list = []


    print("\nStarting")
    for n_stars in Liste:
        file_path = os.path.join(output_dir, f"galaxy_{n_stars}")
        if not os.path.exists(file_path):
            print(f"File not find: {file_path}")
            continue
        print(f"\n== {n_stars} stars: {file_path} ==")
        fps_list = []
        for r in range(1, repeats + 1):
            ncorps = NBodies(file_path)
            elapsed, fps = run_headless(ncorps, delta_t, steps=steps)
            fps_list.append(fps)
            print(f"Run {r}/{repeats}: {steps} steps -> {elapsed:.4f} s, {fps:.2f} FPS")
        avg_fps = sum(fps_list) / len(fps_list) if fps_list else 0.0
        stars_list.append(n_stars)
        avg_fps_list.append(avg_fps)
        print(f"Average FPS for {n_stars} stars: {avg_fps:.2f}\n")

    print("\n End: The numbers of stars increase the iteration time.")"""