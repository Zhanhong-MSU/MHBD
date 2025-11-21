from mrjob.job import MRJob
from mrjob.step import MRStep
import sys
from src.math_utils import manhattan_distance

class MRKMeans(MRJob):
    
    def configure_args(self):
        super(MRKMeans, self).configure_args()
        self.add_file_arg('--centroids-file', help='Path to the centroids file')

    def load_centroids(self):
        # Load centroids from the file passed via --centroids-file
        self.centroids = []
        try:
            with open(self.options.centroids_file, 'r') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(',')
                        self.centroids.append([float(p) for p in parts])
        except Exception as e:
            sys.stderr.write(f"Error loading centroids: {e}\n")

    def mapper_init(self):
        self.load_centroids()

    def mapper(self, _, line):
        # Input format: row_id, col_id, R, G, B
        try:
            parts = list(map(int, line.strip().split(',')))
            # parts[0] is row, parts[1] is col
            pixel = parts[2:] # [R, G, B]
            
            min_dist = float('inf')
            nearest_idx = -1
            
            for idx, centroid in enumerate(self.centroids):
                dist = manhattan_distance(pixel, centroid)
                if dist < min_dist:
                    min_dist = dist
                    nearest_idx = idx
            
            # Emit: centroid_index, (R, G, B, 1)
            # We emit 1 to help calculate the average in the reducer
            yield nearest_idx, (pixel[0], pixel[1], pixel[2], 1)
            
        except ValueError:
            pass

    def reducer(self, key, values):
        # values is a generator of (R, G, B, 1)
        sum_r, sum_g, sum_b, count = 0, 0, 0, 0
        
        for r, g, b, c in values:
            sum_r += r
            sum_g += g
            sum_b += b
            count += c
            
        if count > 0:
            new_r = sum_r / count
            new_g = sum_g / count
            new_b = sum_b / count
            yield key, (new_r, new_g, new_b)

if __name__ == '__main__':
    MRKMeans.run()
