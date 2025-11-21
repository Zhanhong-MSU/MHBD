# Utility Scripts

This folder contains helper scripts for dataset management.

## Files

- **`download_full_newsgroups.py`** - Script to download the complete 20 Newsgroups dataset (17,901 documents)

## Usage

To download the full dataset:

```bash
cd scripts
python3 download_full_newsgroups.py
```

This will download all documents to `../documents/newsgroups_full/`.

**Note**: This script requires `scikit-learn`:
```bash
pip install scikit-learn
```
