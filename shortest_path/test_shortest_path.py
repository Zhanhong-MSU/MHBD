#!/usr/bin/env python3
"""
Test script for Shortest Path algorithm
Author: Student
Date: November 2025
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Run a command and display results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✓ Success")
            print("\nOutput:")
            print("-" * 40)
            print(result.stdout)
            if result.stderr:
                print("Warnings:")
                print(result.stderr)
        else:
            print("✗ Failed")
            print("Error:", result.stderr)
            
    except subprocess.TimeoutExpired:
        print("⚠ Timeout")
    except Exception as e:
        print(f"⚠ Error: {e}")

def test_shortest_path():
    """Test shortest path algorithms"""
    print("Testing Shortest Path Algorithms")
    print("=" * 40)
    
    test_cases = [
        {
            'graph': 'graph.txt',
            'source': 'A',
            'target': 'F',
            'description': 'Shortest path from A to F (positive weights)',
            'negative': False
        },
        {
            'graph': 'graph.txt',
            'source': 'A',
            'target': 'E',
            'description': 'Shortest path from A to E (positive weights)',
            'negative': False
        },
        {
            'graph': 'graph_negative.txt',
            'source': 'A',
            'target': 'F',
            'description': 'Shortest path from A to F (with negative weights)',
            'negative': True
        }
    ]
    
    for test in test_cases:
        if not os.path.exists(test['graph']):
            print(f"Graph file {test['graph']} not found, skipping...")
            continue
        
        cmd = [
            sys.executable, "shortest_path.py",
            "--source", test['source'],
            "--target", test['target']
        ]
        
        if test['negative']:
            cmd.append("--allow-negative")
        
        cmd.append(test['graph'])
        
        run_command(cmd, test['description'])

def main():
    """Main test function"""
    # Check if we're in the shortest_path directory
    if not os.path.exists("shortest_path.py"):
        print("Error: shortest_path.py not found. Please run this script from the shortest_path directory.")
        return
    
    # Check for mrjob
    try:
        import mrjob
        print(f"✓ mrjob available (version: {mrjob.__version__})")
    except ImportError:
        print("Installing mrjob...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mrjob"])
    
    test_shortest_path()
    
    print("\\nShortest Path testing complete!")

if __name__ == "__main__":
    main()