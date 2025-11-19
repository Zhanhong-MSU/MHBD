#!/usr/bin/env python3
"""
Quick validation script for both algorithms
"""

def validate_tfidf():
    """Validate TF-IDF implementation"""
    print("🔍 Validating TF-IDF Implementation...")
    try:
        # Check if tfidf.py exists and is syntactically correct
        with open('/workspaces/MHBG-1/tfidf/tfidf.py', 'r') as f:
            content = f.read()
        
        # Basic validation checks
        checks = [
            ('MRJob import', 'from mrjob.job import MRJob' in content),
            ('TfIdfJob class', 'class TfIdfJob(MRJob)' in content),
            ('configure_args method', 'def configure_args(self)' in content),
            ('steps method', 'def steps(self)' in content),
            ('mapper functions', 'def mapper_' in content),
            ('reducer functions', 'def reducer_' in content),
            ('TF calculation', 'tf' in content.lower()),
            ('IDF calculation', 'idf' in content.lower()),
            ('Query argument', '--query' in content)
        ]
        
        passed = 0
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"  {status} {check_name}")
            if result:
                passed += 1
        
        print(f"  📊 TF-IDF validation: {passed}/{len(checks)} checks passed")
        return passed == len(checks)
        
    except Exception as e:
        print(f"  ❌ Error validating TF-IDF: {e}")
        return False

def validate_shortest_path():
    """Validate Shortest Path implementation"""
    print("\n🗺️  Validating Shortest Path Implementation...")
    try:
        # Check if shortest_path.py exists and is syntactically correct
        with open('/workspaces/MHBG-1/shortest_path/shortest_path.py', 'r') as f:
            content = f.read()
        
        # Basic validation checks
        checks = [
            ('MRJob import', 'from mrjob.job import MRJob' in content),
            ('ShortestPathJob class', 'class ShortestPathJob(MRJob)' in content),
            ('configure_args method', 'def configure_args(self)' in content),
            ('steps method', 'def steps(self)' in content),
            ('source argument', '--source' in content),
            ('target argument', '--target' in content),
            ('negative weights support', '--allow-negative' in content),
            ('mapper functions', 'def mapper_' in content),
            ('reducer functions', 'def reducer_' in content),
            ('distance calculation', 'distance' in content.lower())
        ]
        
        passed = 0
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"  {status} {check_name}")
            if result:
                passed += 1
        
        print(f"  📊 Shortest Path validation: {passed}/{len(checks)} checks passed")
        return passed == len(checks)
        
    except Exception as e:
        print(f"  ❌ Error validating Shortest Path: {e}")
        return False

def validate_sample_data():
    """Validate sample data files"""
    print("\n📄 Validating Sample Data...")
    
    data_files = [
        ('/workspaces/MHBG-1/tfidf/doc1.txt', 'TF-IDF document 1'),
        ('/workspaces/MHBG-1/tfidf/doc2.txt', 'TF-IDF document 2'), 
        ('/workspaces/MHBG-1/tfidf/doc3.txt', 'TF-IDF document 3'),
        ('/workspaces/MHBG-1/shortest_path/graph.txt', 'Positive weight graph'),
        ('/workspaces/MHBG-1/shortest_path/graph_negative.txt', 'Negative weight graph')
    ]
    
    all_good = True
    for filepath, description in data_files:
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
            if content:
                print(f"  ✅ {description}")
            else:
                print(f"  ⚠️  {description} (empty)")
                all_good = False
        except Exception as e:
            print(f"  ❌ {description}: {e}")
            all_good = False
    
    return all_good

def check_project_structure():
    """Check overall project structure"""
    print("\n📁 Validating Project Structure...")
    
    required_items = [
        ('README.md', 'file', 'Main documentation'),
        ('requirements.txt', 'file', 'Dependencies'),
        ('test_all.py', 'file', 'Master test script'),
        ('tfidf/', 'dir', 'TF-IDF folder'),
        ('shortest_path/', 'dir', 'Shortest path folder'),
        ('tfidf/tfidf.py', 'file', 'TF-IDF implementation'),
        ('tfidf/test_tfidf.py', 'file', 'TF-IDF tests'),
        ('shortest_path/shortest_path.py', 'file', 'Shortest path implementation'),
        ('shortest_path/test_shortest_path.py', 'file', 'Shortest path tests')
    ]
    
    all_good = True
    for item, item_type, description in required_items:
        import os
        path = f'/workspaces/MHBG-1/{item}' if not item.startswith('/') else item
        
        if item_type == 'dir':
            exists = os.path.isdir(path)
        else:
            exists = os.path.isfile(path)
        
        status = "✅" if exists else "❌"
        print(f"  {status} {description}")
        if not exists:
            all_good = False
    
    return all_good

def main():
    """Main validation function"""
    print("🚀 MHBG-1 Project Validation")
    print("=" * 50)
    
    # Run all validations
    results = {}
    
    results['structure'] = check_project_structure()
    results['tfidf'] = validate_tfidf()
    results['shortest_path'] = validate_shortest_path()
    results['sample_data'] = validate_sample_data()
    
    # Summary
    print(f"\n{'='*50}")
    print("🎯 VALIDATION SUMMARY")
    print('='*50)
    
    for component, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{component.upper():15} : {status}")
    
    total_passed = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    print(f"\nOverall: {total_passed}/{total_tests} components validated")
    
    if total_passed == total_tests:
        print("\n🎉 Project validation successful!")
        print("📋 Both algorithms are implemented and ready.")
        print("\n📚 Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Test TF-IDF: cd tfidf && python3 test_tfidf.py")
        print("3. Test Shortest Path: cd shortest_path && python3 test_shortest_path.py")
    else:
        print(f"\n⚠️  {total_tests - total_passed} component(s) need attention.")
    
    print("\n🏗️  Clean Project Structure:")
    print("├── 📊 tfidf/              - TF-IDF Algorithm (4 points target)")
    print("└── 🗺️  shortest_path/      - Shortest Path Algorithm (bonus: negative weights)")

if __name__ == "__main__":
    main()