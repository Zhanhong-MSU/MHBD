# Shortest Path Algorithm Implementation

This folder contains the shortest path search algorithm implementation using MRJob.

## Files

- `shortest_path.py` - Main shortest path implementation
- `graph.txt` - Sample graph with positive edge weights
- `graph_negative.txt` - Sample graph with negative edge weights
- `test_shortest_path.py` - Test script for shortest path algorithm

## Usage

```bash
# Positive weights only (Dijkstra-like)
python3 shortest_path.py --source A --target F graph.txt

# With negative weights (Bellman-Ford-like)
python3 shortest_path.py --source A --target F --allow-negative graph_negative.txt
```

## Input Format

CSV file with edges:
```
node1,node2,weight
A,B,4
A,C,2
```

## Output

Shortest distance and path information.

## Features

- ✅ **Positive weights** (Dijkstra-like approach)
- ✅ **Negative weights** (Bellman-Ford-like approach) - *bonus feature*
- ✅ Iterative MapReduce implementation

## Testing

```bash
python3 test_shortest_path.py
```