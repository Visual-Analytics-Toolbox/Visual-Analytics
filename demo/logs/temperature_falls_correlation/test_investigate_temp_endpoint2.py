from vaapi.client import Vaapi
import os
import json

def get_one_sensorjointdata_example(client):
    """Get the simplest possible example from SensorJointData endpoint"""
    
    print("🔍 Attempting to get ONE example from SensorJointData...")
    
    try:
        # Try to get just count first
        count = client.sensorjointdata.get_repr_count()
        print(f"✅ Total SensorJointData entries: {count}")
        
        if count > 0:
            # Try to get the very first entry
            print(f"\n📊 Attempting to get entry ID 1...")
            entry = client.sensorjointdata.get(1)
            
            print(f"✅ SUCCESS! Got entry:")
            print(f"  Type: {type(entry)}")
            print(f"  ID: {entry.id}")
            print(f"  Frame: {entry.frame}")
            print(f"  Frame number: {entry.frame_number}")
            print(f"  Size: {entry.size}")
            print(f"  Start pos: {entry.start_pos}")
            
            print(f"\n🎯 REPRESENTATION DATA:")
            repr_data = entry.representation_data
            print(f"  Type: {type(repr_data)}")
            
            if isinstance(repr_data, dict):
                print(f"  Dict with {len(repr_data)} keys:")
                for key, value in repr_data.items():
                    print(f"    {key}: {value}")
                    
            elif isinstance(repr_data, str):
                print(f"  String length: {len(repr_data)}")
                print(f"  First 200 chars: {repr_data[:200]}")
                
                # Try to parse as JSON
                try:
                    parsed = json.loads(repr_data)
                    print(f"  ✅ Parsed as JSON:")
                    if isinstance(parsed, dict):
                        print(f"    Dict with {len(parsed)} keys:")
                        for key, value in list(parsed.items())[:10]:  # First 10 keys
                            if isinstance(value, (list, dict)) and len(str(value)) > 100:
                                print(f"      {key}: <{type(value).__name__} with {len(value)} items>")
                            else:
                                print(f"      {key}: {value}")
                    elif isinstance(parsed, list):
                        print(f"    List with {len(parsed)} items:")
                        for i, item in enumerate(parsed[:5]):  # First 5 items
                            print(f"      [{i}]: {item}")
                except Exception as parse_error:
                    print(f"  ❌ Not JSON: {parse_error}")
            else:
                print(f"  Other type, value: {repr_data}")
            
            return entry
            
        else:
            print("❌ No entries found")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    
    print("🔧 Simple SensorJointData investigation - ONE example only")
    
    # Connect to API
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    
    # Get one example
    example = get_one_sensorjointdata_example(client)
    
    if example:
        print(f"\n🎉 SUCCESS! We have sensor joint data structure!")
    else:
        print(f"\n❌ Could not retrieve sensor joint data")