import os
import sys
import random
import shutil
import numpy as np
from src.image_utils import load_image_as_array, reconstruct_image_from_array, save_centroids
from src.parallel_kmeans import run_parallel_map_reduce
from src.math_utils import manhattan_distance

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(PROJECT_ROOT, 'dataset')
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

INPUT_IMAGE = os.path.join(DATASET_DIR, 'source_image.jpg')
CENTROIDS_FILE = os.path.join(DATASET_DIR, 'initial_centroids.txt')
OUTPUT_IMAGE = os.path.join(DATASET_DIR, 'output_images', 'result.jpg')

K = 5  # Number of clusters
MAX_ITER = 10
THRESHOLD = 1.0  # Convergence threshold

def initialize_centroids(pixels, k, output_file):
    print("Initializing centroids...")
    # Randomly sample k pixels
    indices = np.random.choice(len(pixels), k, replace=False)
    centroids = pixels[indices].astype(float)
    
    save_centroids(centroids, output_file)
    print(f"Initialized {k} centroids.")
    return centroids

def main():
    # 1. Preprocessing
    if not os.path.exists(INPUT_IMAGE):
        print(f"Error: {INPUT_IMAGE} not found. Please place an image there.")
        return

    print("Step 1: Loading image...")
    # Load image directly into memory as numpy array
    pixels, width, height = load_image_as_array(INPUT_IMAGE)
    
    # 2. Initialization
    print("Step 2: Initializing centroids...")
    current_centroids = initialize_centroids(pixels, K, CENTROIDS_FILE)
    
    # 3. Iteration
    print("Step 3: Starting Parallel K-means iteration...")
    iteration = 0
    while iteration < MAX_ITER:
        print(f"--- Iteration {iteration + 1} ---")
        
        # Run Parallel MapReduce (In-Memory)
        new_centroids = run_parallel_map_reduce(pixels, current_centroids)
        
        # Calculate shift
        max_shift = 0.0
        for i in range(K):
            shift = manhattan_distance(new_centroids[i], current_centroids[i])
            if shift > max_shift:
                max_shift = shift
        
        print(f"Max shift: {max_shift}")
        
        # Update centroids
        current_centroids = new_centroids
        save_centroids(current_centroids, CENTROIDS_FILE)
        
        if max_shift < THRESHOLD:
            print("Converged!")
            break
            
        iteration += 1
    
    # 4. Post-processing
    print("Step 4: Reconstructing image...")
    reconstruct_image_from_array(pixels, current_centroids, width, height, OUTPUT_IMAGE)
    print("Done!")

if __name__ == '__main__':
    main()
