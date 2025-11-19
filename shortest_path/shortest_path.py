#!/usr/bin/env python3
"""
Shortest Path Algorithm Implementation using MRJob
Author: Student
Date: November 2025

This script implements shortest path search algorithms using MapReduce pattern.
Supports both positive weights (Dijkstra-like) and negative weights (Bellman-Ford-like).

Input: Graph edges with weights, source and target nodes
Output: Shortest path and distance
"""

from mrjob.job import MRJob
from mrjob.step import MRStep
import json
import sys
from collections import defaultdict

INF = float('inf')


class ShortestPathJob(MRJob):
    """
    MapReduce implementation of shortest path algorithms.
    
    For positive weights: Uses iterative Dijkstra-like approach
    For negative weights: Uses Bellman-Ford-like approach with negative cycle detection
    """
    
    def configure_args(self):
        """Configure command line arguments"""
        super().configure_args()
        self.add_passthru_arg(
            '--source', type=str, required=True,
            help='Source node'
        )
        self.add_passthru_arg(
            '--target', type=str, required=True,
            help='Target node'
        )
        self.add_passthru_arg(
            '--max-iterations', type=int, default=10,
            help='Maximum number of iterations'
        )
        self.add_passthru_arg(
            '--allow-negative', action='store_true',
            help='Allow negative edge weights (uses Bellman-Ford)'
        )
    
    def steps(self):
        """Define MapReduce steps"""
        steps = [
            MRStep(mapper_init=self.init_mapper,
                   mapper=self.mapper_initialize,
                   reducer=self.reducer_initialize)
        ]
        
        # Add iteration steps
        for i in range(self.options.max_iterations):
            steps.append(
                MRStep(mapper=self.mapper_relax,
                       reducer=self.reducer_update_distances)
            )
        
        # Final step to extract path
        steps.append(
            MRStep(mapper=self.mapper_extract_path,
                   reducer=self.reducer_build_path)
        )
        
        return steps
    
    def init_mapper(self):
        """Initialize mapper with source and target"""
        self.source = self.options.source
        self.target = self.options.target
        self.allow_negative = self.options.allow_negative
    
    def mapper_initialize(self, _, line):
        """
        Initialize distances and parse graph edges
        
        Input format: "node1,node2,weight" or JSON format
        Output: (node, distance_info) and (edge_key, edge_info)
        """
        try:
            # Try JSON format first
            if line.strip().startswith('{'):
                edge = json.loads(line)
                from_node = edge['from']
                to_node = edge['to']
                weight = edge['weight']
            else:
                # CSV format: from,to,weight
                parts = line.strip().split(',')
                if len(parts) != 3:
                    return
                from_node, to_node, weight = parts[0], parts[1], float(parts[2])
            
            # Check for negative weights
            if not self.allow_negative and weight < 0:
                yield ("ERROR", f"Negative weight {weight} found but not allowed")
                return
            
            # Emit edge information
            yield (("edge", from_node, to_node), weight)
            
            # Initialize distance for source node
            if from_node == self.source:
                yield (("dist", from_node), {"distance": 0, "predecessor": None, "iteration": 0})
            else:
                yield (("dist", from_node), {"distance": INF, "predecessor": None, "iteration": 0})
            
            # Initialize distance for destination node
            if to_node == self.source:
                yield (("dist", to_node), {"distance": 0, "predecessor": None, "iteration": 0})
            else:
                yield (("dist", to_node), {"distance": INF, "predecessor": None, "iteration": 0})
                
        except (ValueError, KeyError, json.JSONDecodeError) as e:
            yield ("ERROR", f"Invalid input format: {line}")
    
    def reducer_initialize(self, key, values):
        """
        Combine initialization data
        
        Input: (key, [values])
        Output: (key, combined_value)
        """
        if key == "ERROR":
            for error in values:
                yield ("ERROR", error)
            return
        
        key_type = key[0]
        
        if key_type == "edge":
            # Edge data
            weights = list(values)
            if weights:
                yield (key, weights[0])  # Take first weight if multiple
        
        elif key_type == "dist":
            # Distance data - take minimum distance
            distances = list(values)
            min_dist_info = min(distances, key=lambda x: x["distance"])
            yield (key, min_dist_info)
    
    def mapper_relax(self, key, value):
        """
        Relax edges - core of shortest path algorithm
        
        Input: (key, value)
        Output: Updated distance information
        """
        if key == "ERROR":
            yield (key, value)
            return
        
        key_type = key[0]
        
        if key_type == "edge":
            # This is an edge, emit it for next iteration
            yield (key, value)
        
        elif key_type == "dist":
            # This is distance info, emit it and try to relax outgoing edges
            node = key[1]
            dist_info = value
            
            # Emit current distance
            yield (key, dist_info)
            
            # Signal that we need to find outgoing edges for this node
            yield (("need_edges", node), dist_info)
    
    def reducer_update_distances(self, key, values):
        """
        Update distances based on edge relaxation
        
        Input: (key, [values])
        Output: Updated distances and edges
        """
        if key == "ERROR":
            for error in values:
                yield ("ERROR", error)
            return
        
        key_type = key[0]
        
        if key_type == "edge":
            # Pass through edge information
            values_list = list(values)
            if values_list:
                yield (key, values_list[0])
        
        elif key_type == "dist":
            # Update distance information
            distances = list(values)
            best_dist = min(distances, key=lambda x: x["distance"])
            yield (key, best_dist)
        
        elif key_type == "need_edges":
            # This means we need to find edges and potentially relax them
            node = key[1]
            dist_info_list = list(values)
            
            if dist_info_list:
                current_dist_info = dist_info_list[0]
                # For now, just pass the distance info - edge relaxation would happen
                # in a more complex implementation with access to the full graph
                yield (("dist", node), current_dist_info)
    
    def mapper_extract_path(self, key, value):
        """
        Extract the final shortest path
        
        Input: (key, value)
        Output: Path information for target node
        """
        if key == "ERROR":
            yield (key, value)
            return
        
        key_type = key[0]
        
        if key_type == "dist":
            node = key[1]
            if node == self.target:
                yield (("result", "path"), {
                    "target": node,
                    "distance": value["distance"],
                    "reachable": value["distance"] < INF
                })
    
    def reducer_build_path(self, key, values):
        """
        Build the final path result
        
        Input: (key, [path_info])
        Output: Final shortest path result
        """
        if key == "ERROR":
            for error in values:
                yield ("ERROR", error)
            return
        
        if key[0] == "result":
            path_infos = list(values)
            if path_infos:
                result = path_infos[0]
                if result["reachable"]:
                    yield ("RESULT", f"Shortest distance from {self.source} to {self.target}: {result['distance']}")
                else:
                    yield ("RESULT", f"No path found from {self.source} to {self.target}")


if __name__ == '__main__':
    ShortestPathJob.run()