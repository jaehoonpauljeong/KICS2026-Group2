"""
Enhanced Comprehensive Benchmarking Suite for I2NSF Security Policy System
140 total tests with better distribution and realistic complexity levels
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
# Enhanced Test Case Definitions - 140 Total Tests
# ============================================================================

TEST_CASES = {
    # SIMPLE POLICIES - 30 tests (straightforward, single-condition policies)
    'simple_firewall': [
        "Block all traffic from China",
        "Allow HTTP traffic",
        "Drop all ICMP packets",
        "Block port 22",
        "Allow traffic to 192.168.1.1",
        "Block port 3389",
        "Allow SSH from trusted network",
        "Drop UDP port 53 from external",
        "Block FTP traffic",
        "Allow HTTPS only",
        "Block telnet port 23",
        "Allow traffic from 10.0.0.0/8",
        "Drop all packets from 0.0.0.0",
        "Block SMTP port 25",
        "Allow DNS queries",
    ],
    
    'simple_geographic': [
        "Block all traffic from North Korea",
        "Allow traffic only from United States",
        "Block traffic from Russia",
        "Allow traffic from Canada",
        "Block traffic from Iran",
        "Allow traffic from United Kingdom",
        "Block traffic from Syria",
        "Allow traffic from Germany",
        "Block traffic from Cuba",
        "Allow traffic from Japan",
        "Block traffic from Belarus",
        "Allow traffic from France",
        "Block traffic from Venezuela",
        "Allow traffic from Australia",
        "Block traffic from Sudan",
    ],
    
    # MEDIUM COMPLEXITY - 50 tests (2-3 conditions, realistic business policies)
    'medium_time_based': [
        "Block social media during work hours Monday to Friday",
        "Allow remote access only between 6 AM and 11 PM",
        "Block gaming websites during weekdays",
        "Allow VPN access during business hours only",
        "Block streaming during office hours 9 AM to 5 PM",
        "Allow database access only during maintenance window 2 AM to 4 AM",
        "Block downloads during peak hours 9 AM to 12 PM",
        "Allow admin access only during work hours",
        "Block external email after 6 PM",
        "Allow file transfers only during off-peak hours",
    ],
    
    'medium_application': [
        "Block all social media applications",
        "Allow only HTTP and HTTPS traffic",
        "Block peer-to-peer file sharing",
        "Allow Microsoft Teams but block Skype",
        "Block streaming services during work hours",
        "Allow email protocols SMTP, POP3, IMAP",
        "Block BitTorrent traffic",
        "Allow Zoom and Google Meet only",
        "Block IRC and chat protocols",
        "Allow Slack and Discord for work",
    ],
    
    'medium_ddos': [
        "Mitigate SYN flood with threshold 10000 packets per second",
        "Block UDP flood exceeding 50000 packets per second",
        "Rate limit ICMP to 1000 packets per second",
        "Block HTTP flood over 5000 requests per second",
        "Limit DNS queries to 2000 per second",
        "Block ping flood over 500 per second",
        "Rate limit TCP connections to 10000 per second",
        "Block NTP amplification attacks",
        "Limit HTTPS requests to 3000 per second",
        "Block SSDP reflection attacks",
    ],
    
    'medium_mixed': [
        "Block SNS from Buenos Aires during office hours",
        "Allow HTTP from trusted network during weekdays",
        "Block malicious VoIP packets to company",
        "Rate limit external traffic during peak hours",
        "Allow remote desktop from US and Canada only",
        "Block file downloads from China and Russia",
        "Allow email from known domains only",
        "Block video streaming from external networks",
        "Allow database access from office IPs only",
        "Block FTP from untrusted countries",
        "Allow web traffic from employees during work hours",
        "Block P2P from guest network",
        "Allow SSH from admin IPs only",
        "Block SMTP relay from external sources",
        "Allow API access from verified clients",
        "Block telnet from all sources",
        "Allow RDP from VPN users only",
        "Block IRC from corporate network",
        "Allow Git operations during work hours",
        "Block torrent traffic from all users",
    ],
    
    # MODERATE COMPLEXITY - 40 tests (3-4 conditions, multi-layer policies)
    'moderate_geographic_time': [
        "Block traffic from China to US servers between 9 AM and 5 PM",
        "Allow European traffic during EU business hours only",
        "Block Asian traffic to US during night time",
        "Allow traffic from UK during London office hours",
        "Block traffic from Russia to government servers during weekdays",
        "Allow Canadian access during North American business hours",
        "Block Middle East traffic during peak hours",
        "Allow Australian traffic during Sydney office hours",
        "Block South American traffic during US night time",
        "Allow Japanese traffic during Tokyo business hours",
    ],
    
    'moderate_application_geo': [
        "Block social media from Mexico and Argentina",
        "Allow Microsoft 365 from approved countries only",
        "Block streaming services from high-bandwidth countries",
        "Allow Salesforce access from US and Europe only",
        "Block gaming from office locations during work hours",
        "Allow Slack from company offices worldwide",
        "Block YouTube from guest networks in all locations",
        "Allow AWS access from approved regions only",
        "Block Dropbox from China and Russia",
        "Allow GitHub from developer locations only",
    ],
    
    'moderate_security': [
        "Block suspicious traffic and log all attempts",
        "Allow HTTPS with valid certificates only",
        "Block known malware signatures and IPs",
        "Allow authenticated users with MFA only",
        "Block brute force attempts over 5 per minute",
        "Allow encrypted traffic from trusted sources",
        "Block unsigned executables from downloads",
        "Allow verified API keys only",
        "Block SQL injection patterns",
        "Allow whitelisted user agents only",
    ],
    
    'moderate_rate_limiting': [
        "Rate limit API calls to 100 per minute per user",
        "Block traffic exceeding 1GB per hour",
        "Limit login attempts to 3 per 5 minutes",
        "Rate limit downloads to 10MB per second",
        "Block users exceeding 1000 requests per hour",
        "Limit email sending to 50 per hour",
        "Rate limit database queries to 500 per minute",
        "Block file uploads over 100MB",
        "Limit concurrent connections to 50 per user",
        "Rate limit search queries to 10 per minute",
    ],
    
    # COMPLEX POLICIES - 20 tests (5+ conditions, enterprise-level)
    'complex_multi_layer': [
        "Block social media from Mexico City to Seoul during business hours on weekdays",
        "Allow VPN from approved countries with MFA during extended hours",
        "Block streaming from guest network during peak hours with exceptions for executives",
        "Allow remote access from specific IPs during business hours with rate limiting",
        "Block downloads over 100MB from untrusted sources during work hours",
    ],
    
    'complex_security': [
        "Implement multi-layer DDoS mitigation with progressive rate limiting",
        "Block traffic with malware signatures and suspicious patterns",
        "Allow authenticated users with valid certificates during approved hours",
        "Block brute force with intelligent detection and temporary bans",
        "Implement zero-trust policy with continuous verification",
    ],
    
    'complex_enterprise': [
        "Create tiered access policy for employees, contractors, and guests",
        "Implement geographic restrictions with time zones and holidays",
        "Block high-risk activities with exceptions for approved users",
        "Allow mission-critical applications with failover and redundancy",
        "Create compliance policy for GDPR and HIPAA requirements",
    ],
    
    'complex_advanced': [
        "Implement adaptive rate limiting based on user behavior patterns",
        "Create policy with automatic threat response and mitigation",
        "Block anomalous traffic patterns using behavioral analysis",
        "Allow conditional access based on device posture and location",
        "Implement intelligent routing with load balancing and QoS",
    ],
}

# ============================================================================
# Benchmark Runner with Improvements
# ============================================================================

class EnhancedBenchmarkRunner:
    def __init__(self, timeout=180):
        self.results = []
        self.errors = []
        self.timeout = timeout  # Increased default timeout
        
    def run_single_test(self, test_case: str, category: str, test_num: int, total: int) -> Dict:
        """Run a single test case and collect metrics"""
        print(f"[{test_num}/{total}] {category}: {test_case[:50]}...")
        
        result = {
            'test_case': test_case,
            'category': category,
            'test_number': test_num,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'time_taken': 0,
            'validation_passed': False,
            'error': None,
            'xml_length': 0,
            'timeout_occurred': False,
        }
        
        start_time = time.time()
        
        try:
            # Run generate.py with the test case
            process = subprocess.run(
                ['python', 'generate.py', test_case],
                capture_output=True,
                text=True,
                timeout=self.timeout
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
                    
                    # Archive the generated policy
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    archive_path = f'benchmark_results/policy_{test_num}_{timestamp}.xml'
                    with open(archive_path, 'w') as f:
                        f.write(xml_content)
                else:
                    result['error'] = "XML file not generated"
            else:
                result['error'] = f"Process failed with code {process.returncode}"
                if process.stderr:
                    result['error'] += f": {process.stderr[:200]}"
                    
        except subprocess.TimeoutExpired:
            result['error'] = f"Timeout (>{self.timeout}s)"
            result['time_taken'] = self.timeout
            result['timeout_occurred'] = True
        except Exception as e:
            result['error'] = str(e)
            result['time_taken'] = time.time() - start_time
        
        # Print result
        status = "✓" if result['success'] else "✗"
        validation = "✓" if result['validation_passed'] else "✗"
        timeout_marker = " [TIMEOUT]" if result['timeout_occurred'] else ""
        print(f"  {status} Success | {validation} Valid | {result['time_taken']:.1f}s{timeout_marker}")
        
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
        print("ENHANCED COMPREHENSIVE BENCHMARK - 140 TESTS")
        print("=" * 80)
        print()
        
        # Calculate totals
        total_tests = sum(len(cases) for cases in TEST_CASES.values())
        current_test = 0
        
        print(f"Total Test Cases: {total_tests}")
        print(f"Timeout per test: {self.timeout}s")
        print(f"Estimated time: {total_tests * 60 / 60:.0f} - {total_tests * 90 / 60:.0f} minutes")
        print()
        
        # Category distribution
        print("Test Distribution:")
        for category, cases in TEST_CASES.items():
            print(f"  {category}: {len(cases)} tests")
        print()
        
        start_overall = time.time()
        
        for category, test_cases in TEST_CASES.items():
            print(f"\n{'=' * 80}")
            print(f"Category: {category.upper().replace('_', ' ')} ({len(test_cases)} tests)")
            print(f"{'=' * 80}\n")
            
            for test_case in test_cases:
                current_test += 1
                result = self.run_single_test(test_case, category, current_test, total_tests)
                self.results.append(result)
                
                if result['error']:
                    self.errors.append(result)
                
                # Small delay to avoid overwhelming the API
                time.sleep(2)
        
        end_overall = time.time()
        total_time = end_overall - start_overall
        
        print("\n" + "=" * 80)
        print("BENCHMARK COMPLETE")
        print("=" * 80)
        print(f"Total time: {total_time / 60:.1f} minutes")
        
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
        """Generate comprehensive summary statistics"""
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        validated = sum(1 for r in self.results if r['validation_passed'])
        timeouts = sum(1 for r in self.results if r.get('timeout_occurred', False))
        
        times = [r['time_taken'] for r in self.results if r['success']]
        all_times = [r['time_taken'] for r in self.results]
        
        summary = {
            'total_tests': total,
            'successful': successful,
            'failed': total - successful,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'validated': validated,
            'validation_rate': (validated / total * 100) if total > 0 else 0,
            'timeouts': timeouts,
            'timeout_rate': (timeouts / total * 100) if total > 0 else 0,
            'avg_time_success': np.mean(times) if times else 0,
            'avg_time_all': np.mean(all_times) if all_times else 0,
            'median_time': np.median(times) if times else 0,
            'min_time': np.min(times) if times else 0,
            'max_time': np.max(times) if times else 0,
            'std_time': np.std(times) if times else 0,
            'percentile_95': np.percentile(times, 95) if times else 0,
            'by_category': {}
        }
        
        # Per-category statistics
        for category in TEST_CASES.keys():
            cat_results = [r for r in self.results if r['category'] == category]
            cat_success = sum(1 for r in cat_results if r['success'])
            cat_validated = sum(1 for r in cat_results if r['validation_passed'])
            cat_timeouts = sum(1 for r in cat_results if r.get('timeout_occurred', False))
            cat_times = [r['time_taken'] for r in cat_results if r['success']]
            
            summary['by_category'][category] = {
                'total': len(cat_results),
                'successful': cat_success,
                'failed': len(cat_results) - cat_success,
                'success_rate': (cat_success / len(cat_results) * 100) if cat_results else 0,
                'validated': cat_validated,
                'validation_rate': (cat_validated / len(cat_results) * 100) if cat_results else 0,
                'timeouts': cat_timeouts,
                'timeout_rate': (cat_timeouts / len(cat_results) * 100) if cat_results else 0,
                'avg_time': np.mean(cat_times) if cat_times else 0,
                'median_time': np.median(cat_times) if cat_times else 0,
            }
        
        return summary

# ============================================================================
# Enhanced Visualization Functions
# ============================================================================

def plot_enhanced_results(results: List[Dict]):
    """Generate comprehensive visualizations from benchmark results"""
    print("\n" + "=" * 80)
    print("GENERATING ENHANCED VISUALIZATIONS")
    print("=" * 80)
    
    df = pd.DataFrame(results)
    
    # Figure 1: Overview Dashboard
    plot_overview_dashboard(df)
    
    # Figure 2: Success Rate Analysis
    plot_success_analysis(df)
    
    # Figure 3: Time Performance Analysis
    plot_time_performance(df)
    
    # Figure 4: Category Deep Dive
    plot_category_analysis(df)
    
    # Figure 5: Validation Analysis
    plot_validation_analysis(df)
    
    # Figure 6: Timeout Analysis
    plot_timeout_analysis(df)
    
    # Figure 7: Test Progression
    plot_test_progression(df)
    
    # Figure 8: Complexity vs Performance
    plot_complexity_performance(df)
    
    print("\n✓ All enhanced plots saved to benchmark_plots/")

def plot_overview_dashboard(df):
    """Create comprehensive overview dashboard"""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 4, hspace=0.35, wspace=0.35)
    
    # Calculate key metrics
    total = len(df)
    successful = df['success'].sum()
    validated = df['validation_passed'].sum()
    timeouts = df['timeout_occurred'].sum()
    success_times = df[df['success']]['time_taken']
    
    # Title
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis('off')
    ax_title.text(0.5, 0.7, 'I2NSF Policy Generation System - Comprehensive Benchmark', 
                 ha='center', va='center', fontsize=22, fontweight='bold')
    ax_title.text(0.5, 0.3, f'140 Test Cases Across Multiple Complexity Levels', 
                 ha='center', va='center', fontsize=14, style='italic', color='gray')
    
    # KPI boxes
    kpis = [
        (gs[1, 0], f'{total}', 'Total Tests', '#3498DB'),
        (gs[1, 1], f'{success_times.mean():.1f}s', 'Avg Time', '#F39C12'),
        (gs[1, 2], f'{successful/total*100:.1f}%', 'Success Rate', '#27AE60'),
        (gs[1, 3], f'{validated/total*100:.1f}%', 'Validation Rate', '#9B59B6'),
    ]
    
    for pos, value, label, color in kpis:
        ax = fig.add_subplot(pos)
        ax.axis('off')
        ax.text(0.5, 0.6, value, ha='center', va='center', 
               fontsize=36, fontweight='bold', color=color)
        ax.text(0.5, 0.25, label, ha='center', va='center', 
               fontsize=12, fontweight='bold')
    
    # Category performance summary
    ax_cat = fig.add_subplot(gs[2, :])
    category_stats = df.groupby('category').agg({
        'success': lambda x: (x.sum() / len(x)) * 100,
        'validation_passed': lambda x: (x.sum() / len(x)) * 100,
        'time_taken': 'mean'
    }).reset_index()
    
    x = np.arange(len(category_stats))
    width = 0.25
    
    bars1 = ax_cat.bar(x - width, category_stats['success'], width, 
                      label='Success Rate (%)', color='#27AE60', alpha=0.8)
    bars2 = ax_cat.bar(x, category_stats['validation_passed'], width,
                      label='Validation Rate (%)', color='#3498DB', alpha=0.8)
    
    ax_cat_twin = ax_cat.twinx()
    line = ax_cat_twin.plot(x + width, category_stats['time_taken'], 'ro-',
                           linewidth=2.5, markersize=8, label='Avg Time (s)')
    
    ax_cat.set_xlabel('Category', fontweight='bold', fontsize=11)
    ax_cat.set_ylabel('Rate (%)', fontweight='bold', fontsize=11)
    ax_cat_twin.set_ylabel('Time (seconds)', fontweight='bold', fontsize=11)
    ax_cat.set_title('Performance Summary by Category', fontweight='bold', fontsize=13)
    ax_cat.set_xticks(x)
    ax_cat.set_xticklabels([c.replace('_', '\n') for c in category_stats['category']], 
                           rotation=45, ha='right', fontsize=8)
    ax_cat.legend(loc='upper left', fontsize=9)
    ax_cat_twin.legend(loc='upper right', fontsize=9)
    ax_cat.grid(axis='y', alpha=0.3)
    ax_cat.set_ylim(0, 105)
    
    plt.savefig('benchmark_plots/1_overview_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 1: Overview dashboard")

def plot_success_analysis(df):
    """Detailed success rate analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Subplot 1: Success by category
    ax1 = axes[0, 0]
    category_success = df.groupby('category').agg({
        'success': ['sum', 'count', lambda x: (x.sum()/len(x))*100]
    })['success']
    category_success.columns = ['successful', 'total', 'rate']
    
    bars = ax1.barh(range(len(category_success)), category_success['rate'],
                    color='#27AE60', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_yticks(range(len(category_success)))
    ax1.set_yticklabels([c.replace('_', ' ').title() for c in category_success.index])
    ax1.set_xlabel('Success Rate (%)', fontweight='bold')
    ax1.set_title('Success Rate by Category', fontweight='bold')
    ax1.set_xlim(0, 105)
    ax1.grid(axis='x', alpha=0.3)
    
    for i, (bar, rate) in enumerate(zip(bars, category_success['rate'])):
        ax1.text(rate + 2, i, f'{rate:.1f}%', 
                va='center', fontsize=9, fontweight='bold')
    
    # Subplot 2: Success vs Failure pie
    ax2 = axes[0, 1]
    success_counts = df['success'].value_counts()
    colors = ['#27AE60', '#E74C3C']
    labels = [f'Success\n({success_counts.get(True, 0)})', 
              f'Failed\n({success_counts.get(False, 0)})']
    
    wedges, texts, autotexts = ax2.pie([success_counts.get(True, 0), 
                                         success_counts.get(False, 0)],
                                        labels=labels,
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax2.set_title('Overall Success Distribution', fontweight='bold')
    
    # Subplot 3: Success rate trend
    ax3 = axes[1, 0]
    window_size = 10
    df_sorted = df.sort_values('test_number')
    rolling_success = df_sorted['success'].rolling(window=window_size).mean() * 100
    
    ax3.plot(df_sorted['test_number'], rolling_success, linewidth=2.5, color='#3498DB')
    ax3.fill_between(df_sorted['test_number'], rolling_success, alpha=0.3, color='#3498DB')
    ax3.axhline(y=df['success'].mean()*100, color='red', linestyle='--', 
                linewidth=2, label=f'Overall: {df["success"].mean()*100:.1f}%')
    ax3.set_xlabel('Test Number', fontweight='bold')
    ax3.set_ylabel('Success Rate (%) - Rolling Average', fontweight='bold')
    ax3.set_title(f'Success Rate Trend (Window={window_size})', fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 105)
    
    # Subplot 4: Failure reasons
    ax4 = axes[1, 1]
    failed_df = df[~df['success']]
    
    if len(failed_df) > 0:
        failure_categories = failed_df.groupby('category').size().sort_values(ascending=True)
        bars = ax4.barh(range(len(failure_categories)), failure_categories.values,
                        color='#E74C3C', alpha=0.8, edgecolor='black', linewidth=1.5)
        ax4.set_yticks(range(len(failure_categories)))
        ax4.set_yticklabels([c.replace('_', ' ').title() for c in failure_categories.index])
        ax4.set_xlabel('Number of Failures', fontweight='bold')
        ax4.set_title(f'Failure Distribution (Total: {len(failed_df)})', fontweight='bold')
        ax4.grid(axis='x', alpha=0.3)
        
        for i, (bar, count) in enumerate(zip(bars, failure_categories.values)):
            ax4.text(count + 0.2, i, str(count), 
                    va='center', fontsize=9, fontweight='bold')
    else:
        ax4.text(0.5, 0.5, 'No Failures!\n100% Success', 
                ha='center', va='center', fontsize=20, fontweight='bold', color='green')
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')
    
    plt.suptitle('Success Rate Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('benchmark_plots/2_success_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 2: Success analysis")

def plot_time_performance(df):
    """Comprehensive time performance analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    successful_df = df[df['success']]
    
    # Subplot 1: Time distribution histogram
    ax1 = axes[0, 0]
    ax1.hist(successful_df['time_taken'], bins=40, color='#3498DB', 
            alpha=0.7, edgecolor='black')
    ax1.axvline(successful_df['time_taken'].mean(), color='red', linestyle='--', 
                linewidth=2, label=f'Mean: {successful_df["time_taken"].mean():.1f}s')
    ax1.axvline(successful_df['time_taken'].median(), color='orange', linestyle='--', 
                linewidth=2, label=f'Median: {successful_df["time_taken"].median():.1f}s')
    ax1.set_xlabel('Processing Time (seconds)', fontweight='bold')
    ax1.set_ylabel('Frequency', fontweight='bold')
    ax1.set_title('Processing Time Distribution', fontweight='bold')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Subplot 2: Box plot by category
    ax2 = axes[0, 1]
    categories = successful_df['category'].unique()
    data_to_plot = [successful_df[successful_df['category'] == cat]['time_taken'].values 
                    for cat in categories]
    
    bp = ax2.boxplot(data_to_plot, labels=[c.replace('_', '\n')[:15] for c in categories], 
                     patch_artist=True)
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Processing Time (seconds)', fontweight='bold')
    ax2.set_title('Time by Category', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=7)
    
    # Subplot 3: Cumulative distribution
    ax3 = axes[1, 0]
    sorted_times = np.sort(successful_df['time_taken'])
    cumulative = np.arange(1, len(sorted_times) + 1) / len(sorted_times) * 100
    
    ax3.plot(sorted_times, cumulative, linewidth=2.5, color='#27AE60')
    ax3.axhline(y=50, color='red', linestyle='--', alpha=0.5)
    ax3.axhline(y=95, color='orange', linestyle='--', alpha=0.5)
    ax3.set_xlabel('Processing Time (seconds)', fontweight='bold')
    ax3.set_ylabel('Cumulative Percentage', fontweight='bold')
    ax3.set_title('Cumulative Time Distribution', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Add percentile markers
    p50 = successful_df['time_taken'].median()
    p95 = successful_df['time_taken'].quantile(0.95)
    ax3.text(p50, 55, f'50th: {p50:.1f}s', fontsize=9, fontweight='bold')
    ax3.text(p95, 97, f'95th: {p95:.1f}s', fontsize=9, fontweight='bold')
    
    # Subplot 4: Time statistics table
    ax4 = axes[1, 1]
    ax4.axis('tight')
    ax4.axis('off')
    
    stats_data = [
        ['Metric', 'Value'],
        ['Mean', f'{successful_df["time_taken"].mean():.2f}s'],
        ['Median', f'{successful_df["time_taken"].median():.2f}s'],
        ['Std Dev', f'{successful_df["time_taken"].std():.2f}s'],
        ['Min', f'{successful_df["time_taken"].min():.2f}s'],
        ['Max', f'{successful_df["time_taken"].max():.2f}s'],
        ['25th %ile', f'{successful_df["time_taken"].quantile(0.25):.2f}s'],
        ['75th %ile', f'{successful_df["time_taken"].quantile(0.75):.2f}s'],
        ['95th %ile', f'{successful_df["time_taken"].quantile(0.95):.2f}s'],
    ]
    
    table = ax4.table(cellText=stats_data, cellLoc='center', loc='center',
                     bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    for i in range(len(stats_data)):
        cell = table[(i, 0)]
        cell.set_facecolor('#ECF0F1')
        cell.set_text_props(weight='bold')
        
        if i == 0:
            for j in range(2):
                cell = table[(i, j)]
                cell.set_facecolor('#3498DB')
                cell.set_text_props(weight='bold', color='white')
    
    ax4.set_title('Time Statistics Summary', fontweight='bold', fontsize=12, pad=20)
    
    plt.suptitle('Processing Time Performance Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('benchmark_plots/3_time_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 3: Time performance")

def plot_category_analysis(df):
    """Deep dive into category performance"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Subplot 1: Tests per category
    ax1 = axes[0, 0]
    category_counts = df['category'].value_counts().sort_values(ascending=True)
    
    bars = ax1.barh(range(len(category_counts)), category_counts.values,
                    color='#3498DB', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_yticks(range(len(category_counts)))
    ax1.set_yticklabels([c.replace('_', ' ').title() for c in category_counts.index], fontsize=9)
    ax1.set_xlabel('Number of Tests', fontweight='bold')
    ax1.set_title('Test Distribution by Category', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    for i, (bar, count) in enumerate(zip(bars, category_counts.values)):
        ax1.text(count + 0.5, i, str(count), 
                va='center', fontsize=10, fontweight='bold')
    
    # Subplot 2: Category performance heatmap
    ax2 = axes[0, 1]
    category_metrics = df.groupby('category').agg({
        'success': lambda x: (x.sum()/len(x))*100,
        'validation_passed': lambda x: (x.sum()/len(x))*100,
        'time_taken': 'mean',
        'timeout_occurred': lambda x: (x.sum()/len(x))*100
    }).round(1)
    
    # Normalize for heatmap
    heatmap_data = category_metrics.copy()
    heatmap_data['time_taken'] = 100 - (heatmap_data['time_taken'] / heatmap_data['time_taken'].max() * 100)
    heatmap_data['timeout_occurred'] = 100 - heatmap_data['timeout_occurred']
    
    im = ax2.imshow(heatmap_data.T, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
    
    ax2.set_xticks(range(len(category_metrics)))
    ax2.set_xticklabels([c.replace('_', '\n')[:15] for c in category_metrics.index], 
                        rotation=45, ha='right', fontsize=7)
    ax2.set_yticks(range(len(heatmap_data.columns)))
    ax2.set_yticklabels(['Success', 'Validation', 'Speed', 'Reliability'], fontsize=9)
    ax2.set_title('Category Performance Heatmap', fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2)
    cbar.set_label('Score (0-100)', rotation=270, labelpad=20, fontweight='bold')
    
    # Add text annotations
    for i in range(len(category_metrics)):
        for j in range(len(heatmap_data.columns)):
            text = ax2.text(i, j, f'{heatmap_data.iloc[i, j]:.0f}',
                           ha="center", va="center", color="black", fontsize=7)
    
    # Subplot 3: Average metrics by category
    ax3 = axes[1, 0]
    x = np.arange(len(category_metrics))
    width = 0.35
    
    bars1 = ax3.bar(x - width/2, category_metrics['success'], width,
                   label='Success Rate', color='#27AE60', alpha=0.8)
    bars2 = ax3.bar(x + width/2, category_metrics['validation_passed'], width,
                   label='Validation Rate', color='#3498DB', alpha=0.8)
    
    ax3.set_ylabel('Rate (%)', fontweight='bold')
    ax3.set_title('Success vs Validation by Category', fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels([c.replace('_', '\n')[:12] for c in category_metrics.index],
                        rotation=45, ha='right', fontsize=7)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    ax3.set_ylim(0, 105)
    
    # Subplot 4: Category complexity vs performance
    ax4 = axes[1, 1]
    
    # Assign complexity scores based on category names
    complexity_scores = {
        'simple_firewall': 1, 'simple_geographic': 1,
        'medium_time_based': 2, 'medium_application': 2, 'medium_ddos': 2, 'medium_mixed': 2.5,
        'moderate_geographic_time': 3, 'moderate_application_geo': 3, 
        'moderate_security': 3, 'moderate_rate_limiting': 3,
        'complex_multi_layer': 4, 'complex_security': 4, 
        'complex_enterprise': 4, 'complex_advanced': 4.5
    }
    
    category_perf = df.groupby('category').agg({
        'success': lambda x: (x.sum()/len(x))*100,
        'time_taken': 'mean'
    })
    
    complexity = [complexity_scores.get(cat, 2.5) for cat in category_perf.index]
    
    scatter = ax4.scatter(complexity, category_perf['success'], 
                         s=category_perf['time_taken']*2, 
                         alpha=0.6, c=complexity, cmap='viridis',
                         edgecolors='black', linewidth=1.5)
    
    ax4.set_xlabel('Complexity Level', fontweight='bold')
    ax4.set_ylabel('Success Rate (%)', fontweight='bold')
    ax4.set_title('Complexity vs Success (bubble size = time)', fontweight='bold')
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0.5, 5)
    ax4.set_ylim(0, 105)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax4)
    cbar.set_label('Complexity', rotation=270, labelpad=15, fontweight='bold')
    
    plt.suptitle('Category Analysis Deep Dive', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('benchmark_plots/4_category_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 4: Category analysis")

def plot_validation_analysis(df):
    """Detailed validation analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Subplot 1: Validation success pie
    ax1 = axes[0, 0]
    validation_counts = df['validation_passed'].value_counts()
    colors = ['#27AE60', '#E74C3C']
    labels = [f'Valid\n({validation_counts.get(True, 0)})', 
              f'Invalid\n({validation_counts.get(False, 0)})']
    
    wedges, texts, autotexts = ax1.pie([validation_counts.get(True, 0), 
                                         validation_counts.get(False, 0)],
                                        labels=labels,
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title('Overall Validation Results', fontweight='bold')
    
    # Subplot 2: Validation by category
    ax2 = axes[0, 1]
    category_validation = df.groupby('category').agg({
        'validation_passed': ['sum', 'count', lambda x: (x.sum()/len(x))*100]
    })['validation_passed']
    category_validation.columns = ['valid', 'total', 'rate']
    category_validation = category_validation.sort_values('rate', ascending=True)
    
    bars = ax2.barh(range(len(category_validation)), category_validation['rate'],
                    color='#27AE60', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax2.set_yticks(range(len(category_validation)))
    ax2.set_yticklabels([c.replace('_', ' ').title() for c in category_validation.index], fontsize=8)
    ax2.set_xlabel('Validation Rate (%)', fontweight='bold')
    ax2.set_title('Validation Rate by Category', fontweight='bold')
    ax2.set_xlim(0, 105)
    ax2.grid(axis='x', alpha=0.3)
    
    for i, (bar, rate) in enumerate(zip(bars, category_validation['rate'])):
        ax2.text(rate + 2, i, f'{rate:.1f}%', 
                va='center', fontsize=8, fontweight='bold')
    
    # Subplot 3: Success vs Validation scatter
    ax3 = axes[1, 0]
    
    # Create 2x2 contingency matrix
    success_valid = len(df[(df['success']) & (df['validation_passed'])])
    success_invalid = len(df[(df['success']) & (~df['validation_passed'])])
    fail_valid = len(df[(~df['success']) & (df['validation_passed'])])
    fail_invalid = len(df[(~df['success']) & (~df['validation_passed'])])
    
    categories = ['Success\n& Valid', 'Success\n& Invalid', 'Fail\n& Valid', 'Fail\n& Invalid']
    values = [success_valid, success_invalid, fail_valid, fail_invalid]
    colors_bar = ['#27AE60', '#F39C12', '#3498DB', '#E74C3C']
    
    bars = ax3.bar(categories, values, color=colors_bar, alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Number of Tests', fontweight='bold')
    ax3.set_title('Success vs Validation Matrix', fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{val}\n({val/len(df)*100:.1f}%)', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Subplot 4: Validation rate trend
    ax4 = axes[1, 1]
    window_size = 10
    df_sorted = df.sort_values('test_number')
    rolling_validation = df_sorted['validation_passed'].rolling(window=window_size).mean() * 100
    
    ax4.plot(df_sorted['test_number'], rolling_validation, linewidth=2.5, color='#27AE60')
    ax4.fill_between(df_sorted['test_number'], rolling_validation, alpha=0.3, color='#27AE60')
    ax4.axhline(y=df['validation_passed'].mean()*100, color='red', linestyle='--', 
                linewidth=2, label=f'Overall: {df["validation_passed"].mean()*100:.1f}%')
    ax4.set_xlabel('Test Number', fontweight='bold')
    ax4.set_ylabel('Validation Rate (%) - Rolling Average', fontweight='bold')
    ax4.set_title(f'Validation Rate Trend (Window={window_size})', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 105)
    
    plt.suptitle('Validation Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('benchmark_plots/5_validation_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 5: Validation analysis")

def plot_timeout_analysis(df):
    """Analyze timeout patterns"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    timeout_df = df[df['timeout_occurred'] == True]
    
    # Subplot 1: Timeout distribution
    ax1 = axes[0, 0]
    timeout_counts = df['timeout_occurred'].value_counts()
    colors = ['#27AE60', '#E74C3C']
    labels = [f'Completed\n({timeout_counts.get(False, 0)})', 
              f'Timeout\n({timeout_counts.get(True, 0)})']
    
    wedges, texts, autotexts = ax1.pie([timeout_counts.get(False, 0), 
                                         timeout_counts.get(True, 0)],
                                        labels=labels,
                                        autopct='%1.1f%%',
                                        colors=colors,
                                        startangle=90,
                                        textprops={'fontsize': 11, 'fontweight': 'bold'})
    ax1.set_title('Timeout Distribution', fontweight='bold')
    
    # Subplot 2: Timeouts by category
    ax2 = axes[0, 1]
    
    if len(timeout_df) > 0:
        timeout_by_cat = timeout_df.groupby('category').size().sort_values(ascending=True)
        
        bars = ax2.barh(range(len(timeout_by_cat)), timeout_by_cat.values,
                        color='#E74C3C', alpha=0.8, edgecolor='black', linewidth=1.5)
        ax2.set_yticks(range(len(timeout_by_cat)))
        ax2.set_yticklabels([c.replace('_', ' ').title() for c in timeout_by_cat.index], fontsize=9)
        ax2.set_xlabel('Number of Timeouts', fontweight='bold')
        ax2.set_title(f'Timeouts by Category (Total: {len(timeout_df)})', fontweight='bold')
        ax2.grid(axis='x', alpha=0.3)
        
        for i, (bar, count) in enumerate(zip(bars, timeout_by_cat.values)):
            ax2.text(count + 0.2, i, str(count), 
                    va='center', fontsize=9, fontweight='bold')
    else:
        ax2.text(0.5, 0.5, 'No Timeouts!\nPerfect Performance', 
                ha='center', va='center', fontsize=16, fontweight='bold', color='green')
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.axis('off')
    
    # Subplot 3: Timeout rate by category
    ax3 = axes[1, 0]
    timeout_rate_by_cat = df.groupby('category').agg({
        'timeout_occurred': lambda x: (x.sum()/len(x))*100
    })['timeout_occurred'].sort_values(ascending=True)
    
    bars = ax3.barh(range(len(timeout_rate_by_cat)), timeout_rate_by_cat.values,
                    color='#F39C12', alpha=0.8, edgecolor='black', linewidth=1.5)
    ax3.set_yticks(range(len(timeout_rate_by_cat)))
    ax3.set_yticklabels([c.replace('_', ' ').title() for c in timeout_rate_by_cat.index], fontsize=8)
    ax3.set_xlabel('Timeout Rate (%)', fontweight='bold')
    ax3.set_title('Timeout Rate by Category', fontweight='bold')
    ax3.set_xlim(0, max(timeout_rate_by_cat.values) * 1.2 if len(timeout_rate_by_cat) > 0 else 10)
    ax3.grid(axis='x', alpha=0.3)
    
    for i, (bar, rate) in enumerate(zip(bars, timeout_rate_by_cat.values)):
        ax3.text(rate + 0.5, i, f'{rate:.1f}%', 
                va='center', fontsize=8, fontweight='bold')
    
    # Subplot 4: Timeout trend over tests
    ax4 = axes[1, 1]
    window_size = 10
    df_sorted = df.sort_values('test_number')
    rolling_timeout = df_sorted['timeout_occurred'].rolling(window=window_size).mean() * 100
    
    ax4.plot(df_sorted['test_number'], rolling_timeout, linewidth=2.5, color='#E74C3C')
    ax4.fill_between(df_sorted['test_number'], rolling_timeout, alpha=0.3, color='#E74C3C')
    ax4.axhline(y=df['timeout_occurred'].mean()*100, color='red', linestyle='--', 
                linewidth=2, label=f'Overall: {df["timeout_occurred"].mean()*100:.1f}%')
    ax4.set_xlabel('Test Number', fontweight='bold')
    ax4.set_ylabel('Timeout Rate (%) - Rolling Average', fontweight='bold')
    ax4.set_title(f'Timeout Rate Trend (Window={window_size})', fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, max(rolling_timeout.max() * 1.2 if not rolling_timeout.isna().all() else 10, 5))
    
    plt.suptitle('Timeout Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('benchmark_plots/6_timeout_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 6: Timeout analysis")

def plot_test_progression(df):
    """Visualize test progression over time"""
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    
    df_sorted = df.sort_values('test_number')
    
    # Subplot 1: Success over time
    ax1 = axes[0]
    
    colors = ['#27AE60' if s else '#E74C3C' for s in df_sorted['success']]
    bars = ax1.bar(df_sorted['test_number'], df_sorted['time_taken'], 
                   color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    ax1.set_xlabel('Test Number', fontweight='bold', fontsize=12)
    ax1.set_ylabel('Processing Time (seconds)', fontweight='bold', fontsize=12)
    ax1.set_title('Test Results Over Time (Green=Success, Red=Failure)', 
                  fontweight='bold', fontsize=14)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add category boundaries
    category_changes = []
    current_cat = None
    for idx, row in df_sorted.iterrows():
        if row['category'] != current_cat:
            category_changes.append(row['test_number'])
            current_cat = row['category']
    
    for change in category_changes:
        ax1.axvline(x=change, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    # Subplot 2: Cumulative metrics
    ax2 = axes[1]
    
    cumulative_success = df_sorted['success'].cumsum()
    cumulative_tests = np.arange(1, len(df_sorted) + 1)
    success_rate = (cumulative_success / cumulative_tests) * 100
    
    ax2.plot(cumulative_tests, success_rate, linewidth=3, color='#3498DB', label='Success Rate')
    ax2.fill_between(cumulative_tests, success_rate, alpha=0.3, color='#3498DB')
    
    # Add validation rate
    cumulative_validation = df_sorted['validation_passed'].cumsum()
    validation_rate = (cumulative_validation / cumulative_tests) * 100
    ax2.plot(cumulative_tests, validation_rate, linewidth=3, color='#27AE60', 
            label='Validation Rate', linestyle='--')
    
    ax2.set_xlabel('Test Number', fontweight='bold', fontsize=12)
    ax2.set_ylabel('Cumulative Rate (%)', fontweight='bold', fontsize=12)
    ax2.set_title('Cumulative Success and Validation Rates', fontweight='bold', fontsize=14)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, 105)
    
    # Add final statistics
    final_success = success_rate.iloc[-1]
    final_validation = validation_rate.iloc[-1]
    ax2.text(len(df_sorted) * 0.7, 20, 
            f'Final Success Rate: {final_success:.1f}%\nFinal Validation Rate: {final_validation:.1f}%',
            fontsize=12, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.suptitle('Test Progression Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('benchmark_plots/7_test_progression.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 7: Test progression")

def plot_complexity_performance(df):
    """Analyze performance vs complexity"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Assign complexity levels
    complexity_map = {
        'simple_firewall': 1, 'simple_geographic': 1,
        'medium_time_based': 2, 'medium_application': 2, 'medium_ddos': 2, 'medium_mixed': 2.5,
        'moderate_geographic_time': 3, 'moderate_application_geo': 3, 
        'moderate_security': 3, 'moderate_rate_limiting': 3,
        'complex_multi_layer': 4, 'complex_security': 4, 
        'complex_enterprise': 4, 'complex_advanced': 4.5
    }
    
    df['complexity'] = df['category'].map(complexity_map)
    complexity_labels = ['Simple\n(1)', 'Medium\n(2-2.5)', 'Moderate\n(3)', 'Complex\n(4-4.5)']
    complexity_bins = [0, 1.5, 2.75, 3.5, 5]
    df['complexity_group'] = pd.cut(df['complexity'], bins=complexity_bins, 
                                    labels=complexity_labels)
    
    # Subplot 1: Success rate by complexity
    ax1 = axes[0, 0]
    complexity_success = df.groupby('complexity_group').agg({
        'success': lambda x: (x.sum()/len(x))*100
    })['success']
    
    bars = ax1.bar(range(len(complexity_success)), complexity_success.values,
                   color=['#A8E6CF', '#FFD3B6', '#FFAAA5', '#FF8B94'], 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    ax1.set_xticks(range(len(complexity_success)))
    ax1.set_xticklabels(complexity_labels)
    ax1.set_ylabel('Success Rate (%)', fontweight='bold')
    ax1.set_title('Success Rate by Complexity Level', fontweight='bold')
    ax1.set_ylim(0, 105)
    ax1.grid(axis='y', alpha=0.3)
    
    for bar, rate in zip(bars, complexity_success.values):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{rate:.1f}%', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')
    
    # Subplot 2: Time by complexity
    ax2 = axes[0, 1]
    successful_df = df[df['success']]
    data_to_plot = [successful_df[successful_df['complexity_group'] == label]['time_taken'].values 
                    for label in complexity_labels]
    
    bp = ax2.boxplot(data_to_plot, labels=complexity_labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], ['#A8E6CF', '#FFD3B6', '#FFAAA5', '#FF8B94']):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.set_ylabel('Processing Time (seconds)', fontweight='bold')
    ax2.set_title('Processing Time by Complexity', fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Subplot 3: Complexity scatter
    ax3 = axes[1, 0]
    
    scatter = ax3.scatter(df['complexity'], df['time_taken'],
                         c=['#27AE60' if s else '#E74C3C' for s in df['success']],
                         alpha=0.6, s=100, edgecolors='black', linewidth=1)
    
    ax3.set_xlabel('Complexity Level', fontweight='bold')
    ax3.set_ylabel('Processing Time (seconds)', fontweight='bold')
    ax3.set_title('Complexity vs Time (Green=Success, Red=Failure)', fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    # Add trend line for successful tests
    successful_df = df[df['success']]
    z = np.polyfit(successful_df['complexity'], successful_df['time_taken'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(successful_df['complexity'].min(), 
                         successful_df['complexity'].max(), 100)
    ax3.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, label='Trend')
    ax3.legend()
    
    # Subplot 4: Summary metrics table
    ax4 = axes[1, 1]
    ax4.axis('tight')
    ax4.axis('off')
    
    summary_by_complexity = df.groupby('complexity_group').agg({
        'success': ['count', lambda x: (x.sum()/len(x))*100],
        'validation_passed': lambda x: (x.sum()/len(x))*100,
        'time_taken': 'mean'
    }).round(1)
    
    table_data = [['Level', 'Count', 'Success %', 'Valid %', 'Avg Time']]
    for idx, row in summary_by_complexity.iterrows():
        table_data.append([
            str(idx),
            str(int(row[('success', 'count')])),
            f"{row[('success', '<lambda>')]}%",
            f"{row[('validation_passed', '<lambda>')]}%",
            f"{row[('time_taken', 'mean')]:.1f}s"
        ])
    
    table = ax4.table(cellText=table_data, cellLoc='center', loc='center',
                     bbox=[0, 0, 1, 1])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2.5)
    
    for i in range(len(table_data)):
        for j in range(len(table_data[0])):
            cell = table[(i, j)]
            if i == 0:
                cell.set_facecolor('#3498DB')
                cell.set_text_props(weight='bold', color='white')
            elif i % 2 == 0:
                cell.set_facecolor('#F8F9FA')
    
    ax4.set_title('Complexity Performance Summary', fontweight='bold', fontsize=12, pad=20)
    
    plt.suptitle('Complexity vs Performance Analysis', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('benchmark_plots/8_complexity_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Plot 8: Complexity performance")

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("I2NSF SECURITY POLICY GENERATION SYSTEM")
    print("ENHANCED COMPREHENSIVE BENCHMARK - 140 TESTS")
    print("=" * 80)
    print()
    
    # Check if generate.py exists
    if not os.path.exists('generate.py'):
        print("ERROR: generate.py not found in current directory!")
        print("Please run this script from the llm_backend directory.")
        sys.exit(1)
    
    # Display test plan
    total_tests = sum(len(cases) for cases in TEST_CASES.values())
    print(f"Enhanced Test Suite:")
    print(f"  Total test cases: {total_tests}")
    print(f"\nDistribution by complexity:")
    
    simple_count = len(TEST_CASES['simple_firewall']) + len(TEST_CASES['simple_geographic'])
    medium_count = (len(TEST_CASES['medium_time_based']) + len(TEST_CASES['medium_application']) + 
                   len(TEST_CASES['medium_ddos']) + len(TEST_CASES['medium_mixed']))
    moderate_count = (len(TEST_CASES['moderate_geographic_time']) + len(TEST_CASES['moderate_application_geo']) +
                     len(TEST_CASES['moderate_security']) + len(TEST_CASES['moderate_rate_limiting']))
    complex_count = (len(TEST_CASES['complex_multi_layer']) + len(TEST_CASES['complex_security']) +
                    len(TEST_CASES['complex_enterprise']) + len(TEST_CASES['complex_advanced']))
    
    print(f"    - Simple policies: {simple_count} tests")
    print(f"    - Medium complexity: {medium_count} tests")
    print(f"    - Moderate complexity: {moderate_count} tests")
    print(f"    - Complex policies: {complex_count} tests")
    
    print(f"\nEstimated time: {total_tests * 50 / 60:.0f} - {total_tests * 80 / 60:.0f} minutes")
    print()
    
    response = input("Start enhanced benchmark? (y/n): ")
    if response.lower() != 'y':
        print("Benchmark cancelled.")
        sys.exit(0)
    
    # Run benchmark
    runner = EnhancedBenchmarkRunner(timeout=180)
    runner.run_all_tests()
    
    # Print summary
    print("\n" + "=" * 80)
    print("ENHANCED BENCHMARK SUMMARY")
    print("=" * 80)
    
    summary = runner.generate_summary()
    print(f"\nOverall Statistics:")
    print(f"  Total Tests: {summary['total_tests']}")
    print(f"  Successful: {summary['successful']} ({summary['success_rate']:.1f}%)")
    print(f"  Failed: {summary['failed']}")
    print(f"  Validated: {summary['validated']} ({summary['validation_rate']:.1f}%)")
    print(f"  Timeouts: {summary['timeouts']} ({summary['timeout_rate']:.1f}%)")
    
    print(f"\nTiming Statistics (Successful Tests):")
    print(f"  Average: {summary['avg_time_success']:.2f}s")
    print(f"  Median: {summary['median_time']:.2f}s")
    print(f"  Min: {summary['min_time']:.2f}s")
    print(f"  Max: {summary['max_time']:.2f}s")
    print(f"  95th Percentile: {summary['percentile_95']:.2f}s")
    print(f"  Std Dev: {summary['std_time']:.2f}s")
    
    print(f"\nBy Category:")
    for category, stats in summary['by_category'].items():
        print(f"\n  {category.replace('_', ' ').title()}:")
        print(f"    Tests: {stats['total']}")
        print(f"    Success: {stats['successful']}/{stats['total']} ({stats['success_rate']:.1f}%)")
        print(f"    Validated: {stats['validated']}/{stats['total']} ({stats['validation_rate']:.1f}%)")
        print(f"    Timeouts: {stats['timeouts']} ({stats['timeout_rate']:.1f}%)")
        print(f"    Avg Time: {stats['avg_time']:.2f}s")
    
    # Generate plots
    plot_enhanced_results(runner.results)
    
    print("\n" + "=" * 80)
    print("✓ ENHANCED BENCHMARK COMPLETE")
    print("=" * 80)
    print(f"\nResults saved to: benchmark_results/")
    print(f"Plots saved to: benchmark_plots/")
    print(f"\n8 comprehensive visualization plots generated:")
    print(f"  1. Overview Dashboard")
    print(f"  2. Success Analysis")
    print(f"  3. Time Performance")
    print(f"  4. Category Analysis")
    print(f"  5. Validation Analysis")
    print(f"  6. Timeout Analysis")
    print(f"  7. Test Progression")
    print(f"  8. Complexity Performance")
    print()

if __name__ == "__main__":
    main()