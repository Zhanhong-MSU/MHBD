import os
import sys
import random
import shutil
from src.image_utils import image_to_pixels, reconstruct_image, save_centroids, load_centroids
from src.mr_kmeans import MRKMeans
from src.math_utils import manhattan_distance

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(PROJECT_ROOT, 'dataset')
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

INPUT_IMAGE = os.path.join(DATASET_DIR, 'source_image.jpg')
PIXELS_FILE = os.path.join(DATASET_DIR, 'pixels_input.txt')
CENTROIDS_FILE = os.path.join(DATASET_DIR, 'initial_centroids.txt')
OUTPUT_IMAGE = os.path.join(DATASET_DIR, 'output_images', 'result.jpg')

K = 5  # Number of clusters
MAX_ITER = 10
THRESHOLD = 1.0  # Convergence threshold

def initialize_centroids(pixels_file, k, output_file):
    print("Initializing centroids...")
    # Read all pixels (this might be large, but for this assignment it's okay)
    # For very large files, we should reservoir sample.
    pixels = []
    with open(pixels_file, 'r') as f:
        for line in f:
            parts = list(map(int, line.strip().split(',')))
            pixels.append(parts[2:]) # [R, G, B]
    
    centroids = random.sample(pixels, k)
    save_centroids(centroids, output_file)
    print(f"Initialized {k} centroids.")
    return centroids

def run_mr_job(pixels_file, centroids_file):
    # Run the MRJob
    # We need to pass the centroids file
    args = [pixels_file, '--centroids-file', centroids_file]
    
    # Create the job instance
    job = MRKMeans(args=args)
    
    new_centroids_dict = {}
    
    with job.make_runner() as runner:
        runner.run()
        # Parse output
        for key, value in job.parse_output(runner.cat_output()):
            # key is centroid index, value is [R, G, B]
            new_centroids_dict[key] = value
            
    # Convert dict to list, ensuring order matches indices if possible, 
    # but K-means just needs a set of centroids. 
    # However, our mapper uses index. So we should keep them in order of index.
    # But wait, if a cluster becomes empty, it won't be in the output.
    # We need to handle empty clusters (maybe keep old centroid).
    
    return new_centroids_dict

def main():
    # 1. Preprocessing
    if not os.path.exists(INPUT_IMAGE):
        print(f"Error: {INPUT_IMAGE} not found. Please place an image there.")
        return

    print("Step 1: Converting image to text...")
    width, height = image_to_pixels(INPUT_IMAGE, PIXELS_FILE)
    
    # 2. Initialization
    print("Step 2: Initializing centroids...")
    current_centroids = initialize_centroids(PIXELS_FILE, K, CENTROIDS_FILE)
    
    # 3. Iteration
    print("Step 3: Starting K-means iteration...")
    iteration = 0
    while iteration < MAX_ITER:
        print(f"--- Iteration {iteration + 1} ---")
        
        # Run MapReduce Job
        new_centroids_map = run_mr_job(PIXELS_FILE, CENTROIDS_FILE)
        
        # Construct new centroids list
        new_centroids = []
        max_shift = 0.0
        
        for i in range(K):
            if i in new_centroids_map:
                new_c = new_centroids_map[i]
                old_c = current_centroids[i]
                shift = manhattan_distance(new_c, old_c)
                if shift > max_shift:
                    max_shift = shift
                new_centroids.append(new_c)
            else:
                # Cluster disappeared, keep old centroid or re-init
                # For simplicity, keep old
                print(f"Warning: Cluster {i} is empty. Keeping old centroid.")
                new_centroids.append(current_centroids[i])
        
        print(f"Max shift: {max_shift}")
        
        # Update centroids file
        save_centroids(new_centroids, CENTROIDS_FILE)
        current_centroids = new_centroids
        
        if max_shift < THRESHOLD:
            print("Converged!")
            break
            
        iteration += 1
    
    # 4. Post-processing
    print("Step 4: Reconstructing image...")
    # Ensure output directory exists
    output_dir = os.path.dirname(OUTPUT_IMAGE)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    reconstruct_image(PIXELS_FILE, current_centroids, width, height, OUTPUT_IMAGE)
    print("Done!")

if __name__ == '__main__':
    main()
