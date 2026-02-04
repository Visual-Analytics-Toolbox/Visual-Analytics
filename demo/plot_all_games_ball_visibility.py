#!/usr/bin/env python3
"""
Ball Visibility Analysis - 4 Separate Plots
Master's Thesis Analysis Tool
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

def create_plot_1_first_halves(df, output_folder):
    """Plot 1: First halves only - descending order"""
    half1_data = df[df['game'].str.contains('half1', case=False, na=False)].copy()
    half1_data = half1_data.sort_values('team_visibility_percent', ascending=False).reset_index(drop=True)
    half1_data['short_label'] = half1_data['game'].str.replace('Berlin United_vs_', '').str.replace('BerlinUnited_vs_', '').str.replace('_half1', '')
    
    # Debug: Print the label conversion
    print("Debug: First halves label conversion:")
    for _, row in half1_data.iterrows():
        print(f"  '{row['game']}' → '{row['short_label']}'")
    print()
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(half1_data)), half1_data['team_visibility_percent'], 
                   color='#3498db', alpha=0.8)
    
    plt.title('First Halves - Team Ball Visibility (Descending Order)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Games', fontsize=12)
    plt.ylabel('Team Ball Visibility (%)', fontsize=12)
    plt.xticks(range(len(half1_data)), half1_data['short_label'], rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, value in zip(bars, half1_data['team_visibility_percent']):
        plt.text(bar.get_x() + bar.get_width()/2., value + 0.8,
                f'{value:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    save_path = os.path.join(output_folder, 'plot1_first_halves_descending.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot 1 saved: {save_path}")
    return half1_data

def create_plot_2_second_halves(df, output_folder):
    """Plot 2: Second halves only - descending order"""
    half2_data = df[df['game'].str.contains('half2', case=False, na=False)].copy()
    half2_data = half2_data.sort_values('team_visibility_percent', ascending=False).reset_index(drop=True)
    half2_data['short_label'] = half2_data['game'].str.replace('Berlin United_vs_', '').str.replace('BerlinUnited_vs_', '').str.replace('_half2', '').str.replace('-to', '')
    
    # Debug: Print the label conversion
    print("Debug: Second halves label conversion:")
    for _, row in half2_data.iterrows():
        print(f"  '{row['game']}' → '{row['short_label']}'")
    print()
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(half2_data)), half2_data['team_visibility_percent'], 
                   color='#e74c3c', alpha=0.8)
    
    plt.title('Second Halves - Team Ball Visibility (Descending Order)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Games', fontsize=12)
    plt.ylabel('Team Ball Visibility (%)', fontsize=12)
    plt.xticks(range(len(half2_data)), half2_data['short_label'], rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, value in zip(bars, half2_data['team_visibility_percent']):
        plt.text(bar.get_x() + bar.get_width()/2., value + 0.8,
                f'{value:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    save_path = os.path.join(output_folder, 'plot2_second_halves_descending.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot 2 saved: {save_path}")
    return half2_data

def create_plot_3_all_halves(df, output_folder):
    """Plot 3: Both first and second halves combined - descending order"""
    all_halves = df.copy()
    all_halves = all_halves.sort_values('team_visibility_percent', ascending=False).reset_index(drop=True)
    all_halves['short_label'] = all_halves['game'].str.replace('Berlin United_vs_', '').str.replace('BerlinUnited_vs_', '')
    
    # Debug: Print some label conversions
    print("Debug: All halves label conversion (first 5):")
    for _, row in all_halves.head().iterrows():
        print(f"  '{row['game']}' → '{row['short_label']}'")
    print()
    
    # Color code: blue for half1, red for half2
    colors = ['#3498db' if 'half1' in game else '#e74c3c' for game in all_halves['game']]
    
    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(all_halves)), all_halves['team_visibility_percent'], 
                   color=colors, alpha=0.8)
    
    plt.title('All Game Halves - Team Ball Visibility (Descending Order)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Game Halves', fontsize=12)
    plt.ylabel('Team Ball Visibility (%)', fontsize=12)
    plt.xticks(range(len(all_halves)), all_halves['short_label'], rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, value in zip(bars, all_halves['team_visibility_percent']):
        plt.text(bar.get_x() + bar.get_width()/2., value + 0.8,
                f'{value:.1f}%', ha='center', va='bottom', fontsize=8)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#3498db', alpha=0.8, label='Half 1'),
                      Patch(facecolor='#e74c3c', alpha=0.8, label='Half 2')]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    save_path = os.path.join(output_folder, 'plot3_all_halves_descending.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot 3 saved: {save_path}")
    return all_halves

def create_plot_4_game_averages(df, output_folder):
    """Plot 4: Average of both halves per game - descending order"""
    # Create base game names by removing half indicators
    df['base_game'] = df['game'].str.replace('_half1', '').str.replace('_half2', '').str.replace('-to', '')
    
    # Debug: Print unique base games to check for issues
    print(f"Debug: Unique base games found: {sorted(df['base_game'].unique())}")
    
    # Group by base game name and calculate averages
    game_averages = []
    for base_game in df['base_game'].unique():
        game_data = df[df['base_game'] == base_game]
        print(f"Debug: Base game '{base_game}' has {len(game_data)} entries:")
        for _, row in game_data.iterrows():
            print(f"  - {row['game']}: {row['team_visibility_percent']:.2f}%")
        
        if len(game_data) >= 2:  # Has both halves
            avg_visibility = game_data['team_visibility_percent'].mean()
            clean_name = base_game.replace('Berlin United_vs_', '').replace('BerlinUnited_vs_', '')
            game_averages.append({
                'game': clean_name,
                'avg_visibility': avg_visibility
            })
            print(f"  → Average: {avg_visibility:.2f}% (Clean name: '{clean_name}')")
        else:
            print(f"  → Skipped (only {len(game_data)} half found)")
        print()
    
    # Convert to DataFrame and sort by average visibility (descending)
    avg_df = pd.DataFrame(game_averages)
    avg_df = avg_df.sort_values('avg_visibility', ascending=False).reset_index(drop=True)
    
    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(avg_df)), avg_df['avg_visibility'], 
                   color='#27ae60', alpha=0.8)
    
    plt.title('Game Averages - Team Ball Visibility (Descending Order)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Games', fontsize=12)
    plt.ylabel('Average Team Ball Visibility (%)', fontsize=12)
    plt.xticks(range(len(avg_df)), avg_df['game'], rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, value in zip(bars, avg_df['avg_visibility']):
        plt.text(bar.get_x() + bar.get_width()/2., value + 0.8,
                f'{value:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    save_path = os.path.join(output_folder, 'plot4_game_averages_descending.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Plot 4 saved: {save_path}")
    return avg_df

def print_summary_stats(half1_data, half2_data, all_halves, avg_df):
    """Print summary statistics for all plots"""
    print(f"\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    print(f"\nPlot 1 - First Halves ({len(half1_data)} games):")
    print(f"  Best: {half1_data.iloc[0]['short_label']} - {half1_data.iloc[0]['team_visibility_percent']:.1f}%")
    print(f"  Worst: {half1_data.iloc[-1]['short_label']} - {half1_data.iloc[-1]['team_visibility_percent']:.1f}%")
    print(f"  Average: {half1_data['team_visibility_percent'].mean():.1f}%")
    
    print(f"\nPlot 2 - Second Halves ({len(half2_data)} games):")
    print(f"  Best: {half2_data.iloc[0]['short_label']} - {half2_data.iloc[0]['team_visibility_percent']:.1f}%")
    print(f"  Worst: {half2_data.iloc[-1]['short_label']} - {half2_data.iloc[-1]['team_visibility_percent']:.1f}%")
    print(f"  Average: {half2_data['team_visibility_percent'].mean():.1f}%")
    
    print(f"\nPlot 3 - All Halves Combined ({len(all_halves)} halves):")
    print(f"  Best: {all_halves.iloc[0]['short_label']} - {all_halves.iloc[0]['team_visibility_percent']:.1f}%")
    print(f"  Worst: {all_halves.iloc[-1]['short_label']} - {all_halves.iloc[-1]['team_visibility_percent']:.1f}%")
    print(f"  Overall Average: {all_halves['team_visibility_percent'].mean():.1f}%")
    
    print(f"\nPlot 4 - Game Averages ({len(avg_df)} games):")
    print(f"  Best: {avg_df.iloc[0]['game']} - {avg_df.iloc[0]['avg_visibility']:.1f}%")
    print(f"  Worst: {avg_df.iloc[-1]['game']} - {avg_df.iloc[-1]['avg_visibility']:.1f}%")
    print(f"  Average of averages: {avg_df['avg_visibility'].mean():.1f}%")

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
    print("BALL VISIBILITY ANALYSIS - 4 SEPARATE PLOTS")
    print("="*60)
    
    # Load data
    df = load_and_process_data(csv_path)
    if df is None:
        return
    
    print("\nCreating plots...")
    
    # Create all 4 plots with output folder
    half1_data = create_plot_1_first_halves(df, output_folder)
    half2_data = create_plot_2_second_halves(df, output_folder)
    all_halves = create_plot_3_all_halves(df, output_folder)
    avg_df = create_plot_4_game_averages(df, output_folder)
    
    # Print summary statistics
    print_summary_stats(half1_data, half2_data, all_halves, avg_df)
    
    # Save data to CSV files in output folder
    half1_data.to_csv(os.path.join(output_folder, "plot1_first_halves_data.csv"), index=False)
    half2_data.to_csv(os.path.join(output_folder, "plot2_second_halves_data.csv"), index=False)
    all_halves.to_csv(os.path.join(output_folder, "plot3_all_halves_data.csv"), index=False)
    avg_df.to_csv(os.path.join(output_folder, "plot4_game_averages_data.csv"), index=False)
    
    print(f"\nData files saved in {output_folder}:")
    print(f"  - plot1_first_halves_data.csv")
    print(f"  - plot2_second_halves_data.csv") 
    print(f"  - plot3_all_halves_data.csv")
    print(f"  - plot4_game_averages_data.csv")
    
    print(f"\nAll plots generated successfully in folder: {output_folder}")

if __name__ == "__main__":
    main()