import numpy as np 
import galaxy_generator
import visualizer3d_vbo
import time

import pylab as plt
import numba
DT = 0.01
G = 1.560339e-13

def compute_acce(positions, masses):
    N = len(masses)
    acc = np.zeros((N, 3), dtype=np.float64)

    for i in range(N):
        
        diff = positions - positions[i]        
        dist_sq = np.sum(diff**2, axis =1) 

        mask = dist_sq < 10E-8
        dist_sq[mask]
        dist_sq[i] = 1.0

        inv_dist3 = 1.0 / (dist_sq * np.sqrt(dist_sq))
        inv_dist3[i] = 0.0
        acc[i] = np.sum(G * masses[:, None] * diff * inv_dist3[:, None], axis=0)
    return acc


@numba.njit(parallel=True)
def compute_acce_numba(positions : np.float64, masses : np.float64)-> np.float64:
    n : numba.int64 = 0
    diff = np.zeros(len(masses), 1)
    acc = np.zeros(len(masses), 3, np.int64)
    for i in numba.prange(acc.shape[0]):
        for k in range(len(positions)):
            diff[k] = positions[k] - positions[i] 
        dist_sq = 0
        for l in range(len(diff)):
            dist_sq += diff[l]**2 
        mask = dist_sq < 10E-8
        dist_sq[mask]
        inv_dist3 = 1.0 / (dist_sq * np.sqrt(dist_sq))
        inv_dist3[i] = 0.0

        #dist_sq = np.sum(diff**2, axis =1)
        for j in range(acc.shape[1]):
            acc[i,j] = 0
            for m in range(j):
                acc[i,j] += G * masses[m] * (positions[m]-positions[i]) * inv_dist3
            for m in range(j,acc.shape[1] ):
                acc[i,j] += G * masses[m] * (positions[m]-positions[i]) * inv_dist3
            break
    return acc



def update():
    global positions, velocities

    start = time.time()
    acc = compute_acce_numba(positions, masses)
    print("Compute time:", time.time() - start)

    positions += velocities*DT + 0.5*acc*DT**2
    velocities +=acc*DT
    return positions.astype(np.float32)

if __name__ == '__main__':
    
    N_ETOILES = 200
    masses, positions, velocities, colors = galaxy_generator.generate_galaxy(n_stars=N_ETOILES)

    masses = np.array(masses, dtype=np.float64)            
    positions = np.array(positions, dtype=np.float64)          
    velocities = np.array(velocities, dtype=np.float64)        
    colors_array = np.array(colors, dtype=np.float32)          
    luminosities = np.ones(len(masses), dtype=np.float32)

    if len(positions) > 0:
        max_coord = np.max(np.abs(positions)) * 2.0
    else:
        max_coord = 10.0

    bounds = [(-max_coord, max_coord),
            (-max_coord, max_coord),
            (-max_coord, max_coord)]
    visualizer = visualizer3d_vbo.Visualizer3D(positions.astype(np.float32),colors_array,luminosities,bounds)
    visualizer.run(updater=lambda dt: update(), dt=DT)