# 20 Newsgroups Dataset Setup Guide

## 🚀 Quick Setup

Follow these steps to download and test TF-IDF with the 20 Newsgroups dataset:

### Step 1: Install Dependencies
```bash
pip install scikit-learn
```

### Step 2: Download Dataset
```bash
cd /workspaces/MHBG-1/tfidf
python3 download_newsgroups.py
```

This will:
- Download ~2,500 documents from 5 newsgroups categories
- Save them to `documents/` directory
- Create a dataset summary file

### Step 3: Create TF-IDF Input File
```bash
python3 create_tfidf_input.py
```

This will:
- Read all documents from `documents/` directory
- Create `newsgroups_input.txt` in tab-separated format
- Ready for TF-IDF processing

### Step 4: Run TF-IDF Analysis
```bash
# Example queries based on newsgroups categories:

# Computer Graphics
python3 tfidf.py --query "computer graphics image" --input-dir "." newsgroups_input.txt

# Medical/Science
python3 tfidf.py --query "medical health disease" --input-dir "." newsgroups_input.txt

# Baseball/Sports
python3 tfidf.py --query "baseball game team" --input-dir "." newsgroups_input.txt

# Politics
python3 tfidf.py --query "politics government law" --input-dir "." newsgroups_input.txt

# Religion/Atheism
python3 tfidf.py --query "religion god atheism" --input-dir "." newsgroups_input.txt
```

## 📊 Dataset Information

### Categories Included:
1. **comp.graphics** - Computer graphics discussions
2. **sci.med** - Medical and health topics
3. **rec.sport.baseball** - Baseball discussions
4. **talk.politics.misc** - Political discussions
5. **alt.atheism** - Atheism discussions

### Dataset Size:
- ~2,500 documents total
- ~500 documents per category
- Average document length: 100-500 words

## 🎯 Expected Results

TF-IDF will rank documents based on query relevance:
- Higher TF-IDF scores = more relevant documents
- Documents are ranked by average TF-IDF score for all query terms
- Output format: `(negative_score, filename)`

## 🔧 Troubleshooting

### scikit-learn not installed:
```bash
pip install scikit-learn
# or
pip3 install scikit-learn
```

### Documents folder not found:
```bash
# Make sure you're in the tfidf directory
cd /workspaces/MHBG-1/tfidf
# Then run download script again
python3 download_newsgroups.py
```

### Memory issues with large dataset:
The script downloads a subset of categories. To use fewer documents:
- Edit `download_newsgroups.py`
- Reduce the number of categories
- Or use `subset='test'` instead of `subset='train'`

## 📝 Files Created

After setup, you'll have:
```
tfidf/
├── documents/              # Downloaded newsgroups documents
│   ├── comp_graphics_0001.txt
│   ├── sci_med_0001.txt
│   └── ...
├── newsgroups_input.txt   # TF-IDF input file
└── dataset_info.txt       # Dataset summary
```