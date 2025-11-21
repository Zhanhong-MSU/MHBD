# Utility Scripts

This folder contains helper scripts for dataset management and system information.

## Files

### Dataset Management

- **`download_full_newsgroups.py`** - Script to download the complete 20 Newsgroups dataset (17,901 documents)

### System Information

- **`demo_cpu_detection.py`** - Demonstrates automatic CPU core detection and performance estimation
  - Shows available CPU cores on your system
  - Displays expected performance improvements with parallel processing
  - Provides usage recommendations based on your hardware
  - Usage: `python3 demo_cpu_detection.py`

## Usage

**To download the full dataset:**

```bash
cd scripts
python3 download_full_newsgroups.py
```

This will download all documents to `../dataset/newsgroups_full/`.

**Note**: This script requires `scikit-learn`:
```bash
pip install scikit-learn
```

**To check your system's CPU configuration:**

```bash
cd scripts
python3 demo_cpu_detection.py
```

This will show you how many cores are available and the expected speedup from parallel processing.
