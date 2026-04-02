import json
import os
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from pathlib import Path

# Define the log ID to analyze
LOG_ID = 159  # Change this to the log ID you want to analyze
LOG_DIR = f"downloaded_logs/{LOG_ID}"

def load_team_state_data(log_dir):
    """Load team state data from the downloaded JSON file"""
    team_state_file = Path(log_dir) / "team_state.json"
    
    if not team_state_file.exists():
        print(f"Team state file not found at: {team_state_file}")
        return None
    
    try:
        with open(team_state_file, 'r') as f:
            team_state_data = json.load(f)
        
        print(f"Loaded {len(team_state_data)} team state entries")
        return team_state_data
    except Exception as e:
        print(f"Error loading team state data: {e}")
        return None

def extract_robot_states(team_state_data):
    """Extract robot states by robot number from team state data"""
    if not team_state_data:
        return None
    
    # Dictionary to store states for each robot
    robot_states = defaultdict(list)
    
    # Dictionary to map robot numbers to their states over time
    state_transitions = defaultdict(list)
    
    # List of all unique states we encounter
    all_states = set()
    
    # Process each team state entry
    for entry in team_state_data:
        if 'frame' not in entry:
            continue
        
        frame = entry.get('frame', 0)
        
        if 'representation_data' not in entry:
            continue
        
        rep_data = entry['representation_data']
        if isinstance(rep_data, str):
            try:
                rep_data = json.loads(rep_data)
            except:
                continue
        
        if not isinstance(rep_data, dict) or 'players' not in rep_data:
            continue
        
        # Process players in this frame
        for player in rep_data['players']:
            if 'number' not in player or 'robotState' not in player:
                continue
            
            robot_num = player['number']
            robot_state = player['robotState']
            all_states.add(robot_state)
            
            # Record the frame, state, and update timestamp
            state_transitions[robot_num].append({
                'frame': frame,
                'state': robot_state,
                'update_timestamp': player.get('robotStateUpdate', 0)
            })
    
    print(f"Found data for {len(state_transitions)} robots")
    print(f"All robot states found: {sorted(all_states)}")
    
    return state_transitions

def plot_robot_states(state_transitions):
    """Plot robot state transitions over time"""
    if not state_transitions:
        return
    
    # Define colors for different states
    state_colors = {
        'unstiff': 'gray',
        'standby': 'blue',
        'playing': 'green',
        'penalized': 'red',
        'finished': 'purple',
        'initial': 'yellow',
        # Add more states and colors as needed
    }
    
    # Create a numeric mapping for states for plotting
    all_states = sorted(set(state['state'] for robot_states in state_transitions.values() 
                           for state in robot_states))
    state_to_num = {state: i for i, state in enumerate(all_states)}
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot each robot's state transitions
    for robot_num, states in sorted(state_transitions.items()):
        # Sort states by frame
        states.sort(key=lambda x: x['frame'])
        
        frames = [state['frame'] for state in states]
        state_nums = [state_to_num[state['state']] for state in states]
        
        # Plot the state transitions
        for i in range(len(frames) - 1):
            # Plot a horizontal line for this state
            color = state_colors.get(states[i]['state'], 'black')
            ax.plot([frames[i], frames[i+1]], [state_nums[i], state_nums[i]], 
                   color=color, linewidth=2, label=f"Robot {robot_num}" if i == 0 else "")
            
            # Plot a vertical line for state transitions
            if state_nums[i] != state_nums[i+1]:
                ax.plot([frames[i+1], frames[i+1]], [state_nums[i], state_nums[i+1]], 
                       color='black', linestyle='--', alpha=0.5)
        
        # Plot the last state if we have data
        if frames:
            color = state_colors.get(states[-1]['state'], 'black')
            ax.plot([frames[-1], frames[-1] + 100], [state_nums[-1], state_nums[-1]], 
                   color=color, linewidth=2)
    
    # Set y-axis ticks and labels
    ax.set_yticks(range(len(all_states)))
    ax.set_yticklabels(all_states)
    
    # Add a grid for better readability
    ax.grid(True, alpha=0.3)
    
    # Add labels and title
    ax.set_xlabel('Frame Number')
    ax.set_ylabel('Robot State')
    title = f'Robot State Transitions Over Time (Log ID: {LOG_ID})'
    ax.set_title(title)
    
    # Create legend for robot numbers
    handles = [plt.Line2D([0], [0], color='black', linewidth=2, label=f"Robot {num}") 
              for num in sorted(state_transitions.keys())]
    ax.legend(handles=handles, loc='upper right')
    
    # Create legend for state colors
    state_handles = [plt.Line2D([0], [0], color=color, linewidth=2, label=state) 
                    for state, color in state_colors.items() if state in all_states]
    second_legend = ax.legend(handles=state_handles, loc='upper left')
    ax.add_artist(second_legend)
    
    # Save the plot
    output_dir = Path("robot_state_analysis")
    output_dir.mkdir(exist_ok=True)
    plot_file = output_dir / f"robot_state_transitions_log_{LOG_ID}.png"
    plt.savefig(plot_file)
    
    print(f"Saved robot state transitions plot to {plot_file}")
    plt.show()

def analyze_playing_state(state_transitions):
    """Analyze when robots enter the 'playing' state and how long they stay there"""
    if not state_transitions:
        return
    
    print("\n=== PLAYING STATE ANALYSIS ===")
    
    for robot_num, states in sorted(state_transitions.items()):
        # Sort states by frame
        states.sort(key=lambda x: x['frame'])
        
        # Find when the robot enters 'playing' state
        playing_entries = []
        current_playing = None
        
        for i, state in enumerate(states):
            if state['state'] == 'playing' and (i == 0 or states[i-1]['state'] != 'playing'):
                # Start of a new playing period
                current_playing = {
                    'start_frame': state['frame'],
                    'start_index': i
                }
            elif current_playing and state['state'] != 'playing':
                # End of a playing period
                current_playing['end_frame'] = state['frame']
                current_playing['end_index'] = i
                current_playing['duration'] = current_playing['end_frame'] - current_playing['start_frame']
                playing_entries.append(current_playing)
                current_playing = None
        
        # Handle case where robot is still in playing state at the end
        if current_playing:
            current_playing['end_frame'] = states[-1]['frame']
            current_playing['end_index'] = len(states) - 1
            current_playing['duration'] = current_playing['end_frame'] - current_playing['start_frame']
            playing_entries.append(current_playing)
        
        # Print analysis for this robot
        print(f"\nRobot {robot_num}:")
        if not playing_entries:
            print("  Never entered 'playing' state")
        else:
            print(f"  Entered 'playing' state {len(playing_entries)} times")
            for i, entry in enumerate(playing_entries):
                print(f"  Period {i+1}:")
                print(f"    Start frame: {entry['start_frame']}")
                print(f"    End frame: {entry['end_frame']}")
                print(f"    Duration: {entry['duration']} frames")
                
                # If robot exits playing state, show what state it transitioned to
                if entry['end_index'] < len(states):
                    next_state = states[entry['end_index']]['state']
                    print(f"    Transitioned to: {next_state}")

def main():
    """Main function to analyze robot states"""
    print(f"Analyzing robot states for log ID {LOG_ID}...")
    
    # Load team state data
    team_state_data = load_team_state_data(LOG_DIR)
    
    if not team_state_data:
        print("No team state data available for analysis")
        return
    
    # Extract robot states
    state_transitions = extract_robot_states(team_state_data)
    
    if not state_transitions:
        print("Failed to extract robot states")
        return
    
    # Plot robot state transitions
    plot_robot_states(state_transitions)
    
    # Analyze playing state
    analyze_playing_state(state_transitions)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main()