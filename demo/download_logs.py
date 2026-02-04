import os
import json
from pathlib import Path
import time

# Import your API client
try:
    from vaapi.client import Vaapi
except ImportError:
    print("Warning: Unable to import Vaapi client. Make sure it's installed.")

# ===== MODIFY THESE LOG IDs FOR YOUR TESTING =====
LOG_START, LOG_END = 83, 89  # Replace with your actual log IDs
LOG_IDS = list(range(LOG_START, LOG_END + 1))

OUTPUT_DIR = 'downloaded_logs'
# ================================================

def download_and_save_log(client, log_id, base_dir):
    """Download BallModel and TeamState data for a specific log and save locally"""
    # Create directory structure
    log_dir = Path(base_dir) / str(log_id)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if data already exists
    ball_model_file = log_dir / "ball_model.json"
    team_state_file = log_dir / "team_state.json"
    log_info_file = log_dir / "log_info.json"
    
    # Get log info
    try:
        response = client.logs.get(log_id)
        log_info = {
            'id': log_id,
            'event': response.event_name if hasattr(response, 'event_name') else "Unknown",
            'game': response.game_name if hasattr(response, 'game_name') else "Unknown",
            'player': response.player_number if hasattr(response, 'player_number') else "Unknown"
        }
        
        # Save log info
        with open(log_info_file, 'w') as f:
            json.dump(log_info, f, indent=2)
            
        print(f"Saved log info for log ID {log_id}")
    except Exception as e:
        print(f"Error fetching log info for log ID {log_id}: {e}")
    
    # Download ball model data if it doesn't exist
    if not ball_model_file.exists():
        try:
            print(f"Downloading ball model data for log ID {log_id}...")
            response = client.ballmodel.list(log=log_id)  # Changed from log_id=log_id to log=log_id
            
            if response and len(response) > 0:
                # Convert to serializable format
                ball_model_data = []
                for entry in response:
                    item = {}
                    for attr in dir(entry):
                        if not attr.startswith('_') and attr != 'json':
                            value = getattr(entry, attr)
                            if hasattr(value, '__dict__'):
                                continue  # Skip nested objects for simplicity
                            item[attr] = value
                    
                    # Parse representation_data if it's a string
                    if 'representation_data' in item and isinstance(item['representation_data'], str):
                        try:
                            item['representation_data'] = json.loads(item['representation_data'])
                        except:
                            pass  # Keep as string if can't parse
                    
                    ball_model_data.append(item)
                
                # Save to file
                with open(ball_model_file, 'w') as f:
                    json.dump(ball_model_data, f, indent=2)
                
                print(f"Saved {len(ball_model_data)} ball model entries to {ball_model_file}")
            else:
                print(f"No ball model data found for log ID {log_id}")
        except Exception as e:
            print(f"Error downloading ball model data for log ID {log_id}: {e}")
            return False
    else:
        print(f"Ball model data already exists for log ID {log_id}")
    
    # Download team state data if it doesn't exist
    if not team_state_file.exists():
        try:
            print(f"Downloading team state data for log ID {log_id}...")
            response = client.teamstate.list(log=log_id)
            
            if response and len(response) > 0:
                # Convert to serializable format
                team_state_data = []
                for entry in response:
                    item = {}
                    for attr in dir(entry):
                        if not attr.startswith('_') and attr != 'json':
                            value = getattr(entry, attr)
                            if hasattr(value, '__dict__'):
                                continue  # Skip nested objects for simplicity
                            item[attr] = value
                    
                    # Parse representation_data if it's a string
                    if 'representation_data' in item and isinstance(item['representation_data'], str):
                        try:
                            item['representation_data'] = json.loads(item['representation_data'])
                        except:
                            pass  # Keep as string if can't parse
                    
                    team_state_data.append(item)
                
                # Save to file
                with open(team_state_file, 'w') as f:
                    json.dump(team_state_data, f, indent=2)
                
                print(f"Saved {len(team_state_data)} team state entries to {team_state_file}")
            else:
                print(f"No team state data found for log ID {log_id}")
        except Exception as e:
            print(f"Error downloading team state data for log ID {log_id}: {e}")
            return False
    else:
        print(f"Team state data already exists for log ID {log_id}")
    
    return True


def main():
    """Main function for downloading logs"""
    # Initialize API client
    try:
        client = Vaapi(
            base_url=os.environ.get("VAT_API_URL"),
            api_key=os.environ.get("VAT_API_TOKEN"),
        )
    except Exception as e:
        print(f"Error initializing API client: {e}")
        print("Make sure VAT_API_URL and VAT_API_TOKEN environment variables are set")
        return
    
    # Download logs
    print(f"\nDownloading logs: {LOG_IDS} to directory: {OUTPUT_DIR}")
    
    for log_id in LOG_IDS:
        print(f"\nProcessing log ID: {log_id}")
        success = download_and_save_log(client, log_id, OUTPUT_DIR)
        
        if success:
            print(f"Successfully downloaded data for log ID {log_id}")
        else:
            print(f"Failed to download data for log ID {log_id}")
        
        # Add a small delay to avoid overwhelming the server
        time.sleep(1)
    
    print("\nDownload process completed!")


if __name__ == "__main__":
    main()