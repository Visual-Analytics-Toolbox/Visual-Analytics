from vaapi.client import Vaapi
import os
import pandas as pd

def test_api_connection():
    """Test basic API connection"""
    try:
        client = Vaapi(
            base_url=os.environ.get("VAT_API_URL"),
            api_key=os.environ.get("VAT_API_TOKEN"),
        )
        print("✅ API connection established")
        return client
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return None

def test_fall_detection(client, log_id=282):
    """Test fall detection using the method from your example"""
    
    print(f"\n📊 Testing fall detection for log {log_id}:")
    
    fall_states = [
        "falling_front",
        "falling_front_wait", 
        "falling_back",
        "falling_back_wait",
        "falling",
        "wait_before_stand_up",
        "stand_up",
        "stand",
        "wait_for_completed_stand"
    ]
    
    all_fall_frames = []
    
    for state in fall_states:
        try:
            response = client.behavior_frame_option.filter(
                log=log_id,
                option_name="fall_down_and_stand_up",
                state_name=state,
            )
            frame_numbers = [frame.frame_number for frame in response]
            
            if frame_numbers:
                print(f"  {state}: {len(frame_numbers)} frames")
                if state in ["falling_front", "falling_back", "falling"]:
                    all_fall_frames.extend(frame_numbers)
            else:
                print(f"  {state}: 0 frames")
                
        except Exception as e:
            print(f"  ❌ Error querying {state}: {e}")
    
    # Count unique fall events (not frames)
    unique_fall_frames = sorted(set(all_fall_frames))
    print(f"\n  Total unique fall frames: {len(unique_fall_frames)}")
    
    return len(unique_fall_frames)

def explore_available_endpoints(client):
    """Explore what endpoints/methods are available"""
    
    print(f"\n🔍 Exploring available client methods:")
    
    # Print available attributes/methods
    client_methods = [attr for attr in dir(client) if not attr.startswith('_')]
    print("Available client endpoints:")
    for method in client_methods:
        print(f"  - {method}")
    
    return client_methods

def test_temperature_endpoints(client, log_id=282):
    """Try to find temperature data endpoints"""
    
    print(f"\n🌡️ Searching for temperature data for log {log_id}:")
    
    # Try common temperature-related endpoint names
    potential_temp_endpoints = [
        'temperature',
        'joint_temperature', 
        'sensor_data',
        'joint_data',
        'motor_data',
        'behavior_frame_input',  # This might contain temperature data
        'sensor_frame',
        'joint_frame'
    ]
    
    for endpoint_name in potential_temp_endpoints:
        if hasattr(client, endpoint_name):
            print(f"  ✅ Found endpoint: {endpoint_name}")
            try:
                # Try to get some data to see structure
                endpoint = getattr(client, endpoint_name)
                if hasattr(endpoint, 'filter'):
                    response = endpoint.filter(log=log_id)
                    print(f"    Sample response type: {type(response)}")
                    if hasattr(response, '__iter__'):
                        sample = list(response)[:1]  # Get first item
                        if sample:
                            print(f"    Sample data keys: {list(sample[0].__dict__.keys()) if hasattr(sample[0], '__dict__') else 'No dict'}")
                elif hasattr(endpoint, 'list'):
                    response = endpoint.list(log=log_id)
                    print(f"    List response type: {type(response)}")
            except Exception as e:
                print(f"    ❌ Error accessing {endpoint_name}: {e}")
        else:
            print(f"  ❌ No endpoint: {endpoint_name}")

def test_behavior_frame_input(client, log_id=282):
    """Test behavior_frame_input which might contain temperature data"""
    
    print(f"\n🔍 Testing behavior_frame_input for log {log_id}:")
    
    try:
        # Try to get behavior frame input data
        if hasattr(client, 'behavior_frame_input'):
            response = client.behavior_frame_input.filter(log=log_id)
            sample_frames = list(response)[:5]  # Get first 5 frames
            
            if sample_frames:
                print(f"  Found {len(sample_frames)} sample frames")
                for i, frame in enumerate(sample_frames):
                    print(f"  Frame {i} attributes: {list(frame.__dict__.keys()) if hasattr(frame, '__dict__') else 'No attributes'}")
                    
                    # Look for temperature-related fields
                    if hasattr(frame, '__dict__'):
                        for key, value in frame.__dict__.items():
                            if 'temp' in key.lower() or 'joint' in key.lower():
                                print(f"    🌡️ Temperature/Joint field: {key} = {value}")
            else:
                print("  No frames found")
        else:
            print("  behavior_frame_input endpoint not available")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")

def test_with_multiple_logs(client, log_ids=[111, 112, 113]):
    """Test fall detection with multiple log IDs from your CSV"""
    
    print(f"\n📊 Testing multiple logs: {log_ids}")
    
    results = []
    
    for log_id in log_ids:
        try:
            fall_count = test_fall_detection(client, log_id)
            results.append({
                'log_id': log_id,
                'fall_count': fall_count,
                'status': 'success'
            })
        except Exception as e:
            print(f"❌ Error processing log {log_id}: {e}")
            results.append({
                'log_id': log_id, 
                'fall_count': 0,
                'status': f'error: {e}'
            })
    
    # Print summary
    print(f"\n📋 Summary:")
    for result in results:
        print(f"  Log {result['log_id']}: {result['fall_count']} falls ({result['status']})")
    
    return results

if __name__ == "__main__":
    
    print("🚀 Testing API connection and endpoints...")
    
    # Test 1: Basic connection
    client = test_api_connection()
    if not client:
        exit(1)
    
    # Test 2: Explore available endpoints
    available_methods = explore_available_endpoints(client)
    
    # Test 3: Test fall detection with example log
    test_fall_detection(client, log_id=282)
    
    # Test 4: Search for temperature endpoints
    test_temperature_endpoints(client)
    
    # Test 5: Test behavior frame input
    test_behavior_frame_input(client)
    
    # Test 6: Test with your actual log IDs
    print(f"\n" + "="*50)
    print("Testing with your actual log IDs:")
    test_log_ids = [111, 112, 113]  # From your CSV
    test_with_multiple_logs(client, test_log_ids)
    
    print(f"\n✅ API testing complete!")