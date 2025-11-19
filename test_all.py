#!/usr/bin/env python3
"""
Master test script for all algorithms
Author: Student
Date: November 2025

This script runs tests for both TF-IDF and Shortest Path algorithms.
"""

import subprocess
import sys
import os

def run_test_in_directory(directory, test_script):
    """Run a test script in a specific directory"""
    print(f"\n{'='*80}")
    print(f"TESTING {directory.upper()} ALGORITHM")
    print('='*80)
    
    if not os.path.exists(directory):
        print(f"❌ Directory {directory} not found!")
        return False
    
    test_path = os.path.join(directory, test_script)
    if not os.path.exists(test_path):
        print(f"❌ Test script {test_script} not found in {directory}!")
        return False
    
    try:
        # Change to the directory and run the test
        original_dir = os.getcwd()
        os.chdir(directory)
        
        result = subprocess.run(
            [sys.executable, test_script], 
            capture_output=True, 
            text=True, 
            timeout=120
        )
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            print(f"✅ {directory.upper()} tests completed successfully!")
            print("\nOutput:")
            print("-" * 40)
            print(result.stdout)
            return True
        else:
            print(f"❌ {directory.upper()} tests failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {directory.upper()} tests timed out!")
        return False
    except Exception as e:
        print(f"💥 Error running {directory.upper()} tests: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("🔧 Installing dependencies...")
    try:
        # Check if mrjob is already installed
        import mrjob
        print(f"✅ mrjob already installed (version: {mrjob.__version__})")
        return True
    except ImportError:
        print("📦 Installing mrjob...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "mrjob"])
            print("✅ mrjob installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install mrjob!")
            return False

def check_project_structure():
    """Check if project structure is correct"""
    print("🔍 Checking project structure...")
    
    required_items = [
        ("tfidf", "directory"),
        ("shortest_path", "directory"),
        ("requirements.txt", "file"),
        ("tfidf/tfidf.py", "file"),
        ("tfidf/test_tfidf.py", "file"),
        ("shortest_path/shortest_path.py", "file"),
        ("shortest_path/test_shortest_path.py", "file")
    ]
    
    all_good = True
    for item, item_type in required_items:
        if item_type == "directory":
            exists = os.path.isdir(item)
        else:
            exists = os.path.isfile(item)
        
        if exists:
            print(f"✅ {item}")
        else:
            print(f"❌ {item} not found!")
            all_good = False
    
    return all_good

def main():
    """Main test orchestration"""
    print("🚀 MHBG-1 Master Test Script")
    print("=" * 50)
    print("Testing both TF-IDF and Shortest Path algorithms")
    print("=" * 50)
    
    # Check project structure
    if not check_project_structure():
        print("\n❌ Project structure is incomplete!")
        print("Please ensure all required files are present.")
        return
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies!")
        return
    
    # Run tests
    results = {}
    
    # Test TF-IDF
    results['tfidf'] = run_test_in_directory('tfidf', 'test_tfidf.py')
    
    # Test Shortest Path
    results['shortest_path'] = run_test_in_directory('shortest_path', 'test_shortest_path.py')
    
    # Summary
    print(f"\n{'='*80}")
    print("🎯 TEST SUMMARY")
    print('='*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for algorithm, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{algorithm.upper():15} : {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} algorithms passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests completed successfully!")
        print("📋 Both algorithms are ready for submission.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} algorithm(s) failed.")
        print("🔧 Please check the error messages above.")
    
    print("\n📁 Project Structure:")
    print("├── tfidf/              - TF-IDF Algorithm")
    print("└── shortest_path/      - Shortest Path Algorithm")

if __name__ == "__main__":
    main()