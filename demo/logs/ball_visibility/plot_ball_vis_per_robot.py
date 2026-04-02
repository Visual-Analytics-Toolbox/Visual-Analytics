#!/usr/bin/env python3
"""
Robot Number Ball Visibility Analysis
Analyzes which robot numbers see the ball most across all games
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def load_and_process_data(csv_path):
    """Load CSV data and process it for analysis"""
    try:
        df = pd.read_csv(csv_path)
        print(f"Successfully loaded {len(df)} rows from {csv_path}")
        return df
    except FileNotFoundError:
        print(f"Error: Could not find file at {csv_path}")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_robot_visibility(df):
    """Analyze ball visibility per robot number across all games"""
    
    # Get all player columns
    player_columns = [col for col in df.columns if col.startswith('player_') and col.endswith('_visibility_percent')]
    
    print(f"\nFound {len(player_columns)} player columns: {player_columns}")
    
    # Dictionary to store statistics for each robot number
    robot_stats = {}
    
    for col in player_columns:
        # Extract robot number from column name (e.g., 'player_1_visibility_percent' -> 1)
        robot_num = int(col.split('_')[1])
        
        # Get all non-null values for this robot
        values = df[col].dropna()
        
        # Filter out zeros (which likely mean the robot didn't participate)
        values = values[values > 0]
        
        if len(values) > 0:
            robot_stats[robot_num] = {
                'max': values.max(),
                'min': values.min(),
                'avg': values.mean(),
                'std': values.std(),
                'count': len(values)
            }
            
            print(f"\nRobot {robot_num}:")
            print(f"  Games played: {len(values)}")
            print(f"  Max visibility: {values.max():.2f}%")
            print(f"  Min visibility: {values.min():.2f}%")
            print(f"  Avg visibility: {values.mean():.2f}%")
            print(f"  Std deviation: {values.std():.2f}%")
    
    return robot_stats

def create_robot_visibility_plot(robot_stats, output_folder):
    """Create single grouped bar chart showing max, avg, min - ordered by max descending"""
    
    # Prepare data sorted by maximum visibility (descending)
    robot_numbers = sorted(robot_stats.keys())
    robot_data = [(r, robot_stats[r]['max'], robot_stats[r]['avg'], robot_stats[r]['min']) 
                  for r in robot_numbers]
    # Sort by maximum value (descending)
    robot_data.sort(key=lambda x: x[1], reverse=True)
    
    # Extract sorted data
    robots = [f'Robot {r}' for r, _, _, _ in robot_data]
    max_values = [max_val for _, max_val, _, _ in robot_data]
    avg_values = [avg_val for _, _, avg_val, _ in robot_data]
    min_values = [min_val for _, _, _, min_val in robot_data]
    
    # Set up the bar positions
    x = np.arange(len(robots))
    width = 0.25  # Width of bars
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 8))
    
    bars1 = ax.bar(x - width, max_values, width, label='Maximum', color='#2ecc71', alpha=0.8)
    bars2 = ax.bar(x, avg_values, width, label='Average', color='#3498db', alpha=0.8)
    bars3 = ax.bar(x + width, min_values, width, label='Minimum', color='#e74c3c', alpha=0.8)
    
    # Add value labels on bars
    for bar, value in zip(bars1, max_values):
        ax.text(bar.get_x() + bar.get_width()/2., value + 1,
               f'{value:.1f}%', ha='center', va='bottom', fontsize=9)
    
    for bar, value in zip(bars2, avg_values):
        ax.text(bar.get_x() + bar.get_width()/2., value + 1,
               f'{value:.1f}%', ha='center', va='bottom', fontsize=9)
    
    for bar, value in zip(bars3, min_values):
        ax.text(bar.get_x() + bar.get_width()/2., value + 1,
               f'{value:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Customize the plot
    ax.set_xlabel('Robot Number', fontsize=14, fontweight='bold')
    ax.set_ylabel('Ball Visibility (%)', fontsize=14, fontweight='bold')
    ax.set_title('Ball Visibility by Robot Number (Ordered by Maximum - Descending)\nMax, Average, and Min across all games', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(robots, rotation=45, ha='right')
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(True, alpha=0.3, axis='y')
    
    # Set y-axis to start from 0
    ax.set_ylim(0, max(max_values) + 10)
    
    plt.tight_layout()
    
    # Save the plot
    save_path = os.path.join(output_folder, 'robot_visibility_grouped.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot saved: {save_path}")

def create_detailed_statistics_plot(robot_stats, output_folder):
    """Create additional plot showing detailed statistics"""
    
    # Ensure robot numbers are ordered from 1 to 7 (or whatever range exists)
    robot_numbers = sorted(robot_stats.keys())
    avg_values = [robot_stats[r]['avg'] for r in robot_numbers]
    std_values = [robot_stats[r]['std'] for r in robot_numbers]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Average visibility with error bars (std deviation)
    bars = ax1.bar(robot_numbers, avg_values, color='#3498db', alpha=0.7, 
                   yerr=std_values, capsize=5, error_kw={'linewidth': 2})
    
    ax1.set_xlabel('Robot Number', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Average Ball Visibility (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Average Visibility by Robot (with Std Deviation)', fontsize=14, fontweight='bold')
    
    # Ensure x-axis shows all numbers from 1 to 7 (or max robot number)
    max_robot = max(robot_numbers) if robot_numbers else 7
    ax1.set_xticks(range(1, max_robot + 1))
    ax1.set_xticklabels([f'{r}' for r in range(1, max_robot + 1)])
    
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for i, (bar, val, std) in enumerate(zip(bars, avg_values, std_values)):
        ax1.text(bar.get_x() + bar.get_width()/2., val + std + 1,
                f'{val:.1f}%', ha='center', va='bottom', fontsize=10)
    
    # Plot 2: Games played by each robot
    games_played = [robot_stats[r]['count'] for r in robot_numbers]
    bars2 = ax2.bar(robot_numbers, games_played, color='#e67e22', alpha=0.7)
    
    ax2.set_xlabel('Robot Number', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Number of Games Played', fontsize=12, fontweight='bold')
    ax2.set_title('Games Played by Robot Number', fontsize=14, fontweight='bold')
    
    # Ensure x-axis shows all numbers from 1 to 7 (or max robot number)
    ax2.set_xticks(range(1, max_robot + 1))
    ax2.set_xticklabels([f'{r}' for r in range(1, max_robot + 1)])
    
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, val in zip(bars2, games_played):
        ax2.text(bar.get_x() + bar.get_width()/2., val + 0.2,
                f'{int(val)}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    # Save the plot
    save_path = os.path.join(output_folder, 'robot_detailed_statistics.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Detailed statistics plot saved: {save_path}")    
    
def save_statistics_to_csv(robot_stats, output_folder):
    """Save robot statistics to CSV file"""
    
    data = []
    for robot_num in sorted(robot_stats.keys()):
        stats = robot_stats[robot_num]
        data.append({
            'robot_number': robot_num,
            'max_visibility': stats['max'],
            'min_visibility': stats['min'],
            'avg_visibility': stats['avg'],
            'std_deviation': stats['std'],
            'games_played': stats['count']
        })
    
    df = pd.DataFrame(data)
    save_path = os.path.join(output_folder, 'robot_visibility_statistics.csv')
    df.to_csv(save_path, index=False)
    
    print(f"Statistics saved to: {save_path}")
    
    return df

def print_summary(robot_stats):
    """Print summary of findings"""
    
    print("\n" + "="*60)
    print("ROBOT VISIBILITY ANALYSIS SUMMARY")
    print("="*60)
    
    robot_numbers = sorted(robot_stats.keys())
    avg_values = [(r, robot_stats[r]['avg']) for r in robot_numbers]
    avg_values.sort(key=lambda x: x[1], reverse=True)
    
    print("\n📊 ROBOTS RANKED BY AVERAGE VISIBILITY:")
    for i, (robot, avg) in enumerate(avg_values, 1):
        print(f"  {i}. Robot {robot}: {avg:.2f}% (played {robot_stats[robot]['count']} games)")
    
    # Best performing robot
    best_robot, best_avg = avg_values[0]
    print(f"\n🏆 BEST PERFORMER: Robot {best_robot}")
    print(f"   Average: {best_avg:.2f}%")
    print(f"   Max: {robot_stats[best_robot]['max']:.2f}%")
    print(f"   Min: {robot_stats[best_robot]['min']:.2f}%")
    
    # Most consistent robot (lowest std deviation)
    consistent_robot = min(robot_numbers, key=lambda r: robot_stats[r]['std'])
    print(f"\n📈 MOST CONSISTENT: Robot {consistent_robot}")
    print(f"   Std deviation: {robot_stats[consistent_robot]['std']:.2f}%")
    print(f"   Average: {robot_stats[consistent_robot]['avg']:.2f}%")
    
    # Highest peak performance
    peak_robot = max(robot_numbers, key=lambda r: robot_stats[r]['max'])
    print(f"\n⭐ HIGHEST PEAK: Robot {peak_robot}")
    print(f"   Max visibility: {robot_stats[peak_robot]['max']:.2f}%")
    
    print("\n" + "="*60)

def main():
    """Main analysis function"""
    csv_path = "team_analysis_tables/master_team_summary.csv"
    
    # Create output folder with date
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_folder = f"output_{date_str}"
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")
    else:
        print(f"Using existing output folder: {output_folder}")
    
    print("="*60)
    print("ROBOT NUMBER BALL VISIBILITY ANALYSIS")
    print("="*60)
    
    # Load data
    df = load_and_process_data(csv_path)
    if df is None:
        return
    
    # Analyze robot visibility
    robot_stats = analyze_robot_visibility(df)
    
    if not robot_stats:
        print("No robot visibility data found!")
        return
    
    # Create visualizations
    print("\nCreating visualization...")
    create_robot_visibility_plot(robot_stats, output_folder)
    create_detailed_statistics_plot(robot_stats, output_folder)
    
    # Save statistics
    stats_df = save_statistics_to_csv(robot_stats, output_folder)
    
    # Print summary
    print_summary(robot_stats)
    
    print(f"\n✅ Analysis complete! All files saved in: {output_folder}")
    print(f"\nGenerated plots:")
    print(f"  - robot_visibility_grouped.png (max, avg, min grouped)")
    print(f"  - robot_detailed_statistics.png")
    print(f"  - robot_visibility_statistics.csv")

if __name__ == "__main__":
    main()

