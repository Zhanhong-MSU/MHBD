# TF-IDF Algorithm Implementation

This folder contains the TF-IDF (Term Frequency * Inverse Document Frequency) algorithm implementation for academic paper analysis.

## 📁 Project Structure

```
tfidf/
├── documents/                          # Input documents directory
│   ├── paper1_machine_learning.txt     # ML in Healthcare paper
│   ├── paper2_deep_learning.txt        # Deep Learning NLP paper  
│   ├── paper3_data_science.txt         # Data Science Business paper
│   ├── paper4_artificial_intelligence.txt  # AI Ethics paper
│   └── paper5_computer_vision.txt      # Computer Vision paper
├── tfidf_english.py                    # 🎯 Main TF-IDF implementation (RECOMMENDED)
├── run_analysis.py                     # 📊 Complete demonstration script
├── tfidf.py                           # MRJob distributed version (optional)
├── requirements.txt                    # Dependencies (none required for main script)
└── README.md                          # This file
```

## 🚀 Quick Start

### Option 1: Direct Execution (Recommended)
```bash
python3 tfidf_english.py
```

### Option 2: Full Demonstration
```bash
python3 run_analysis.py
```

## 📋 System Requirements

- **Python**: 3.6 or higher
- **Dependencies**: None (uses only Python standard library)
- **OS**: Any (Linux, Windows, macOS)
- **Memory**: Minimum 512MB RAM
- **Storage**: 10MB free space

## 🌐 VPS Deployment

### Step 1: Upload Files
```bash
# Upload the entire tfidf/ folder to your VPS
scp -r tfidf/ user@your-vps-ip:/path/to/destination/
```

### Step 2: Connect and Run
```bash
# Connect to VPS
ssh user@your-vps-ip

# Navigate to project directory
cd /path/to/destination/tfidf/

# Run the analysis
python3 tfidf_english.py
```

### Step 3: Verify Installation
```bash
# Check Python version (must be 3.6+)
python3 --version

# Check file structure
ls -la documents/

# Run quick test
python3 -c "import re, math, os; print('✅ All dependencies available')"
```

## 📊 Output Examples

### Query Results Format
```
Query: 'machine learning healthcare'
----------------------------------------
1. paper1_machine_learning.txt (Score: 0.0099)
   Matching terms:
     'machine': TF=0.0325, IDF=0.2231, TF-IDF=0.0073
     'learning': TF=0.0447, IDF=0.0000, TF-IDF=0.0000
     'healthcare': TF=0.0244, IDF=0.9163, TF-IDF=0.0223
```

## 🔧 Technical Details

### Algorithm Implementation
- **TF (Term Frequency)**: `count_of_word_in_doc / total_words_in_doc`
- **IDF (Inverse Document Frequency)**: `log(total_documents / documents_containing_word)`
- **TF-IDF Score**: `TF × IDF`
- **Document Ranking**: Average TF-IDF score for all query terms

### Test Queries
1. "machine learning healthcare"
2. "deep learning natural language"  
3. "data science business analytics"
4. "artificial intelligence ethics"
5. "computer vision autonomous systems"
6. "neural networks algorithms"
7. "predictive analytics"
8. "transformer models"

## 🐛 Troubleshooting

### Common Issues

**Python version error:**
```bash
# Update Python on Ubuntu/Debian
sudo apt update && sudo apt install python3

# Update Python on CentOS/RHEL  
sudo yum install python3
```

**File encoding error:**
```bash
# Check file encoding
file documents/*.txt

# Fix if needed (convert to UTF-8)
iconv -f ISO-8859-1 -t UTF-8 input.txt > output.txt
```

**Permission error:**
```bash
# Fix file permissions
chmod +x *.py
chmod -R 644 documents/
```

## 📈 Performance

- **Processing Time**: ~0.1 seconds for 5 documents (~2000 words)
- **Memory Usage**: ~10MB for typical document collection
- **Scalability**: Linear with document count and vocabulary size

## 🎓 Academic Usage

This implementation is designed for educational purposes and demonstrates:
- Information retrieval concepts
- Document ranking algorithms  
- Text processing techniques
- Statistical analysis methods

Perfect for computer science assignments, research projects, and learning TF-IDF fundamentals.

## 📞 Support

For issues or questions:
1. Verify Python 3.6+ is installed
2. Check all files are present in correct structure
3. Ensure documents/ folder contains .txt files
4. Run with `-v` flag for verbose output if available