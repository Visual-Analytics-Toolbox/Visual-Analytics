import json
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import datetime
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from collections import defaultdict

# ===== ONLY INPUT REQUIRED =====
LOG_START, LOG_END = 153, 159  # Replace with your actual log IDs
LOG_IDS = list(range(LOG_START, LOG_END + 1))

INPUT_DIR = 'downloaded_logs'
# This script creates:
# 1. Combined Plot - Team ball visibility (OR operation) with robot states as background
#    - Playing state shown in light green background
#    - Full duration analysis (no frame limits)
# 2. Summary Table - Individual player visibility (Player 1-7) + team statistics
#    - Individual player visibility percentages at the top of table
#    - Team-level ball visibility statistics
#    - Visibility run analysis (consecutive periods)
# ===============================

class ConsoleCapture:
    """Capture console output to both display and save to file"""
    
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.console_output = StringIO()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        
    def __enter__(self):
        class TeeWriter:
            def __init__(self, original, buffer):
                self.original = original
                self.buffer = buffer
                
            def write(self, text):
                self.original.write(text)
                self.buffer.write(text)
                
            def flush(self):
                self.original.flush()
                self.buffer.flush()
        
        self.tee_stdout = TeeWriter(self.original_stdout, self.console_output)
        self.tee_stderr = TeeWriter(self.original_stderr, self.console_output)
        
        sys.stdout = self.tee_stdout
        sys.stderr = self.tee_stderr
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            f.write(self.console_output.getvalue())

class SimplifiedTeamAnalyzer:
    """
    Simplified analyzer focusing on:
    1. Team ball visibility (OR operation across all robots) for full duration
    2. Robot states from one robot as background colors
    3. Master summary table that gets appended to for cross-game analysis
    
    Creates one plot and appends to one master table with essential metrics only.
    """
    
    def __init__(self, log_ids, input_dir='downloaded_logs'):
        self.log_ids = log_ids
        self.input_dir = Path(input_dir)
        self.robot_visibility = {}
        self.robot_states_data = None
        self.team_visibility_data = None
        self.playing_frames = {}
        self.log_info = {}
        self.event_name = ""
        self.game_name = ""
        
        # State colors for background visualization
        self.state_colors = {
            'unstiff': '#E8E8E8',      # Light Gray
            'standby': '#FFE4B5',      # Moccasin
            'calibration': '#FFB6C1',  # Light Pink
            'initial': '#E0F6FF',      # Light Blue
            'ready': '#F0FFF0',        # Honeydew
            'set': '#FFEDCC',          # Light Orange
            'playing': '#90EE90',      # Light Green (as requested)
            'finished': '#FFB6C1',     # Light Pink
            'penalized': '#FFB6B6',    # Light Red
            'timeout': '#E6E6FA',      # Lavender
            'unknown': '#F5F5F5'       # White Smoke
        }
        
        # Auto-load log info and detect playing frames
        self._load_log_info()
        self._auto_detect_playing_frames()
        
    def _load_log_info(self):
        """Load log information from log_info.json files"""
        print("Loading log information from log_info.json files...")
        
        events = set()
        games = set()
        
        for log_id in self.log_ids:
            log_dir = self.input_dir / str(log_id)
            log_info_file = log_dir / "log_info.json"
            
            if log_info_file.exists():
                try:
                    with open(log_info_file, 'r') as f:
                        info = json.load(f)
                    
                    self.log_info[log_id] = info
                    
                    if 'event' in info:
                        events.add(info['event'])
                    if 'game' in info:
                        games.add(info['game'])
                    
                    print(f"  Log {log_id}: Event='{info.get('event', 'N/A')}', Game='{info.get('game', 'N/A')}', Player={info.get('player', 'N/A')}")
                    
                except Exception as e:
                    print(f"  Error reading log_info.json for log {log_id}: {e}")
            else:
                print(f"  log_info.json not found for log {log_id}")
        
        # Determine event and game names
        self.event_name = list(events)[0] if len(events) == 1 else "Mixed_Events" if events else "Unknown_Event"
        self.game_name = list(games)[0] if len(games) == 1 else "Mixed_Games" if games else "Unknown_Game"
        
        print(f"Auto-detected: Event='{self.event_name}', Game='{self.game_name}'")
        print()
    
    def _auto_detect_playing_frames(self):
        """Auto-detect playing frames from team_state.json files"""
        print("Auto-detecting playing frames from team_state.json files...")
        
        for log_id in self.log_ids:
            playing_frame = self._find_playing_frame_for_robot(log_id)
            if playing_frame is not None:
                self.playing_frames[log_id] = playing_frame
                print(f"  Robot {log_id}: First playing frame detected at {playing_frame}")
            else:
                print(f"  Robot {log_id}: Could not detect playing frame")
        
        print(f"Successfully detected playing frames for {len(self.playing_frames)} robots")
        print()
    
    def _find_playing_frame_for_robot(self, log_id):
        """Find the first playing frame for a specific robot from team_state.json"""
        log_dir = self.input_dir / str(log_id)
        team_state_file = log_dir / "team_state.json"
        
        if not team_state_file.exists():
            return None
        
        try:
            with open(team_state_file, 'r') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                return None
            
            for entry in data:
                if not isinstance(entry, dict) or 'frame' not in entry or 'representation_data' not in entry:
                    continue
                
                frame = entry['frame']
                rep_data = entry['representation_data']
                
                if isinstance(rep_data, str):
                    try:
                        rep_data = json.loads(rep_data)
                    except:
                        continue
                
                if isinstance(rep_data, dict) and 'players' in rep_data:
                    players = rep_data['players']
                    if isinstance(players, list):
                        for player in players:
                            if isinstance(player, dict) and 'robotState' in player:
                                if str(player['robotState']).lower() == 'playing':
                                    return frame
            return None
            
        except Exception as e:
            print(f"    Error reading team_state.json for log {log_id}: {e}")
            return None
    
    def load_ball_visibility_data(self):
        """Load ball visibility data for all robots"""
        print("Loading ball visibility data for all robots...")
        
        for log_id in self.log_ids:
            log_dir = self.input_dir / str(log_id)
            ball_model_file = log_dir / "ball_model.json"
            
            if not ball_model_file.exists():
                print(f"  Ball model file not found for log {log_id}")
                continue
            
            try:
                with open(ball_model_file, 'r') as f:
                    ball_data = json.load(f)
                
                # Extract frames and visibility
                frames = []
                visibility = []
                
                for entry in ball_data:
                    if 'frame' not in entry or 'representation_data' not in entry:
                        continue
                    
                    frame = entry['frame']
                    rep_data = entry['representation_data']
                    
                    if isinstance(rep_data, str):
                        try:
                            rep_data = json.loads(rep_data)
                        except:
                            rep_data = {}
                    
                    knows_ball = False
                    if isinstance(rep_data, dict) and 'knows' in rep_data:
                        knows_ball = bool(rep_data['knows'])
                    
                    frames.append(frame)
                    visibility.append(1 if knows_ball else 0)
                
                if frames:
                    # Sort by frame
                    sorted_indices = np.argsort(frames)
                    frames = np.array(frames)[sorted_indices]
                    visibility = np.array(visibility)[sorted_indices]
                    
                    # Calculate stats
                    visible_frames = np.sum(visibility)
                    total_frames = len(visibility)
                    visibility_percent = (visible_frames / total_frames) * 100 if total_frames > 0 else 0
                    
                    self.robot_visibility[log_id] = {
                        'frames': frames,
                        'visibility': visibility,
                        'stats': {
                            'visible_frames': visible_frames,
                            'total_frames': total_frames,
                            'visibility_percent': visibility_percent
                        }
                    }
                    
                    print(f"  Robot {log_id}: {visibility_percent:.2f}% visibility ({visible_frames}/{total_frames} frames)")
                else:
                    print(f"  Robot {log_id}: No valid frame data found")
                    
            except Exception as e:
                print(f"  Error loading ball model data for Robot {log_id}: {e}")
        
        print(f"Successfully loaded ball visibility data for {len(self.robot_visibility)} robots")
        print()
    
    def load_robot_states_data(self):
        """Load robot states data from the first available robot for background - full duration"""
        print("Loading robot states data for background...")
        
        # Try to load from the first robot that has ball data
        candidate_robots = [log_id for log_id in self.log_ids if log_id in self.robot_visibility]
        
        if not candidate_robots:
            candidate_robots = self.log_ids
        
        if not candidate_robots:
            print("  No robot available for state data")
            return
        
        log_id = candidate_robots[0]
        log_dir = self.input_dir / str(log_id)
        team_state_file = log_dir / "team_state.json"
        
        if not team_state_file.exists():
            print(f"  team_state.json not found for robot {log_id}")
            return
        
        try:
            with open(team_state_file, 'r') as f:
                team_data = json.load(f)
            
            print(f"  Loading robot states from log {log_id}: {len(team_data)} entries")
            
            # Extract robot states over time for this robot's player number
            player_num = self.log_info.get(log_id, {}).get('player', 1)
            frames = []
            states = []
            
            for entry in team_data:
                if 'frame' not in entry or 'representation_data' not in entry:
                    continue
                
                frame = entry['frame']
                rep_data = entry['representation_data']
                
                if isinstance(rep_data, str):
                    try:
                        rep_data = json.loads(rep_data)
                    except:
                        continue
                
                if 'players' not in rep_data:
                    continue
                
                # Find this robot's state in the players array
                robot_state = 'unknown'
                for player in rep_data['players']:
                    if isinstance(player, dict) and player.get('number') == player_num:
                        robot_state = player.get('robotState', 'unknown')
                        break
                
                frames.append(frame)
                states.append(robot_state)
            
            if frames:
                # Sort by frame
                sorted_indices = np.argsort(frames)
                frames = np.array(frames)[sorted_indices]
                states = np.array(states)[sorted_indices]
                
                self.robot_states_data = {
                    'frames': frames,
                    'states': states,
                    'log_id': log_id,
                    'player_num': player_num
                }
                
                unique_states = set(states)
                print(f"  Loaded states for Robot {log_id} (Player {player_num}): {len(frames)} frames")
                print(f"  States found: {sorted(unique_states)}")
                print(f"  Frame range: {frames[0]} to {frames[-1]}")
            else:
                print(f"  No valid state data found for Robot {log_id}")
                
        except Exception as e:
            print(f"  Error loading robot states for log {log_id}: {e}")
        
        print()
    
    def synchronize_team_visibility(self):
        """Synchronize ball visibility data across all robots and compute team visibility"""
        if not self.robot_visibility:
            print("No robot visibility data available")
            return None
        
        print("Synchronizing team ball visibility...")
        
        # Use playing frames for synchronization if available
        robots_with_playing_frames = [log_id for log_id in self.robot_visibility.keys() 
                                    if log_id in self.playing_frames]
        
        if robots_with_playing_frames:
            reference_frame = min(self.playing_frames[log_id] for log_id in robots_with_playing_frames)
            print(f"Using playing frame synchronization, reference: {reference_frame}")
        else:
            # Fall back to first frame synchronization
            reference_frame = min(data['frames'][0] for data in self.robot_visibility.values())
            print(f"Using first frame synchronization, reference: {reference_frame}")
            # Create pseudo-playing frames
            for log_id, robot_data in self.robot_visibility.items():
                self.playing_frames[log_id] = robot_data['frames'][0]
        
        # Create synchronized DataFrames
        dfs = []
        for log_id, robot_data in self.robot_visibility.items():
            playing_frame = self.playing_frames.get(log_id, robot_data['frames'][0])
            offset = playing_frame - reference_frame
            
            # Adjust frames to reference
            adjusted_frames = robot_data['frames'] - offset
            
            df = pd.DataFrame({
                'frame': adjusted_frames,
                f'robot_{log_id}_visibility': robot_data['visibility']
            })
            
            dfs.append(df)
            print(f"  Robot {log_id}: Offset = {offset} frames")
        
        # Merge all DataFrames
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = pd.merge(merged_df, df, on='frame', how='outer')
        
        # Sort and fill missing values
        merged_df = merged_df.sort_values('frame').fillna(0)
        
        # Compute team visibility (OR operation)
        visibility_columns = [col for col in merged_df.columns if col.endswith('_visibility')]
        merged_df['team_visibility'] = merged_df[visibility_columns].max(axis=1)
        
        self.team_visibility_data = merged_df
        
        # Calculate statistics
        team_visible = merged_df['team_visibility'].sum()
        total_frames = len(merged_df)
        team_percent = (team_visible / total_frames) * 100 if total_frames > 0 else 0
        
        print(f"\nTEAM VISIBILITY STATISTICS:")
        print(f"Total synchronized frames: {total_frames}")
        print(f"Team can see ball: {team_visible} frames ({team_percent:.2f}%)")
        print(f"Team cannot see ball: {total_frames - team_visible} frames ({100 - team_percent:.2f}%)")
        print()
        
        return merged_df
    
    def create_combined_plot(self):
        """Create combined plot with team ball visibility and robot states properly synchronized"""
        if self.team_visibility_data is None:
            print("No team visibility data available for plotting")
            return None, None
        
        df = self.team_visibility_data.copy()
        
        print(f"Creating combined plot for full duration: {len(df)} frames")
        print(f"Ball visibility frame range: {df['frame'].min()} to {df['frame'].max()}")
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(20, 8))
        
        # Add robot states as background if available
        if self.robot_states_data is not None:
            states_data = self.robot_states_data
            log_id = states_data['log_id']
            player_num = states_data['player_num']
            
            print(f"Robot states from Robot {log_id} (Player {player_num})")
            print(f"Robot states frame range: {states_data['frames'].min()} to {states_data['frames'].max()}")
            
            # Synchronize state frames with visibility data
            if log_id in self.playing_frames and len(self.playing_frames) > 1:
                # Use playing frame synchronization
                reference_frame = min(self.playing_frames.values())
                playing_frame = self.playing_frames[log_id]
                offset = playing_frame - reference_frame
                adjusted_state_frames = states_data['frames'] - offset
                print(f"Using playing frame synchronization: offset = {offset}")
            else:
                # Use direct frame mapping (no offset)
                adjusted_state_frames = states_data['frames']
                print("Using direct frame mapping (no offset)")
            
            print(f"Adjusted robot states frame range: {adjusted_state_frames.min()} to {adjusted_state_frames.max()}")
            
            # Create state background by mapping states to visibility frame range
            visibility_frame_min = df['frame'].min()
            visibility_frame_max = df['frame'].max()
            
            # Create a mapping from frames to states
            state_dict = {}
            for i, frame in enumerate(adjusted_state_frames):
                state_dict[frame] = states_data['states'][i]
            
            # Fill in states for the entire visibility range
            prev_state = 'unknown'
            prev_frame = visibility_frame_min
            
            # Sort the state frames that overlap with visibility range
            relevant_state_frames = [f for f in adjusted_state_frames 
                                   if visibility_frame_min <= f <= visibility_frame_max]
            relevant_state_frames = sorted(relevant_state_frames)
            
            print(f"Found {len(relevant_state_frames)} relevant state frames")
            
            # If no relevant frames, use the closest states
            if not relevant_state_frames:
                # Find closest state before and after
                before_frames = [f for f in adjusted_state_frames if f < visibility_frame_min]
                after_frames = [f for f in adjusted_state_frames if f > visibility_frame_max]
                
                if before_frames:
                    closest_before = max(before_frames)
                    closest_state = state_dict[closest_before]
                    # Use this state for the entire range
                    color = self.state_colors.get(closest_state, '#F5F5F5')
                    ax.axvspan(visibility_frame_min, visibility_frame_max, alpha=0.3, color=color, zorder=0)
                    print(f"Using closest state '{closest_state}' for entire range")
                else:
                    print("No robot state data overlaps with ball visibility data")
            else:
                # Draw state segments
                for i, frame in enumerate(relevant_state_frames):
                    current_state = state_dict[frame]
                    
                    if i == 0:
                        # First state - check if we need to extend backwards
                        start_frame = visibility_frame_min
                    else:
                        start_frame = prev_frame
                    
                    if i == len(relevant_state_frames) - 1:
                        # Last state - extend to end
                        end_frame = visibility_frame_max
                    else:
                        end_frame = frame
                    
                    # Draw this state
                    if prev_state != 'unknown':
                        color = self.state_colors.get(prev_state, '#F5F5F5')
                        ax.axvspan(start_frame, end_frame, alpha=0.3, color=color, zorder=0)
                        print(f"State '{prev_state}': frames {start_frame} to {end_frame}")
                    
                    prev_state = current_state
                    prev_frame = frame
                
                # Draw the final state
                if prev_state != 'unknown':
                    color = self.state_colors.get(prev_state, '#F5F5F5')
                    ax.axvspan(prev_frame, visibility_frame_max, alpha=0.3, color=color, zorder=0)
                    print(f"Final state '{prev_state}': frames {prev_frame} to {visibility_frame_max}")
            
            print(f"Added robot states background from Robot {log_id} (Player {player_num})")
        
        # Plot team ball visibility on top
        ax.step(df['frame'], df['team_visibility'], where='post', linewidth=3, color='darkred', zorder=2, label='Team Ball Visibility')
        ax.fill_between(df['frame'], 0, df['team_visibility'], step='post', alpha=0.6, color='red', zorder=1)
        
        # Customize the plot
        ax.set_xlabel('Frame Number (Synchronized)', fontsize=14)
        ax.set_ylabel('Team Ball Visibility', fontsize=14)
        
        # Create title
        title = f'Team Ball Visibility with Robot States Background (Full Duration)'
        if self.event_name != "Unknown_Event" and self.game_name != "Unknown_Game":
            title += f'\n{self.event_name} - {self.game_name}'
        
        ax.set_title(title, fontsize=16, pad=20)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Ball Not Visible', 'Ball Visible'])
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add statistics
        visible_frames = df['team_visibility'].sum()
        total_frames = len(df)
        visibility_percent = (visible_frames / total_frames) * 100 if total_frames > 0 else 0
        
        stats_text = f"Team Visibility: {visibility_percent:.1f}% ({visible_frames}/{total_frames} frames)"
        ax.text(0.02, 0.95, stats_text, transform=ax.transAxes, fontsize=12, 
               bbox={"facecolor":"white", "alpha":0.9, "pad":5}, verticalalignment='top')
        
        # Add frame range info
        frame_range = f"Frames: {df['frame'].iloc[0]:.0f} to {df['frame'].iloc[-1]:.0f}"
        ax.text(0.98, 0.95, frame_range, transform=ax.transAxes, ha='right', fontsize=12, 
               bbox={"facecolor":"white", "alpha":0.9, "pad":5}, verticalalignment='top')
        
        # Add robot states info
        if self.robot_states_data is not None:
            states_info = f"Robot States: Player {self.robot_states_data['player_num']} (Log {self.robot_states_data['log_id']})"
            ax.text(0.02, 0.05, states_info, transform=ax.transAxes, fontsize=10, 
                   bbox={"facecolor":"white", "alpha":0.9, "pad":3}, verticalalignment='bottom')
        
        # Create comprehensive legend
        legend_elements = []
        
        # Add team visibility
        legend_elements.append(mpatches.Patch(color='red', alpha=0.6, label='Team Ball Visibility'))
        
        # Add robot states from the background
        if self.robot_states_data is not None:
            states_in_plot = set(self.robot_states_data['states'])
            for state in sorted(states_in_plot):
                color = self.state_colors.get(state, '#F5F5F5')
                legend_elements.append(mpatches.Patch(color=color, alpha=0.3, label=f'{state.title()} State'))
        
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
        
        plt.tight_layout()
        
        # Save the plot
        output_dir = Path("team_analysis_plots")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename
        filename_parts = ["team_visibility_with_states_full"]
        if self.event_name != "Unknown_Event":
            filename_parts.append(self.event_name)
        if self.game_name != "Unknown_Game":
            filename_parts.append(self.game_name)
        filename_parts.append(timestamp)
        
        plot_filename = "_".join(filename_parts) + ".png"
        plot_file = output_dir / plot_filename
        
        plt.savefig(plot_file, dpi=300, bbox_inches='tight')
        print(f"Saved combined plot to {plot_file}")
        
        plt.show()
        
        return plot_file, plot_filename
    
    def create_summary_table(self):
        """Create a simplified summary table that gets appended to a master file"""
        print("Creating simplified summary table...")
        
        if self.team_visibility_data is None:
            print("No team visibility data available for summary")
            return None, None
        
        df = self.team_visibility_data
        
        # Calculate team visibility statistics
        team_visible_frames = df['team_visibility'].sum()
        total_frames = len(df)
        team_visibility_percent = (team_visible_frames / total_frames) * 100 if total_frames > 0 else 0
        
        # Get player numbers from log info
        player_numbers = []
        for log_id in self.log_ids:
            if log_id in self.log_info:
                player_num = self.log_info[log_id].get('player', None)
                if player_num is not None:
                    player_numbers.append(player_num)
        
        # If no player numbers found, use log IDs
        if not player_numbers:
            player_numbers = list(self.robot_visibility.keys())
        
        # Sort player numbers to get consistent ordering
        player_numbers = sorted(set(player_numbers))
        max_players = max(player_numbers) if player_numbers else 7
        
        print(f"  Organizing data for players: {player_numbers}")
        
        # Create simplified summary record
        summary_record = {
            'event': self.event_name,
            'game': self.game_name,
            'analysis_timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'team_visibility_percent': round(team_visibility_percent, 2),
        }
        
        # Add individual player visibility percentages
        individual_percentages = []
        for player_num in range(1, max_players + 1):
            # Find the log_id for this player
            log_id_for_player = None
            for log_id in self.log_ids:
                if log_id in self.log_info:
                    if self.log_info[log_id].get('player') == player_num:
                        log_id_for_player = log_id
                        break
            
            # If we didn't find by player number, try to match by position in list
            if log_id_for_player is None and player_num <= len(self.log_ids):
                # Fallback: use log IDs in order
                sorted_log_ids = sorted(self.log_ids)
                if player_num - 1 < len(sorted_log_ids):
                    log_id_for_player = sorted_log_ids[player_num - 1]
            
            # Calculate visibility for this player
            if log_id_for_player and log_id_for_player in self.robot_visibility:
                robot_data = self.robot_visibility[log_id_for_player]
                
                # Calculate visibility percentage for this player
                individual_visible = 0
                individual_frames = 0
                
                # Map robot data to synchronized frames
                if log_id_for_player in self.playing_frames:
                    reference_frame = min(self.playing_frames.values())
                    playing_frame = self.playing_frames[log_id_for_player]
                    offset = playing_frame - reference_frame
                    
                    # Find overlapping frames with team data
                    robot_frames = robot_data['frames'] - offset
                    for i, frame in enumerate(robot_frames):
                        if frame >= df['frame'].min() and frame <= df['frame'].max():
                            individual_frames += 1
                            if robot_data['visibility'][i] == 1:
                                individual_visible += 1
                
                individual_percent = (individual_visible / individual_frames * 100) if individual_frames > 0 else 0
                summary_record[f'player_{player_num}_visibility_percent'] = round(individual_percent, 2)
                individual_percentages.append(individual_percent)
            else:
                # Player not found or no data
                summary_record[f'player_{player_num}_visibility_percent'] = 0.0
        
        # Calculate average individual visibility from players with data
        avg_individual = np.mean([perc for perc in individual_percentages if perc > 0]) if individual_percentages else 0
        summary_record['average_individual_visibility_percent'] = round(avg_individual, 2)
        
        # Add robot count info
        summary_record['total_robots'] = len(self.log_ids)
        summary_record['robots_with_data'] = len(self.robot_visibility)
        
        # Create DataFrame with this single record
        new_summary_df = pd.DataFrame([summary_record])
        
        # Define the master table file
        output_dir = Path("team_analysis_tables")
        output_dir.mkdir(exist_ok=True)
        master_table_file = output_dir / "master_team_summary.csv"
        
        # Check if master table exists
        if master_table_file.exists():
            try:
                # Load existing master table
                existing_df = pd.read_csv(master_table_file)
                print(f"  Loading existing master table with {len(existing_df)} records")
                
                # Append new record
                combined_df = pd.concat([existing_df, new_summary_df], ignore_index=True)
                print(f"  Appending new record to master table")
                
            except Exception as e:
                print(f"  Error reading existing master table: {e}")
                print(f"  Creating new master table")
                combined_df = new_summary_df
        else:
            print(f"  Creating new master table")
            combined_df = new_summary_df
        
        # Save the combined table
        combined_df.to_csv(master_table_file, index=False)
        print(f"Saved master summary table to {master_table_file}")
        print(f"Master table now contains {len(combined_df)} records")
        
        # Also save individual game summary
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_parts = ["game_summary"]
        if self.event_name != "Unknown_Event":
            filename_parts.append(self.event_name)
        if self.game_name != "Unknown_Game":
            filename_parts.append(self.game_name)
        filename_parts.append(timestamp)
        
        individual_csv_filename = "_".join(filename_parts) + ".csv"
        individual_csv_file = output_dir / individual_csv_filename
        new_summary_df.to_csv(individual_csv_file, index=False)
        print(f"Saved individual game summary to {individual_csv_file}")
        
        # Print summary to console
        print(f"\nSUMMARY STATISTICS:")
        print(f"Event: {self.event_name}, Game: {self.game_name}")
        print(f"Team Visibility: {team_visibility_percent:.2f}%")
        print(f"Average Individual Visibility: {avg_individual:.2f}%")
        print(f"Individual Player Visibility:")
        for player_num in range(1, max_players + 1):
            visibility = summary_record[f'player_{player_num}_visibility_percent']
            if visibility > 0:
                print(f"  Player {player_num}: {visibility:.2f}%")
        
        return combined_df, master_table_file
    
    def run_analysis(self):
        """Run the complete simplified analysis for full duration"""
        print("Starting simplified team analysis...")
        print(f"Event: {self.event_name}")
        print(f"Game: {self.game_name}")
        print()
        
        # Load ball visibility data
        self.load_ball_visibility_data()
        if not self.robot_visibility:
            print("Failed to load ball visibility data")
            return False
        
        # Load robot states data for background
        self.load_robot_states_data()
        
        # Synchronize team visibility
        team_data = self.synchronize_team_visibility()
        if team_data is None:
            print("Failed to synchronize team visibility")
            return False
        
        # Create combined plot for full duration
        plot_file, plot_filename = self.create_combined_plot()
        if plot_file is None:
            print("Failed to create combined plot")
            return False
        
        # Create summary table
        summary_df, summary_file = self.create_summary_table()
        if summary_df is None:
            print("Failed to create summary table")
            return False
        
        print("Simplified team analysis completed successfully!")
        return True

def main():
    """Main function to run simplified team analysis"""
    
    # Create output directory for console logs
    output_dir = Path("team_analysis_plots")
    output_dir.mkdir(exist_ok=True)
    
    # Create console log filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_console_log_filename = f"simplified_team_analysis_{timestamp}_console.txt"
    temp_console_log_path = output_dir / temp_console_log_filename
    
    # Run analysis with console output capture
    with ConsoleCapture(temp_console_log_path):
        print(f"=== SIMPLIFIED TEAM ANALYSIS ===")
        print(f"Analysis started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Create analyzer
        analyzer = SimplifiedTeamAnalyzer(LOG_IDS, INPUT_DIR)
        
        # Update console log filename with auto-detected info
        filename_parts = ["simplified_team_analysis"]
        if analyzer.event_name != "Unknown_Event":
            filename_parts.append(analyzer.event_name)
        if analyzer.game_name != "Unknown_Game":
            filename_parts.append(analyzer.game_name)
        filename_parts.append(timestamp)
        
        final_console_log_filename = "_".join(filename_parts) + "_console.txt"
        final_console_log_path = output_dir / final_console_log_filename
        
        print(f"Console output will be saved to: {final_console_log_path}")
        print()
        
        # Run full analysis
        print("=== Full Analysis (Complete Duration) ===")
        success = analyzer.run_analysis()
        
        if success:
            print(f"\nAnalysis completed successfully!")
            print(f"\nOutput files:")
            print(f"- Combined plot: team_analysis_plots/")
            print(f"- Master summary table: team_analysis_tables/master_team_summary.csv")
            print(f"- Individual game summary: team_analysis_tables/")
            print(f"- Console log: {final_console_log_path}")
        else:
            print(f"\nAnalysis failed!")
        
        print(f"Analysis ended at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Rename console log
    if temp_console_log_path.exists() and temp_console_log_path != final_console_log_path:
        temp_console_log_path.rename(final_console_log_path)
        print(f"\nConsole output saved to: {final_console_log_path}")
    else:
        print(f"\nConsole output saved to: {temp_console_log_path}")

if __name__ == "__main__":
    main()