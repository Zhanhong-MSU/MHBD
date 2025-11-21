from PIL import Image
import numpy as np
import os
from src.math_utils import manhattan_distance

def image_to_pixels(image_path, output_text_path):
    """
    Reads an image and converts it to a text file where each line is:
    row_id, col_id, R, G, B
    
    Args:
        image_path (str): Path to the source image.
        output_text_path (str): Path to save the pixel data.
        
    Returns:
        tuple: (width, height) of the image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size
    pixels = np.array(img)

    with open(output_text_path, 'w') as f:
        for r in range(height):
            for c in range(width):
                R, G, B = pixels[r, c]
                f.write(f"{r},{c},{R},{G},{B}\n")
    
    print(f"Converted image {image_path} to text {output_text_path}. Size: {width}x{height}")
    return width, height

def reconstruct_image(pixels_path, centroids, width, height, output_image_path):
    """
    Reconstructs the image using the final centroids.
    Each pixel is replaced by the color of its nearest centroid.
    
    Args:
        pixels_path (str): Path to the pixel text file.
        centroids (list): List of final centroids (each is [R, G, B]).
        width (int): Image width.
        height (int): Image height.
        output_image_path (str): Path to save the result image.
    """
    # Create a blank image array
    new_pixels = np.zeros((height, width, 3), dtype=np.uint8)
    
    print("Reconstructing image...")
    with open(pixels_path, 'r') as f:
        for line in f:
            parts = list(map(int, line.strip().split(',')))
            r_idx, c_idx = parts[0], parts[1]
            pixel_rgb = parts[2:]
            
            # Find nearest centroid
            min_dist = float('inf')
            nearest_centroid = None
            
            for centroid in centroids:
                dist = manhattan_distance(pixel_rgb, centroid)
                if dist < min_dist:
                    min_dist = dist
                    nearest_centroid = centroid
            
            new_pixels[r_idx, c_idx] = nearest_centroid

    img = Image.fromarray(new_pixels)
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
