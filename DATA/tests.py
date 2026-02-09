import numpy as np
from numpy.linalg import norm
import visualizer3d_vbo as vbo
import galaxy_generator as gg
from Class import Body, NBodies
import time
import sys
import os
sys.path.append(os.getcwd())


Liste = [10, 25, 50, 100, 200, 1000]



def generate_galaxies(star_counts, output_dir="galaxies_data"):
    """Generate multiple galaxy data files.

    Args:
        star_counts: The number of stars for each generated galaxy.
        output_dir (sspecifyingtr): Directory where generated files will be written. 

    Returns:
        None
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Dossier '{output_dir}' créé.")
    
    for n_stars in star_counts:
        filename = os.path.join(output_dir, f"galaxy_{n_stars}")
        print(f"\nGeneration: {n_stars} stars -> {filename}")
        gg.generate_galaxy(n_stars=n_stars, output_file=filename)
    
    print(f"\n All files are available in {output_dir}'")



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


def run_headless(ncorps, delta_t, steps=10):
    """Execute the simulation without visualization for benchmarking.

    Args:
        ncorps (NBodies): The simulation object to update.
        delta_t (float): Time step to pass to ncorps.update.
        steps (int): Number of update steps to execute.

    Returns:
        tuple: (elapsed_seconds, fps) where fps is the measured 'frames per second".
    """

    t0 = time.time()
    for _ in range(steps):
        ncorps.update(delta_t)
    elapsed = time.time() - t0
    fps = steps / elapsed if elapsed > 0 else float('inf')
    return elapsed, fps



if __name__ == "__main__":
    output_dir = "galaxies_data"
    generate_galaxies(Liste, output_dir=output_dir)

    
    repeats = 3
    steps = 10
    delta_t = 1

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
        print(f"Average FPS for {n_stars} stars: {avg_fps:.2f}\n")

    print("\n End: The numbers of stars increase the iteration time.")
    

