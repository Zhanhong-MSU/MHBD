# MHBG-1: MapReduce Algorithms Implementation

This project implements two algorithms using Python's MRJob framework:

## 🧹 **Project Cleanup**

**⚠️ Important**: There are redundant files in the root directory that should be cleaned up.

To remove duplicate files and get a clean project structure:

```bash
python3 cleanup.py
```

This will remove:
- `tfidf.py` (duplicate - use `tfidf/tfidf.py`)
- `shortest_path.py` (duplicate - use `shortest_path/shortest_path.py`) 
- `doc*.txt` files (duplicates - use files in `tfidf/`)
- `graph*.txt` files (duplicates - use files in `shortest_path/`)
- `test.py` (replaced by `test_all.py`)

## 📁 **Clean Project Structure**

After cleanup, the structure should be:

```
MHBG-1/
├── README.md              # Main project documentation
├── requirements.txt       # Python dependencies
├── test_all.py           # Master test script
├── homework_1.pdf        # Original assignment
├── tfidf/                # TF-IDF Algorithm
│   ├── tfidf.py          # TF-IDF implementation
│   ├── test_tfidf.py     # TF-IDF tests
│   ├── README.md         # TF-IDF documentation
│   └── doc*.txt          # Sample documents
└── shortest_path/        # Shortest Path Algorithm
    ├── shortest_path.py  # Shortest path implementation
    ├── test_shortest_path.py # Tests
    ├── README.md         # Documentation
    └── graph*.txt        # Sample graphs
```

## 🎯 Algorithms Implemented

### 1. TF-IDF Algorithm
- **Purpose**: Rank documents by relevance to search query using TF-IDF scoring
- **Location**: `/tfidf/` folder
- **Grade Target**: 4 points (良)

### 2. Shortest Path Algorithm
- **Purpose**: Find shortest path in weighted graphs using MapReduce
- **Location**: `/shortest_path/` folder
- **Features**: Supports both positive and negative weights (bonus)

## 🚀 Quick Start

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Clean Up Project (First Time)
```bash
python3 cleanup.py
```

### Run All Tests
```bash
python3 test_all.py
```

### Test Individual Algorithms

#### TF-IDF
```bash
cd tfidf/
python3 test_tfidf.py
```

#### Shortest Path
```bash
cd shortest_path/
python3 test_shortest_path.py
```

## 📖 Detailed Usage

### TF-IDF Algorithm
```bash
cd tfidf/
python3 tfidf.py --query "search terms" --input-dir "." input_file.txt
```

### Shortest Path Algorithm
```bash
cd shortest_path/
# Positive weights
python3 shortest_path.py --source A --target F graph.txt

# Negative weights (bonus feature)
python3 shortest_path.py --source A --target F --allow-negative graph_negative.txt
```

## 🔧 Requirements

- Python 3.x
- mrjob library

## 📚 Documentation

Each algorithm folder contains its own README.md with detailed documentation and usage examples.
