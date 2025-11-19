# Testing Guide for MHBG-1 Project

## ✅ Project Status

Your project has been successfully organized and cleaned up! Here's what we have:

### 📁 Clean Project Structure
```
MHBG-1/
├── README.md              ✅ Complete documentation
├── requirements.txt       ✅ Dependencies (mrjob>=0.7.4)
├── test_all.py           ✅ Master test script
├── validate.py           ✅ Validation script
├── cleanup.py            ✅ Cleanup utility (already used)
├── homework_1.pdf        ✅ Original assignment
├── tfidf/                ✅ TF-IDF Algorithm
│   ├── tfidf.py          ✅ Complete implementation
│   ├── test_tfidf.py     ✅ Test script
│   ├── README.md         ✅ Documentation
│   ├── doc1.txt          ✅ Sample: Python/ML content
│   ├── doc2.txt          ✅ Sample: Java content  
│   └── doc3.txt          ✅ Sample: ML/AI content
└── shortest_path/        ✅ Shortest Path Algorithm
    ├── shortest_path.py  ✅ Complete implementation
    ├── test_shortest_path.py ✅ Test script
    ├── README.md         ✅ Documentation
    ├── graph.txt         ✅ Sample: Positive weights
    └── graph_negative.txt ✅ Sample: Negative weights
```

## 🚀 How to Test Your Algorithms

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Both Algorithms
```bash
# Run master test script
python3 test_all.py

# Or validate project structure
python3 validate.py
```

### 3. Test Individual Algorithms

#### TF-IDF Algorithm
```bash
cd tfidf/

# Run tests
python3 test_tfidf.py

# Manual test examples:
# Create input file
echo -e "doc1.txt\tPython machine learning data science" > test_input.txt
echo -e "doc2.txt\tJava programming enterprise applications" >> test_input.txt
echo -e "doc3.txt\tMachine learning artificial intelligence" >> test_input.txt

# Run TF-IDF
python3 tfidf.py --query "python machine" --input-dir "." test_input.txt
```

#### Shortest Path Algorithm
```bash
cd shortest_path/

# Run tests  
python3 test_shortest_path.py

# Manual test examples:
# Positive weights
python3 shortest_path.py --source A --target F graph.txt

# Negative weights (bonus feature)
python3 shortest_path.py --source A --target F --allow-negative graph_negative.txt
```

## 🎯 Algorithm Features

### TF-IDF Implementation
- ✅ **3-step MapReduce process**
  1. Term Frequency (TF) calculation
  2. Inverse Document Frequency (IDF) calculation  
  3. TF-IDF scoring and ranking
- ✅ **Command line interface** with query and input-dir arguments
- ✅ **Document ranking** by average TF-IDF score
- ✅ **English comments** as requested

### Shortest Path Implementation  
- ✅ **Positive weight support** (Dijkstra-like approach)
- ✅ **Negative weight support** (Bellman-Ford-like) - **BONUS FEATURE**
- ✅ **Iterative MapReduce** implementation
- ✅ **Command line interface** with source, target, and options
- ✅ **English comments** as requested

## 🏆 Grade Target Compliance

### TF-IDF Algorithm (Target: 4 points/良)
- ✅ Implements complete TF-IDF algorithm using MapReduce
- ✅ Accepts directory of text files and search query
- ✅ Outputs ranked list by average TF-IDF score
- ✅ Flexible input/output format (tab-separated)
- ✅ Clean, documented English code

### Shortest Path Algorithm  
- ✅ Implements shortest path search using MapReduce
- ✅ Graph edges with positive weights (**main requirement**)
- ✅ Negative weight support (**bonus feature**)
- ✅ Flexible input format (CSV)
- ✅ Clean, documented English code

## 💡 Project Highlights

1. **Clean Organization**: Each algorithm in separate folder
2. **Complete Documentation**: README files for each component
3. **Test Coverage**: Individual and master test scripts
4. **Bonus Features**: Negative weight shortest path support
5. **Professional Structure**: Follows software engineering best practices
6. **English Documentation**: All comments and docs in English as requested

## 🎉 Ready for Submission!

Your project is complete and ready for evaluation:
- Both algorithms implemented using mrjob
- Clean project structure with no redundant files
- Comprehensive testing and documentation
- Bonus features included
- Grade target of 4 points (良) should be achievable!