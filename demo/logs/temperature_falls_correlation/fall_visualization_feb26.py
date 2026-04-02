# fall_temperature_visualization.py
from naoth.log import Reader as LogReader
from naoth.log import BehaviorParser
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime
from collections import defaultdict
import matplotlib.colors as mcolors

def extract_state_data(game_log, max_frames=None):
    """Extract state data from log file"""
    
    data = {
        'frame': [], 'time': [], 'fall_down_state': [],
        'game_state': [], 'motion_type': [],
        'temp_left': [], 'temp_right': []
    }
    
    parser = None
    frame_count = 0
    
    print(f"Processing {game_log}...")
    
    with LogReader(game_log) as reader:
        for frame in reader.read():
            if "BehaviorStateComplete" in frame and parser is None:
                parser = BehaviorParser(frame["BehaviorStateComplete"])
            
            if parser is not None and "BehaviorStateSparse" in frame:
                behavior_frame = parser.parse(frame["BehaviorStateSparse"])
                
                if behavior_frame is not None and hasattr(behavior_frame, 'input_symbols'):
                    inputs = behavior_frame.input_symbols
                    
                    data['frame'].append(frame.number)
                    data['time'].append(frame.number / 30.0)  # 30 FPS
                    
                    # Extract states and temperatures
                    fall_state = str(inputs.get('fall_down_state', 'unknown')).split('.')[-1]
                    data['fall_down_state'].append(fall_state)
                    
                    game_state = str(inputs.get('game.state', 'unknown')).split('.')[-1]
                    data['game_state'].append(game_state)
                    
                    motion = str(inputs.get('executed_motion.type', 'unknown')).split('.')[-1]
                    data['motion_type'].append(motion)
                    
                    data['temp_left'].append(inputs.get('body.temperature.leg.left', 0))
                    data['temp_right'].append(inputs.get('body.temperature.leg.right', 0))
                    
                    frame_count += 1
                    if frame_count % 5000 == 0:
                        print(f"Processed {frame_count} behavior frames...")
                    if max_frames and frame_count >= max_frames:
                        break
    
    print(f"Extracted data from {frame_count} frames")
    return data

def plot_states_timeline(data, output_filename=None):
    """Create comprehensive timeline visualization"""
    
    fig, axes = plt.subplots(5, 1, figsize=(18, 12), sharex=True)
    fig.suptitle('Robot States Timeline During Game', fontsize=16)
    
    times = np.array(data['time'])
    
    # Color definitions
    fall_colors = {'undefined': 'lightgray', 'upright': 'lightgreen',
                   'lying_on_front': 'red', 'lying_on_back': 'darkred'}
    
    game_colors = {'initial': 'lightblue', 'ready': 'yellow', 'set': 'orange',
                   'playing': 'green', 'standby': 'gray', 'unstiff': 'purple',
                   'finished': 'darkgray', 'penalized': 'red'}
    
    # Plot 1: Fall States
    plot_state_segments(axes[0], times, data['fall_down_state'], fall_colors, 'Fall State')
    
    # Plot 2: Game States  
    plot_state_segments(axes[1], times, data['game_state'], game_colors, 'Game State')
    
    # Plot 3: Temperature with Fall Highlights
    axes[2].plot(times, data['temp_left'], 'b-', label='Left Leg', alpha=0.7)
    axes[2].plot(times, data['temp_right'], 'r-', label='Right Leg', alpha=0.7)
    
    # Highlight fall periods
    highlight_fall_periods(axes[2], times, data['fall_down_state'])
    axes[2].set_ylabel('Temperature (°C)')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    # Plot 4: Falls per Minute Summary
    plot_falls_summary(axes[3], times, data)
    
    plt.tight_layout()
    if output_filename:
        plt.savefig(output_filename, dpi=150, bbox_inches='tight')
        print(f"Saved plot to {output_filename}")
    else:
        plt.show()

# Helper functions for plotting...
def plot_state_segments(ax, times, states, color_map, ylabel):
    """Plot states as continuous colored segments"""
    segments = []
    current_state = states[0]
    start_time = times[0]
    
    for i in range(1, len(states)):
        if states[i] != current_state:
            segments.append((start_time, times[i-1], current_state))
            current_state = states[i]
            start_time = times[i-1]
    segments.append((start_time, times[-1], current_state))
    
    for start, end, state in segments:
        color = color_map.get(state, 'gray')
        ax.barh(0, end-start, left=start, height=0.8, color=color, edgecolor='none', alpha=0.8)
    
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([])
    
    # Legend with counts
    state_counts = defaultdict(int)
    for _, _, state in segments:
        state_counts[state] += 1
    
    patches = [mpatches.Patch(color=color_map.get(state, 'gray'), 
                             label=f'{state} ({count}x)') 
               for state, count in state_counts.items() if state != 'unknown']
    ax.legend(handles=patches, loc='right', bbox_to_anchor=(1.15, 0.5), fontsize=8)

if __name__ == "__main__":
    game_log = "logs/game_spqr_5.log"  # Update path
    data = extract_state_data(game_log)
    plot_states_timeline(data, f"timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")