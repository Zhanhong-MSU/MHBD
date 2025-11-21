import numpy as np
import multiprocessing
from src.math_utils import manhattan_distance

def map_task(args):
    """
    Mapper task for a chunk of pixels.
    Args:
        args: tuple containing (pixels_chunk, centroids)
    Returns:
        dict: {centroid_idx: {'sum': np.array([r,g,b]), 'count': int}}
    """
    pixels_chunk, centroids = args
    partial_results = {}
    
    # Pre-initialize dictionary for all k centroids
    for i in range(len(centroids)):
        partial_results[i] = {'sum': np.zeros(3, dtype=np.float64), 'count': 0}

    # Iterate over pixels in this chunk
    for pixel in pixels_chunk:
        # Find nearest centroid (Manhattan distance)
        # Optimization: Vectorized calculation is faster, but let's stick to the logic
        # of checking each centroid to simulate the "Map" process clearly.
        
        min_dist = float('inf')
        nearest_idx = -1
        
        # Calculate distances to all centroids
        # Using numpy broadcasting for speed within the chunk would be faster,
        # but here we iterate to be explicit about the distance metric.
        for idx, centroid in enumerate(centroids):
            # Manual Manhattan distance: sum(|p - c|)
            dist = np.sum(np.abs(pixel - centroid))
            if dist < min_dist:
                min_dist = dist
                nearest_idx = idx
        
        # Accumulate
        if nearest_idx != -1:
            partial_results[nearest_idx]['sum'] += pixel
            partial_results[nearest_idx]['count'] += 1
            
    return partial_results

def run_parallel_map_reduce(pixels, centroids, num_processes=None):
    """
    Driver for the Parallel MapReduce K-means.
    """
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
        
    # 1. Split data (Split phase)
    chunk_size = len(pixels) // num_processes
    chunks = []
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else len(pixels)
        chunks.append((pixels[start:end], centroids))
        
    # 2. Map phase (Parallel execution)
    with multiprocessing.Pool(processes=num_processes) as pool:
        map_results = pool.map(map_task, chunks)
        
    # 3. Reduce phase (Aggregation)
    new_centroids = []
    
    for i in range(len(centroids)):
        total_sum = np.zeros(3, dtype=np.float64)
        total_count = 0
        
        # Aggregate results from all mappers for this centroid
        for partial_result in map_results:
            if i in partial_result:
                total_sum += partial_result[i]['sum']
                total_count += partial_result[i]['count']
        
        # Calculate new average
        if total_count > 0:
            new_centroids.append(total_sum / total_count)
        else:
            # If a cluster is empty, keep the old centroid
            new_centroids.append(centroids[i])
            
    return new_centroids
