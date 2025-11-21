from PIL import Image
import numpy as np
import os
from src.math_utils import manhattan_distance

def load_image_as_array(image_path):
    """
    Reads an image and returns it as a flat numpy array of pixels.
    
    Args:
        image_path (str): Path to the source image.
        
    Returns:
        tuple: (pixels_array, width, height)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    # Convert to numpy array and reshape to (N, 3)
    pixels = np.array(img).reshape(-1, 3)
    
    print(f"Loaded image {image_path}. Size: {width}x{height} ({len(pixels)} pixels)")
    return pixels, width, height

def reconstruct_image_from_array(pixels, centroids, width, height, output_image_path):
    """
    Reconstructs the image using the final centroids (in-memory version).
    """
    print("Reconstructing image...")
    
    # We need to assign each pixel to its nearest centroid one last time
    # Optimization: We can do this in parallel too, but for simplicity let's do it here
    # or use a simple loop. For 4K image, this might take a moment.
    
    new_pixels = np.zeros_like(pixels)
    
    for i, pixel in enumerate(pixels):
        min_dist = float('inf')
        nearest_centroid = None
        
        for centroid in centroids:
            dist = np.sum(np.abs(pixel - centroid)) # Manhattan
            if dist < min_dist:
                min_dist = dist
                nearest_centroid = centroid
        
        new_pixels[i] = nearest_centroid
        
    # Reshape back to image dimensions
    img_array = new_pixels.reshape(height, width, 3).astype(np.uint8)
    img = Image.fromarray(img_array)
    img.save(output_image_path)
    print(f"Saved reconstructed image to {output_image_path}")

def save_centroids(centroids, filepath):
    with open(filepath, 'w') as f:
        for c in centroids:
            f.write(','.join(map(str, c)) + '\n')

def load_centroids(filepath):
    centroids = []
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        for line in f:
            if line.strip():
                centroids.append(list(map(float, line.strip().split(','))))
    return centroids
