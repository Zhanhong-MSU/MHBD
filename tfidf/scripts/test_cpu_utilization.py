#!/usr/bin/env python3
"""
CPU Utilization Test for Multi-Process TF-IDF
Tests different chunk sizes and process counts to maximize CPU utilization
"""

import sys
import os
import time
from multiprocessing import Pool, cpu_count

# Add parent directory to path to import run_analysis_parallel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def heavy_computation(args):
    """Simulate heavy computation (tokenization and scoring)."""
    text, index = args
    # Simulate text processing
    words = text.lower().split()
    # Simulate some computation
    result = sum(len(w) for w in words)
    time.sleep(0.001)  # Small delay to simulate I/O
    return (index, result, len(words))

def test_parallel_efficiency(num_docs, num_processes, chunksize):
    """Test parallel processing efficiency."""
    print(f"\n{'='*80}")
    print(f"Testing: {num_docs} documents, {num_processes} processes, chunksize={chunksize}")
    print(f"{'='*80}")
    
    # Generate fake documents
    documents = [f"This is test document number {i} with some text content for processing analysis" * 10 
                 for i in range(num_docs)]
    
    # Sequential processing (baseline)
    print("⏱️  Sequential processing...")
    start = time.time()
    seq_results = [heavy_computation((doc, i)) for i, doc in enumerate(documents)]
    seq_time = time.time() - start
    print(f"   Time: {seq_time:.3f}s")
    
    # Parallel processing
    print(f"⚡ Parallel processing ({num_processes} cores, chunksize={chunksize})...")
    start = time.time()
    with Pool(processes=num_processes) as pool:
        args = [(doc, i) for i, doc in enumerate(documents)]
        par_results = pool.map(heavy_computation, args, chunksize=chunksize)
    par_time = time.time() - start
    print(f"   Time: {par_time:.3f}s")
    
    # Calculate metrics
    speedup = seq_time / par_time
    efficiency = (speedup / num_processes) * 100
    
    print(f"\n📊 Results:")
    print(f"   Speedup: {speedup:.2f}x")
    print(f"   Efficiency: {efficiency:.1f}%")
    print(f"   CPU Utilization: {'🟢 Good' if efficiency > 70 else '🟡 Medium' if efficiency > 50 else '🔴 Poor'}")
    
    return {
        'processes': num_processes,
        'chunksize': chunksize,
        'seq_time': seq_time,
        'par_time': par_time,
        'speedup': speedup,
        'efficiency': efficiency
    }

def main():
    """Run CPU utilization tests."""
    print("="*80)
    print("🔬 CPU UTILIZATION TEST FOR MULTI-PROCESS TF-IDF")
    print("="*80)
    
    cpu_cores = cpu_count()
    print(f"\n💻 System Information:")
    print(f"   CPU Cores Detected: {cpu_cores}")
    print(f"   Python Version: {sys.version.split()[0]}")
    
    # Test parameters
    num_docs = 1000  # Number of fake documents to process
    
    print(f"\n🧪 Test Configuration:")
    print(f"   Documents: {num_docs}")
    print(f"   Task: Tokenization + word counting")
    
    # Test different configurations
    results = []
    
    print("\n" + "="*80)
    print("TESTING DIFFERENT CONFIGURATIONS")
    print("="*80)
    
    # Test 1: Use all cores with auto chunksize (default)
    results.append(test_parallel_efficiency(
        num_docs=num_docs,
        num_processes=cpu_cores,
        chunksize=max(1, num_docs // (cpu_cores * 4))
    ))
    
    # Test 2: Use all cores with smaller chunks (better distribution)
    results.append(test_parallel_efficiency(
        num_docs=num_docs,
        num_processes=cpu_cores,
        chunksize=max(1, num_docs // (cpu_cores * 8))
    ))
    
    # Test 3: Use all cores with very small chunks (maximum distribution)
    results.append(test_parallel_efficiency(
        num_docs=num_docs,
        num_processes=cpu_cores,
        chunksize=1
    ))
    
    if cpu_cores >= 4:
        # Test 4: Use half cores (for comparison)
        results.append(test_parallel_efficiency(
            num_docs=num_docs,
            num_processes=cpu_cores // 2,
            chunksize=max(1, num_docs // (cpu_cores * 2))
        ))
    
    # Summary
    print("\n" + "="*80)
    print("📈 PERFORMANCE SUMMARY")
    print("="*80)
    print(f"{'Config':<20} {'Processes':<10} {'Chunk':<8} {'Time':<10} {'Speedup':<10} {'Efficiency':<12}")
    print("-"*80)
    
    for i, r in enumerate(results, 1):
        config = f"Test {i}"
        print(f"{config:<20} {r['processes']:<10} {r['chunksize']:<8} {r['par_time']:<10.3f} "
              f"{r['speedup']:<10.2f}x {r['efficiency']:<11.1f}%")
    
    print("-"*80)
    
    # Find best configuration
    best = max(results, key=lambda x: x['efficiency'])
    print(f"\n🏆 Best Configuration:")
    print(f"   Processes: {best['processes']}")
    print(f"   Chunk Size: {best['chunksize']}")
    print(f"   Efficiency: {best['efficiency']:.1f}%")
    print(f"   Speedup: {best['speedup']:.2f}x")
    
    print("\n💡 Recommendations:")
    if best['efficiency'] > 80:
        print("   ✅ Excellent CPU utilization! Current configuration is optimal.")
    elif best['efficiency'] > 60:
        print("   ✅ Good CPU utilization. Configuration is working well.")
    elif best['efficiency'] > 40:
        print("   ⚠️  Moderate CPU utilization. Consider:")
        print("      • Using smaller chunk sizes for better load balancing")
        print("      • Increasing workload per task to reduce overhead")
    else:
        print("   ⚠️  Low CPU utilization. Issues:")
        print("      • Tasks may be too small (overhead dominates)")
        print("      • I/O bottleneck (disk/memory limited)")
        print("      • Python GIL limitations (if using threads instead of processes)")
    
    if cpu_cores > 4:
        print(f"\n   For {cpu_cores}-core system processing large datasets:")
        print(f"   • Recommended processes: {cpu_cores}")
        print(f"   • Recommended chunk size: {max(1, num_docs // (cpu_cores * 8))} for {num_docs} documents")
        print(f"   • For 17,901 documents: chunk size = {max(1, 17901 // (cpu_cores * 8))}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
