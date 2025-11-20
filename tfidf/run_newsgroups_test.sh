#!/bin/bash
# One-click setup and test script for 20 Newsgroups TF-IDF

echo "🚀 20 Newsgroups TF-IDF Setup and Test"
echo "======================================"
echo ""

# Check if we're in the right directory
if [[ ! -f "download_newsgroups.py" ]]; then
    echo "❌ Error: Not in tfidf directory"
    echo "Please run: cd /workspaces/MHBG-1/tfidf"
    exit 1
fi

# Step 1: Install dependencies
echo "📦 Step 1: Installing dependencies..."
pip3 install scikit-learn
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: pip install failed, trying with --user flag"
    pip3 install --user scikit-learn
fi
echo ""

# Step 2: Download dataset
echo "📥 Step 2: Downloading 20 Newsgroups dataset..."
python3 download_newsgroups.py
if [ $? -ne 0 ]; then
    echo "❌ Error downloading dataset"
    exit 1
fi
echo ""

# Step 3: Create input file
echo "📝 Step 3: Creating TF-IDF input file..."
python3 create_tfidf_input.py
if [ $? -ne 0 ]; then
    echo "❌ Error creating input file"
    exit 1
fi
echo ""

# Step 4: Run TF-IDF tests
echo "🔍 Step 4: Running TF-IDF tests..."
echo ""

echo "Test 1: Computer Graphics Query"
echo "--------------------------------"
python3 tfidf.py --query "computer graphics image" --input-dir "." newsgroups_input.txt | grep -E "^[\(\"]" | head -5
echo ""

echo "Test 2: Medical Query"
echo "---------------------"
python3 tfidf.py --query "medical health disease" --input-dir "." newsgroups_input.txt | grep -E "^[\(\"]" | head -5
echo ""

echo "Test 3: Baseball Query"
echo "----------------------"
python3 tfidf.py --query "baseball game team" --input-dir "." newsgroups_input.txt | grep -E "^[\(\"]" | head -5
echo ""

echo "🎉 All tests completed!"
echo ""
echo "📊 Dataset info:"
ls -lh documents/ | head -10
echo "..."
echo "Total documents: $(ls documents/*.txt | wc -l)"
echo ""
echo "💡 Try more queries:"
echo "   python3 tfidf.py --query 'politics government' --input-dir '.' newsgroups_input.txt"
echo "   python3 tfidf.py --query 'religion god atheism' --input-dir '.' newsgroups_input.txt"