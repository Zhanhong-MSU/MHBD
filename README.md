# K-means Image Color Quantization using MapReduce

This project implements K-means clustering for image color quantization using Hadoop MapReduce (via `mrjob`). It uses Manhattan distance as the metric.

## Project Structure

```text
.
├── dataset/
│   ├── source_image.jpg         # Input image
│   ├── pixels_input.txt         # Intermediate pixel data
│   ├── initial_centroids.txt    # Centroids file
│   └── output_images/           # Output directory
├── src/
│   ├── mr_kmeans.py             # MapReduce Job
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
   Note: If you encounter an error about `distutils` (e.g. on Python 3.12+), install `setuptools`:
   ```bash
   pip install setuptools
   ```

## Usage

1. Place your input image at `dataset/source_image.jpg`.
   Or run the helper script to download a sample image:
   ```bash
   python3 src/download_sample.py
   ```

2. Run the main program:
   ```bash
   python3 main.py
   ```

3. The result will be saved to `dataset/output_images/result.jpg`.

## Configuration

You can modify `main.py` to change:
- `K`: Number of clusters (colors).
- `MAX_ITER`: Maximum number of iterations.
- `THRESHOLD`: Convergence threshold.

## Implementation Details

- **Distance Metric**: Manhattan Distance ($|R_1 - R_2| + |G_1 - G_2| + |B_1 - B_2|$).
- **MapReduce**: 
    - **Mapper**: Assigns each pixel to the nearest centroid.
    - **Reducer**: Calculates the new centroid for each cluster.
