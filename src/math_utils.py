import numpy as np

def manhattan_distance(point1, point2):
    """
    Calculate the Manhattan distance (L1 Norm) between two points.
    
    Args:
        point1 (list or np.array): Coordinates of the first point (e.g., [R, G, B]).
        point2 (list or np.array): Coordinates of the second point (e.g., [R, G, B]).
        
    Returns:
        float: The Manhattan distance.
    """
    p1 = np.array(point1)
    p2 = np.array(point2)
    return np.sum(np.abs(p1 - p2))
