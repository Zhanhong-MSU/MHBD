# K-means Image Color Quantization (Parallel MapReduce)

This project implements K-means clustering for image color quantization. It uses a **Parallel MapReduce** architecture (via Python `multiprocessing`) to efficiently process high-resolution images (e.g., 4K) on multi-core systems.

## Project Structure

```text
.
├── dataset/
│   ├── source_image.jpg         # Input image
│   ├── initial_centroids.txt    # Centroids file
│   └── output_images/           # Output directory
├── src/
│   ├── parallel_kmeans.py       # Parallel MapReduce Engine
│   ├── mr_kmeans.py             # (Legacy) mrjob implementation
│   ├── image_utils.py           # Image processing utilities
│   ├── math_utils.py            # Math utilities (Manhattan distance)
│   └── download_sample.py       # Download sample image script
├── main.py                      # Main driver script
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Prerequisites

- Python 3.6+
- `pip`

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your input image at `dataset/source_image.jpg`.
   Or run the helper script to download a **4K sample image**:
   ```bash
   python3 src/download_sample.py
   ```

2. Run the main program:
   ```bash
   python3 main.py
   ```
   *The program will automatically detect the number of CPU cores and parallelize the workload.*

3. The result will be saved to `dataset/output_images/result.jpg`.

## Configuration

You can modify `main.py` to change:
- `K`: Number of clusters (colors).
- `MAX_ITER`: Maximum number of iterations.
- `THRESHOLD`: Convergence threshold.

## Implementation Details

- **Architecture**: In-Memory Parallel MapReduce.
- **Distance Metric**: Manhattan Distance ($|R_1 - R_2| + |G_1 - G_2| + |B_1 - B_2|$).
- **Map Phase**: The image pixels are split into chunks. Each CPU core processes a chunk to calculate local cluster sums and counts.
- **Reduce Phase**: The main process aggregates the local results from all cores to update the centroids.
