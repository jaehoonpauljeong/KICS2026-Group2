"""
Comprehensive Benchmarking and Testing Suite for I2NSF Security Policy System
Runs actual tests on generate.py and collects real performance metrics
"""

import subprocess
import time
import json
import os
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import traceback
from typing import Dict, List, Tuple
import pandas as pd

# Set style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

# Create directories
os.makedirs('benchmark_results', exist_ok=True)
os.makedirs('benchmark_plots', exist_ok=True)

# ============================================================================
# Test Case Definitions
# ============================================================================

TEST_CASES = {
    'simple': [
        "Block all traffic from China",
        "Allow HTTP traffic",
        "Drop all ICMP packets",
        "Block port 22",
        "Allow traffic to 192.168.1.1",
    ],
    'medium': [
        "Block SNS access from Buenos Aires to Seoul during office hours",
        "Mitigate DDoS attacks on web servers with threshold 1000 packets per second",
        "Block malicious VoIP packets coming to the company",
        "Allow HTTP and HTTPS traffic from trusted network 10.0.0.0/8 during weekdays",
        "Block all traffic from Russia and China to US servers between 9 AM and 5 PM",
    ],
    'complex': [
        "Create a policy that blocks social media access from Mexico City and Buenos Aires to corporate servers in Seoul and Tokyo during business hours (9 AM to 6 PM) on weekdays, but allows access on weekends",
        "Implement DDoS mitigation for web servers in New York with rate limiting of 5000 packets per second, mirror suspicious traffic to monitoring server, and block sources that exceed threshold for more than 30 seconds",
        "Block VoIP calls from known malicious SIP addresses, allow internal company VoIP between 192.168.0.0/16 networks, rate limit external VoIP to 100 concurrent calls, and log all rejected attempts",
        "Create multi-layer security policy that blocks malware signatures, filters URLs from blacklist, applies geographic restrictions for traffic from high-risk countries, and implements time-based access control for remote workers",
        "Establish policy for remote work: allow VPN access from approved countries (US, Canada, UK, Germany, Japan) during extended hours (6 AM to 10 PM), require MFA for access outside business hours, block all other remote access attempts, and log all connection attempts",
    ],
    'geographic': [
        "Block all traffic from North Korea",
        "Allow traffic only from United States and Canada",
        "Block traffic from China, Russia, and Iran to government servers",
        "Create policy that allows European traffic but blocks Asian traffic during US night time",
        "Block traffic from high-risk countries: Syria, Iran, North Korea, and Russia",
    ],
    'time_based': [
        "Block social media during work hours Monday to Friday",
        "Allow remote access only between 6 AM and 11 PM",
        "Block gaming websites during weekdays but allow on weekends",
        "Rate limit non-essential traffic during peak hours 9 AM to 5 PM",
        "Block all external access outside business hours except for specific IPs",
    ],
    'application': [
        "Block all social media applications",
        "Allow only HTTP, HTTPS, and DNS traffic",
        "Block peer-to-peer file sharing applications",
        "Allow Microsoft Teams and Zoom but block Skype",
        "Block streaming services like Netflix, YouTube, and Spotify during work hours",
    ],
    'ddos': [
        "Mitigate SYN flood attacks with threshold 10000 packets per second",
        "Block UDP flood attacks exceeding 50000 packets per second",
        "Rate limit ICMP traffic to 1000 packets per second",
        "Implement progressive rate limiting: 5000 pps normal, 10000 pps warning, block above",
        "Create DDoS mitigation policy with dynamic thresholds based on baseline traffic patterns",
    ],
    'edge_cases': [
        "Block everything",
        "Allow everything",
        "Create policy with no time restrictions",
        "Block traffic from 300 different countries",  # Invalid - should fail gracefully
        "Allow traffic on port 99999",  # Invalid port
    ],
}

# ============================================================================
# Benchmark Runner
# ============================================================================

class BenchmarkRunner:
    def __init__(self):
        self.results = []
        self.errors = []
        self.validation_results = []
        
    def run_single_test(self, test_case: str, category: str) -> Dict:
        """Run a single test case and collect metrics"""
        print(f"  Testing: {test_case[:60]}...")
        
        result = {
            'test_case': test_case,
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'time_taken': 0,
            'validation_passed': False,
            'error': None,
            'xml_length': 0,
        }
        
        start_time = time.time()
        
        try:
            # Run generate.py with the test case
            process = subprocess.run(
                ['python', 'generate.py', test_case],
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            end_time = time.time()
            result['time_taken'] = end_time - start_time
            
            # Check if process succeeded
            if process.returncode == 0:
                result['success'] = True
                
                # Check if XML was generated
                if os.path.exists('generated_policy.xml'):
                    with open('generated_policy.xml', 'r') as f:
                        xml_content = f.read()
                        result['xml_length'] = len(xml_content)
                    
                    # Run validation
                    result['validation_passed'] = self.validate_xml()
                else:
                    result['error'] = "XML file not generated"
            else:
                result['error'] = f"Process failed with code {process.returncode}"
                if process.stderr:
                    result['error'] += f": {process.stderr[:200]}"
                    
        except subprocess.TimeoutExpired:
            result['error'] = "Timeout (>120s)"
            result['time_taken'] = 120
        except Exception as e:
            result['error'] = str(e)
            result['time_taken'] = time.time() - start_time
        
        return result
    
    def validate_xml(self) -> bool:
        """Validate generated XML against schema"""
        try:
            process = subprocess.run(
                ['python', 'validate.py'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return 'VALID' in process.stdout
        except:
            return False
    
    def run_all_tests(self):
        """Run all test cases"""
        print("=" * 80)
        print("STARTING COMPREHENSIVE BENCHMARK")
        print("=" * 80)
        print()
        
        total_tests = sum(len(cases) for cases in TEST_CASES.values())
        current_test = 0
        
        for category, test_cases in TEST_CASES.items():
            print(f"\n{'=' * 80}")
            print(f"Category: {category.upper()} ({len(test_cases)} tests)")
            print(f"{'=' * 80}")
            
            for test_case in test_cases:
                current_test += 1
                print(f"\n[{current_test}/{total_tests}] ", end="")
                
                result = self.run_single_test(test_case, category)
                self.results.append(result)
                
                # Print result
                status = "✓ PASS" if result['success'] else "✗ FAIL"
                validation = "✓" if result['validation_passed'] else "✗"
                print(f"  {status} | Validation: {validation} | Time: {result['time_taken']:.2f}s")
                
                if result['error']:
                    print(f"  Error: {result['error']}")
                    self.errors.append(result)
                
                # Small delay to avoid overwhelming the API
                time.sleep(1)
        
        print("\n" + "=" * 80)
        print("BENCHMARK COMPLETE")
        print("=" * 80)
        self.save_results()
    
    def save_results(self):
        """Save results to JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        with open(f'benchmark_results/results_{timestamp}.json', 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save summary
        summary = self.generate_summary()
        with open(f'benchmark_results/summary_{timestamp}.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✓ Results saved to benchmark_results/results_{timestamp}.json")
        print(f"✓ Summary saved to benchmark_results/summary_{timestamp}.json")
    
    def generate_summary(self) -> Dict:
        """Generate summary statistics"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        validated = sum(1 for r in self.results if r['validation_passed'])
        
        times = [r['time_taken'] for r in self.results if r['success']]
        
        summary = {
            'total_tests': total,
            'successful': successful,
            'failed': total - successful,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'validated': validated,
            'validation_rate': (validated / total * 100) if total > 0 else 0,
            'avg_time': np.mean(times) if times else 0,
            'median_time': np.median(times) if times else 0,
            'min_time': np.min(times) if times else 0,
            'max_time': np.max(times) if times else 0,
            'std_time': np.std(times) if times else 0,
            'by_category': {}
        }
        
        # Per-category statistics
        for category in TEST_CASES.keys():
            cat_results = [r for r in self.results if r['category'] == category]
            cat_success = sum(1 for r in cat_results if r['success'])
            cat_validated = sum(1 for r in cat_results if r['validation_passed'])
            cat_times = [r['time_taken'] for r in cat_results if r['success']]
            
            summary['by_category'][category] = {
                'total': len(cat_results),
                'successful': cat_success,
                'success_rate': (cat_success / len(cat_results) * 100) if cat_results else 0,
                'validated': cat_validated,
                'validation_rate': (cat_validated / len(cat_results) * 100) if cat_results else 0,
                'avg_time': np.mean(cat_times) if cat_times else 0,
            }
        
        return summary

# ============================================================================
# Visualization Functions
# ============================================================================

def plot_results(results: List[Dict]):
    """Generate all plots from benchmark results"""
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    df = pd.DataFrame(results)
    
    # Figure 1: Success Rate by Category
    plot_success_rate_by_category(df)
    
    # Figure 2: Processing Time Distribution
    plot_time_distribution(df)
    
    # Figure 3: Time by Category
    plot_time_by_category(df)
    
    # Figure 4: Validation Results
    plot_validation_results(df)
    
    # Figure 5: Success vs Time Scatter
    plot_success_vs_time(df)
    
    # Figure 6: Error Analysis
    plot_error_analysis(df)
    
    # Figure 7: Complexity Analysis
    plot_complexity_analysis(df)
    
    # Figure 8: Performance Summary Dashboard
    plot_performance_dashboard(df)
    
    print("\n✓ All plots saved to benchmark_plots/")

def plot_success_rate_by_category(df):
    """Plot success rate by category"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    category_stats = df.groupby('category').agg({
        'success': ['sum', 'count', 'mean'],
        'validation_passed': 'sum'
    }).reset_index()
    
    categories = category_stats['category']
    success_rates = category_stats[('success', 'mean')] * 100
    validation_rates = (category_stats[('validation_passed', 'sum')] / 
                       category_stats[('success', 'count')]) * 100
    
    x = np.arange(len(categories))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, success_rates, width, label='Success Rate', 
                   color='#3498DB', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, validation_rates, width, label='Validation Rate', 
                   color='#27AE60', alpha=0.8, edgecolor='black', linewidth=1.5)
    
    ax.set_xlabel('Category', fontweight='bold', fontsize=12)
    ax.set_ylabel('Rate (%)', fontweight='bold', fontsize=12)
    ax.set_title('Success and Validation Rates by Category', fontweight='bold', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 105)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('benchmark_plots/1_success_rate_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 1: Success rate by category")

def plot_time_distribution(df):
    """Plot processing time distribution"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    successful_times = df[df['success']]['time_taken']
    
    # Histogram
    ax1.hist(successful_times, bins=30, color='#3498DB', alpha=0.7, edgecolor='black')
    ax1.axvline(successful_times.mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {successful_times.mean():.2f}s')
    ax1.axvline(successful_times.median(), color='orange', linestyle='--', 
                linewidth=2, label=f'Median: {successful_times.median():.2f}s')
    ax1.set_xlabel('Processing Time (seconds)', fontweight='bold')
    ax1.set_ylabel('Frequency', fontweight='bold')
    ax1.set_title('Processing Time Distribution', fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Box plot
    ax2.boxplot([successful_times], labels=['All Tests'], vert=True)
    ax2.set_ylabel('Processing Time (seconds)', fontweight='bold')
    ax2.set_title('Processing Time Box Plot', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add statistics text
    stats_text = f"""
    Mean: {successful_times.mean():.2f}s
    Median: {successful_times.median():.2f}s
    Std Dev: {successful_times.std():.2f}s
    Min: {successful_times.min():.2f}s
    Max: {successful_times.max():.2f}s
    95th %ile: {successful_times.quantile(0.95):.2f}s
    """
    ax2.text(1.3, successful_times.median(), stats_text, 
            fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('benchmark_plots/2_time_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 2: Time distribution")

def plot_time_by_category(df):
    """Plot processing time by category"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    successful_df = df[df['success']]
    categories = successful_df['category'].unique()
    
    data_to_plot = [successful_df[successful_df['category'] == cat]['time_taken'].values 
                    for cat in categories]
    
    bp = ax.boxplot(data_to_plot, labels=categories, patch_artist=True)
    
    # Color boxes
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_xlabel('Category', fontweight='bold', fontsize=12)
    ax.set_ylabel('Processing Time (seconds)', fontweight='bold', fontsize=12)
    ax.set_title('Processing Time by Category', fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('benchmark_plots/3_time_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 3: Time by category")

def plot_validation_results(df):
    """Plot validation results"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Overall validation
    validation_counts = df['validation_passed'].value_counts()
    colors = ['#27AE60', '#E74C3C']
    labels = ['Valid', 'Invalid']
    
    wedges, texts, autotexts = ax1.pie([validation_counts.get(True, 0), 
                                         validation_counts.get(False, 0)],
                                        labels=labels,
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax1.set_title('Overall Validation Results', fontweight='bold', fontsize=14)
    
    # Validation by category
    category_validation = df.groupby('category')['validation_passed'].agg(['sum', 'count'])
    category_validation['rate'] = (category_validation['sum'] / category_validation['count']) * 100
    
    categories = category_validation.index
    rates = category_validation['rate']
    
    bars = ax2.bar(categories, rates, color='#27AE60', alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Category', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Validation Rate (%)', fontweight='bold', fontsize=12)
    ax2.set_title('Validation Rate by Category', fontweight='bold', fontsize=14)
    ax2.set_ylim(0, 105)
    ax2.grid(axis='y', alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', 
                fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('benchmark_plots/4_validation_results.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 4: Validation results")

def plot_success_vs_time(df):
    """Scatter plot of success vs time"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    successful = df[df['success']]
    failed = df[~df['success']]
    
    ax.scatter(range(len(successful)), successful['time_taken'], 
              c='#27AE60', alpha=0.6, s=100, label='Successful', edgecolors='black')
    ax.scatter(range(len(successful), len(successful) + len(failed)), failed['time_taken'], 
              c='#E74C3C', alpha=0.6, s=100, label='Failed', marker='x', linewidths=2)
    
    ax.set_xlabel('Test Number', fontweight='bold', fontsize=12)
    ax.set_ylabel('Processing Time (seconds)', fontweight='bold', fontsize=12)
    ax.set_title('Test Results: Success vs Failure Over Time', fontweight='bold', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Add average line
    if len(successful) > 0:
        ax.axhline(successful['time_taken'].mean(), color='green', 
                  linestyle='--', alpha=0.5, label=f'Avg Success: {successful["time_taken"].mean():.2f}s')
    
    plt.tight_layout()
    plt.savefig('benchmark_plots/5_success_vs_time.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 5: Success vs time scatter")

def plot_error_analysis(df):
    """Analyze and plot errors"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    failed = df[~df['success']]
    
    if len(failed) == 0:
        ax.text(0.5, 0.5, 'No Errors Detected!\n100% Success Rate', 
               ha='center', va='center', fontsize=20, fontweight='bold', color='green')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
    else:
        error_categories = failed.groupby('category').size()
        
        bars = ax.barh(error_categories.index, error_categories.values, 
                      color='#E74C3C', alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_xlabel('Number of Errors', fontweight='bold', fontsize=12)
        ax.set_ylabel('Category', fontweight='bold', fontsize=12)
        ax.set_title(f'Error Distribution by Category (Total: {len(failed)} errors)', 
                    fontweight='bold', fontsize=14)
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, error_categories.values)):
            ax.text(val + 0.1, i, str(val), 
                   va='center', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('benchmark_plots/6_error_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 6: Error analysis")

def plot_complexity_analysis(df):
    """Analyze performance by complexity"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Map categories to complexity
    complexity_map = {
        'simple': 1,
        'medium': 2,
        'complex': 3,
        'geographic': 2,
        'time_based': 2,
        'application': 2,
        'ddos': 2,
        'edge_cases': 1
    }
    
    df['complexity'] = df['category'].map(complexity_map)
    
    # Plot 1: Success rate by complexity
    ax1 = axes[0, 0]
    complexity_success = df.groupby('complexity')['success'].agg(['sum', 'count', 'mean'])
    complexity_labels = ['Simple', 'Medium', 'Complex']
    
    bars = ax1.bar(complexity_labels, complexity_success['mean'] * 100, 
                   color=['#A8E6CF', '#FFD3B6', '#FFAAA5'], alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Success Rate (%)', fontweight='bold')
    ax1.set_title('Success Rate by Complexity', fontweight='bold')
    ax1.set_ylim(0, 105)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Plot 2: Time by complexity
    ax2 = axes[0, 1]
    successful_df = df[df['success']]
    data_to_plot = [successful_df[successful_df['complexity'] == i]['time_taken'].values 
                    for i in [1, 2, 3]]
    
    bp = ax2.boxplot(data_to_plot, labels=complexity_labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], ['#A8E6CF', '#FFD3B6', '#FFAAA5']):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Processing Time (seconds)', fontweight='bold')
    ax2.set_title('Processing Time by Complexity', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Plot 3: XML length by complexity
    ax3 = axes[1, 0]
    xml_by_complexity = successful_df.groupby('complexity')['xml_length'].mean()
    
    bars = ax3.bar(complexity_labels, xml_by_complexity, 
                   color=['#A8E6CF', '#FFD3B6', '#FFAAA5'], alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Average XML Length (chars)', fontweight='bold')
    ax3.set_title('Generated XML Length by Complexity', fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Plot 4: Correlation scatter
    ax4 = axes[1, 1]
    colors_scatter = {1: '#A8E6CF', 2: '#FFD3B6', 3: '#FFAAA5'}
    for complexity in [1, 2, 3]:
        data = successful_df[successful_df['complexity'] == complexity]
        ax4.scatter(data['xml_length'], data['time_taken'], 
                   c=colors_scatter[complexity], label=complexity_labels[complexity-1],
                   alpha=0.6, s=100, edgecolors='black')
    
    ax4.set_xlabel('XML Length (chars)', fontweight='bold')
    ax4.set_ylabel('Processing Time (seconds)', fontweight='bold')
    ax4.set_title('XML Length vs Processing Time', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle('Complexity Analysis', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig('benchmark_plots/7_complexity_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 7: Complexity analysis")

def plot_performance_dashboard(df):
    """Create comprehensive performance dashboard"""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Calculate statistics
    total_tests = len(df)
    successful = df['success'].sum()
    validated = df['validation_passed'].sum()
    avg_time = df[df['success']]['time_taken'].mean()
    
    # Title box
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis('off')
    ax_title.text(0.5, 0.6, 'I2NSF Policy Generation System', 
                 ha='center', va='center', fontsize=24, fontweight='bold')
    ax_title.text(0.5, 0.3, 'Comprehensive Benchmark Results', 
                 ha='center', va='center', fontsize=18, style='italic')
    
    # Stats boxes
    ax_stats1 = fig.add_subplot(gs[1, 0])
    ax_stats1.axis('off')
    ax_stats1.text(0.5, 0.7, f'{total_tests}', ha='center', va='center', 
                  fontsize=48, fontweight='bold', color='#3498DB')
    ax_stats1.text(0.5, 0.3, 'Total Tests', ha='center', va='center', 
                  fontsize=14, fontweight='bold')
    
    ax_stats2 = fig.add_subplot(gs[1, 1])
    ax_stats2.axis('off')
    success_rate = (successful / total_tests * 100) if total_tests > 0 else 0
    ax_stats2.text(0.5, 0.7, f'{success_rate:.1f}%', ha='center', va='center', 
                  fontsize=48, fontweight='bold', color='#27AE60')
    ax_stats2.text(0.5, 0.3, 'Success Rate', ha='center', va='center', 
                  fontsize=14, fontweight='bold')
    
    ax_stats3 = fig.add_subplot(gs[1, 2])
    ax_stats3.axis('off')
    ax_stats3.text(0.5, 0.7, f'{avg_time:.2f}s', ha='center', va='center', 
                  fontsize=48, fontweight='bold', color='#F39C12')
    ax_stats3.text(0.5, 0.3, 'Avg Time', ha='center', va='center', 
                  fontsize=14, fontweight='bold')
    
    # Category performance
    ax_cat = fig.add_subplot(gs[2, :])
    category_stats = df.groupby('category').agg({
        'success': 'mean',
        'validation_passed': 'sum',
        'time_taken': 'mean'
    }).reset_index()
    
    categories = category_stats['category']
    x = np.arange(len(categories))
    width = 0.25
    
    bars1 = ax_cat.bar(x - width, category_stats['success'] * 100, width, 
                      label='Success Rate (%)', color='#3498DB', alpha=0.8)
    bars2 = ax_cat.bar(x, (category_stats['validation_passed'] / 
                          df.groupby('category').size()) * 100, width,
                      label='Validation Rate (%)', color='#27AE60', alpha=0.8)
    
    ax_cat_twin = ax_cat.twinx()
    line = ax_cat_twin.plot(x + width, category_stats['time_taken'], 'ro-',
                           linewidth=2, markersize=8, label='Avg Time (s)')
    
    ax_cat.set_xlabel('Category', fontweight='bold', fontsize=12)
    ax_cat.set_ylabel('Rate (%)', fontweight='bold', fontsize=12)
    ax_cat_twin.set_ylabel('Time (seconds)', fontweight='bold', fontsize=12)
    ax_cat.set_title('Performance by Category', fontweight='bold', fontsize=14)
    ax_cat.set_xticks(x)
    ax_cat.set_xticklabels(categories, rotation=45, ha='right')
    ax_cat.legend(loc='upper left')
    ax_cat_twin.legend(loc='upper right')
    ax_cat.grid(axis='y', alpha=0.3)
    
    plt.savefig('benchmark_plots/8_performance_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 8: Performance dashboard")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("I2NSF SECURITY POLICY GENERATION SYSTEM")
    print("COMPREHENSIVE BENCHMARK AND TEST SUITE")
    print("=" * 80)
    print()
    
    # Check if generate.py exists
    if not os.path.exists('generate.py'):
        print("ERROR: generate.py not found in current directory!")
        print("Please run this script from the llm_backend directory.")
        sys.exit(1)
    
    # Display test plan
    total_tests = sum(len(cases) for cases in TEST_CASES.values())
    print(f"Test Plan:")
    print(f"  Total test cases: {total_tests}")
    for category, cases in TEST_CASES.items():
        print(f"    - {category}: {len(cases)} tests")
    
    print(f"\nEstimated time: {total_tests * 10 / 60:.1f} - {total_tests * 15 / 60:.1f} minutes")
    print()
    
    response = input("Start benchmark? (y/n): ")
    if response.lower() != 'y':
        print("Benchmark cancelled.")
        sys.exit(0)
    
    # Run benchmark
    runner = BenchmarkRunner()
    runner.run_all_tests()
    
    # Print summary
    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)
    
    summary = runner.generate_summary()
    print(f"\nOverall Statistics:")
    print(f"  Total Tests: {summary['total_tests']}")
    print(f"  Successful: {summary['successful']} ({summary['success_rate']:.1f}%)")
    print(f"  Failed: {summary['failed']}")
    print(f"  Validated: {summary['validated']} ({summary['validation_rate']:.1f}%)")
    print(f"\nTiming Statistics:")
    print(f"  Average: {summary['avg_time']:.2f}s")
    print(f"  Median: {summary['median_time']:.2f}s")
    print(f"  Min: {summary['min_time']:.2f}s")
    print(f"  Max: {summary['max_time']:.2f}s")
    print(f"  Std Dev: {summary['std_time']:.2f}s")
    
    print(f"\nBy Category:")
    for category, stats in summary['by_category'].items():
        print(f"  {category}:")
        print(f"    Success: {stats['successful']}/{stats['total']} ({stats['success_rate']:.1f}%)")
        print(f"    Validated: {stats['validated']}/{stats['total']} ({stats['validation_rate']:.1f}%)")
        print(f"    Avg Time: {stats['avg_time']:.2f}s")
    
    # Generate plots
    plot_results(runner.results)
    
    print("\n" + "=" * 80)
    print("✓ BENCHMARK COMPLETE")
    print("=" * 80)
    print(f"\nResults saved to: benchmark_results/")
    print(f"Plots saved to: benchmark_plots/")
    print()

if __name__ == "__main__":
    main()