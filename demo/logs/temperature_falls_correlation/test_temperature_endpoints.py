from vaapi.client import Vaapi
import os

def get_sensor_joint_data_by_log(client, log_id=113):
    """Get sensor joint data using the correct method"""
    
    print(f"🌡️ Getting sensor joint data for log {log_id}:")
    
    try:
        # Motion data uses list() method, not filter()
        all_sensor_data = client.sensorjointdata.list()
        
        print(f"  Found {len(all_sensor_data)} total sensor entries")
        
        # Filter by log_id manually (since there's no filter method)
        log_sensor_data = [entry for entry in all_sensor_data 
                          if hasattr(entry, 'log_id') and entry.log_id == log_id]
        
        print(f"  Found {len(log_sensor_data)} entries for log {log_id}")
        
        if log_sensor_data:
            # Examine structure
            sample = log_sensor_data[0]
            print(f"  Sample entry type: {type(sample)}")
            if hasattr(sample, '__dict__'):
                print(f"  Available attributes: {list(sample.__dict__.keys())}")
                
                # Look for temperature data
                for key, value in sample.__dict__.items():
                    if 'temp' in key.lower():
                        print(f"    🌡️ Temperature field: {key} = {value}")
        
        return log_sensor_data
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return []

def get_falls_and_temperatures_from_api(client, log_id):
    """Get both falls and temperatures for a single log using API"""
    
    print(f"\n📊 Processing log {log_id}:")
    
    # 1. Get fall data (we know this works when API is up)
    fall_count = 0
    try:
        fall_states = [
            "falling_front", "falling_back", "falling"
        ]
        
        all_fall_frames = []
        for state in fall_states:
            response = client.behavior_frame_option.filter(
                log=log_id,
                option_name="fall_down_and_stand_up", 
                state_name=state,
            )
            frames = [frame.frame_number for frame in response]
            all_fall_frames.extend(frames)
        
        fall_count = len(set(all_fall_frames))  # Unique frames
        print(f"  Falls: {fall_count}")
        
    except Exception as e:
        print(f"  ❌ Error getting falls: {e}")
    
    # 2. Get temperature data
    max_temps = {}
    try:
        sensor_data = get_sensor_joint_data_by_log(client, log_id)
        
        if sensor_data:
            # Process temperature data
            temperatures = []
            for entry in sensor_data:
                # You'll need to adjust based on actual data structure
                if hasattr(entry, 'temperature_data'):  # Example field name
                    temperatures.append(entry.temperature_data)
            
            if temperatures:
                max_temps = {
                    'max_temp': max(temperatures),
                    'avg_temp': sum(temperatures) / len(temperatures)
                }
        
    except Exception as e:
        print(f"  ❌ Error getting temperatures: {e}")
    
    return {
        'log_id': log_id,
        'fall_count': fall_count,
        'temperatures': max_temps
    }

def test_api_when_working(client):
    """Test the corrected API calls"""
    
    print("🔧 Testing corrected API methods...")
    
    # Test logs that we know have data
    test_logs = [111, 112, 113]
    
    results = []
    for log_id in test_logs:
        try:
            result = get_falls_and_temperatures_from_api(client, log_id)
            results.append(result)
        except Exception as e:
            print(f"❌ Error with log {log_id}: {e}")
    
    return results

if __name__ == "__main__":
    
    print("🔧 Testing corrected temperature data access...")
    
    # Connect to API  
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    
    # Test when API is working
    results = test_api_when_working(client)
    
    print(f"\n📋 Results: {results}")