#!/usr/bin/env python3
"""
Cleanup script to remove redundant files from root directory
"""
import os

def cleanup_root_directory():
    """Remove redundant files from project root"""
    root_dir = "/workspaces/MHBG-1"
    
    # Files that should be removed (they exist in subfolders)
    files_to_remove = [
        "tfidf.py",           # Moved to tfidf/
        "shortest_path.py",   # Moved to shortest_path/
        "doc1.txt",          # Moved to tfidf/
        "doc2.txt",          # Moved to tfidf/
        "doc3.txt",          # Moved to tfidf/
        "graph.txt",         # Moved to shortest_path/
        "graph_negative.txt", # Moved to shortest_path/
        "test.py"            # Replaced by test_all.py and individual test scripts
    ]
    
    print("🧹 Cleaning up redundant files...")
    removed_count = 0
    
    for filename in files_to_remove:
        filepath = os.path.join(root_dir, filename)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"✅ Removed: {filename}")
                removed_count += 1
            else:
                print(f"ℹ️  Already gone: {filename}")
        except Exception as e:
            print(f"❌ Failed to remove {filename}: {e}")
    
    print(f"\n🎉 Cleanup complete! Removed {removed_count} redundant files.")
    
    # Show clean project structure
    print("\n📁 Clean project structure:")
    print("MHBG-1/")
    print("├── README.md              # Main project documentation") 
    print("├── requirements.txt       # Python dependencies")
    print("├── test_all.py           # Master test script")
    print("├── homework_1.pdf        # Original assignment")
    print("├── tfidf/                # TF-IDF Algorithm")
    print("│   ├── tfidf.py          # TF-IDF implementation")
    print("│   ├── test_tfidf.py     # TF-IDF tests")
    print("│   ├── README.md         # TF-IDF documentation")
    print("│   └── doc*.txt          # Sample documents")
    print("└── shortest_path/        # Shortest Path Algorithm")
    print("    ├── shortest_path.py  # Shortest path implementation")
    print("    ├── test_shortest_path.py # Tests")
    print("    ├── README.md         # Documentation")
    print("    └── graph*.txt        # Sample graphs")

if __name__ == "__main__":
    cleanup_root_directory()