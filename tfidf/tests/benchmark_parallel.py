#!/usr/bin/env python3
"""
Performance Benchmark: Single-threaded vs Multi-process Parallel TF-IDF

This script compares the execution time of single-threaded and multi-process
parallel implementations of TF-IDF analysis on the full newsgroups dataset.

Author: Student Submission
Date: November 2025
"""

import subprocess
import time
import sys
import os
from multiprocessing import cpu_count

def run_command(command):
    """
    Run a shell command and measure execution time.
    
    Args:
        command (str): Command to execute
        
    Returns:
        tuple: (execution_time, success)
    """
    print(f"\n{'='*80}")
    print(f"Running: {command}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=False,
            text=True
        )
        execution_time = time.time() - start_time
        success = True
    except subprocess.CalledProcessError as e:
        execution_time = time.time() - start_time
        print(f"❌ Command failed with exit code {e.returncode}")
        success = False
    
    return execution_time, success

def main():
    """
    Main benchmark function.
    """
    print("="*80)
    print("📊 TF-IDF PERFORMANCE BENCHMARK")
    print("Single-threaded vs Multi-process Parallel Implementation")
    print("="*80)
    print()
    
    # Detect system information
    cores = cpu_count()
    print(f"System Information:")
    print(f"  CPU Cores Available: {cores}")
    print(f"  Python Version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print()
    
    # Check if we're in the correct directory
    if not os.path.exists('run_analysis.py'):
        print("❌ Error: Please run this script from the tfidf/ directory")
        return 1
    
    # Check if full dataset exists
    if not os.path.exists('dataset/newsgroups_full'):
        print("⚠️  Warning: Full dataset not found. This benchmark requires the full dataset.")
        print("   Run: python3 scripts/download_full_newsgroups.py")
        return 1
    
    # Determine which dataset to use based on command-line argument
    dataset = 'full'
    if len(sys.argv) > 1:
        if sys.argv[1] in ['sample', 'full']:
            dataset = sys.argv[1]
        else:
            print("Usage: python benchmark_parallel.py [sample|full]")
            print("  sample: Benchmark on 10-document sample (default: full)")
            print("  full:   Benchmark on 17,901-document full dataset")
            return 1
    
    print(f"Dataset: {dataset}")
    print(f"{'='*80}")
    
    results = {}
    
    # Benchmark 1: Single-threaded version
    print("\n🔹 Test 1: Single-threaded Implementation")
    print("-" * 80)
    time_single, success_single = run_command(f"python3 run_analysis.py {dataset}")
    
    if success_single:
        results['single'] = time_single
        print(f"\n✅ Single-threaded completed in {time_single:.2f} seconds")
    else:
        print("\n❌ Single-threaded version failed")
        return 1
    
    # Benchmark 2: Multi-process parallel version (auto-detect cores)
    print("\n🔹 Test 2: Multi-process Parallel Implementation (Auto-detect cores)")
    print("-" * 80)
    time_parallel_auto, success_parallel = run_command(f"python3 run_analysis_parallel.py {dataset}")
    
    if success_parallel:
        results['parallel_auto'] = time_parallel_auto
        print(f"\n✅ Parallel (auto-detect) completed in {time_parallel_auto:.2f} seconds")
    else:
        print("\n❌ Parallel version failed")
        return 1
    
    # Benchmark 3: Test with different core counts (only if we have multiple cores)
    if cores > 1 and dataset == 'full':
        for num_cores in [1, 2, min(4, cores), cores]:
            if num_cores in results:
                continue  # Skip if already tested
                
            print(f"\n🔹 Test: Multi-process Parallel with {num_cores} core(s)")
            print("-" * 80)
            time_parallel, success = run_command(
                f"python3 run_analysis_parallel.py {dataset} {num_cores}"
            )
            
            if success:
                results[f'parallel_{num_cores}'] = time_parallel
                print(f"\n✅ Parallel ({num_cores} cores) completed in {time_parallel:.2f} seconds")
    
    # Print summary
    print("\n" + "="*80)
    print("📊 BENCHMARK SUMMARY")
    print("="*80)
    print()
    print(f"{'Implementation':<40} {'Time (s)':<15} {'Speedup':<10} {'Efficiency':<10}")
    print("-" * 80)
    
    baseline_time = results['single']
    
    # Sort results for display
    display_order = [
        ('single', 'Single-threaded'),
        ('parallel_auto', f'Multi-process (auto: {cores} cores)'),
    ]
    
    # Add specific core count results
    if cores > 1 and dataset == 'full':
        for num_cores in [1, 2, min(4, cores), cores]:
            key = f'parallel_{num_cores}'
            if key in results and key != 'parallel_auto':
                display_order.append((key, f'Multi-process ({num_cores} core{"s" if num_cores > 1 else ""})'))
    
    for key, label in display_order:
        if key in results:
            exec_time = results[key]
            speedup = baseline_time / exec_time
            
            # Calculate efficiency (speedup / cores used)
            if key == 'single':
                cores_used = 1
            elif key == 'parallel_auto':
                cores_used = cores
            else:
                cores_used = int(key.split('_')[1])
            
            efficiency = speedup / cores_used * 100
            
            print(f"{label:<40} {exec_time:<15.2f} {speedup:<10.2f}x {efficiency:<10.1f}%")
    
    print("-" * 80)
    print()
    
    # Performance insights
    print("📈 PERFORMANCE INSIGHTS:")
    print()
    
    if 'parallel_auto' in results:
        speedup = baseline_time / results['parallel_auto']
        print(f"✅ Parallel processing achieved {speedup:.2f}x speedup using {cores} cores")
        print(f"✅ Time saved: {baseline_time - results['parallel_auto']:.2f} seconds ({(1 - results['parallel_auto']/baseline_time)*100:.1f}%)")
        
        # Calculate ideal vs actual speedup
        ideal_speedup = cores
        efficiency = (speedup / ideal_speedup) * 100
        print(f"✅ Parallel efficiency: {efficiency:.1f}% (ideal: 100%, actual: {speedup:.2f}x of {ideal_speedup}x)")
        
        if efficiency < 50:
            print("⚠️  Low efficiency suggests overhead from process creation and communication")
        elif efficiency < 80:
            print("✅ Good efficiency - parallel processing is beneficial")
        else:
            print("🎉 Excellent efficiency - near-linear speedup!")
    
    print()
    print("💡 RECOMMENDATIONS:")
    print()
    
    if dataset == 'sample':
        print("• Sample dataset (10 docs) is too small to see significant parallel benefits")
        print("• Parallel overhead dominates for small datasets")
        print("• Use single-threaded version for small datasets")
    else:
        if cores >= 4:
            print(f"• Your system has {cores} cores - parallel processing is highly recommended")
            print(f"• Expected speedup: {min(cores * 0.7, cores):.1f}x - {min(cores * 0.9, cores):.1f}x")
        elif cores == 2:
            print("• Your system has 2 cores - parallel processing provides moderate speedup")
            print("• Expected speedup: 1.5x - 1.8x")
        else:
            print("• Your system has 1 core - parallel processing won't help")
            print("• Use single-threaded version")
        
        print(f"• For {dataset} dataset, parallel processing is {'RECOMMENDED' if cores > 1 else 'NOT beneficial'}")
    
    print()
    print("="*80)
    print("✅ BENCHMARK COMPLETE")
    print("="*80)
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
