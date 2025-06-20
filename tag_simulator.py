import time
from datetime import datetime
import uuid
import logging
import os
import aiofiles
import json

# Create log directory if it doesn't exist
log_dir = "./log"
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_dir, 'simulator_tag_data.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Tag IDs and storage for last CNT and timestamp
tag_ids = [str(uuid.uuid4())[:12] for _ in range(3)]
tag_data = {tag_id: {'cnt': None, 'timestamp': None} for tag_id in tag_ids}
global_cnt = 0  # Global counter to ensure unique, incrementing cnt

def generate_tag_data():
    """Generate simulated tag data for all tags with globally unique cnt."""
    global global_cnt
    data_list = []
    
    # Update all 3 tags in each iteration
    for tag_id in tag_ids:
        global_cnt += 1  # Increment global counter
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S.%f")[:15]
        
        # Log if this tag had a previous cnt
        if tag_data[tag_id]['cnt'] is not None:
            logging.info(
                f"Tag {tag_id}: CNT changed from {tag_data[tag_id]['cnt']} to "
                f"{global_cnt}, Timestamp: {timestamp}"
            )
        
        # Update stored data for the tag
        tag_data[tag_id]['cnt'] = global_cnt
        tag_data[tag_id]['timestamp'] = timestamp
        
        # Format the data string for this tag
        data = f"TAG,{tag_id},{global_cnt},{timestamp}"
        data_list.append(data)
    
    return data_list

async def save_tag_data():
    """Save current tag data to JSON file asynchronously."""
    async with aiofiles.open(os.path.join(log_dir, 'simulator_tag_data_storage.json'), 'w') as f:
        await f.write(json.dumps(tag_data, indent=4))

def simulate():
    """Main simulation loop, runs until interrupted."""
    try:
        while True:  # Run indefinitely until interrupted
            data_list = generate_tag_data()
            for data in data_list:
                print(data)  # Output to standard output
            # Run async save_tag_data in a synchronous context
            import asyncio
            asyncio.run(save_tag_data())  # Save current state
            time.sleep(1)  # Delay to simulate periodic increment
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
        # Save final state before exiting
        import asyncio
        asyncio.run(save_tag_data())
        raise SystemExit

if __name__ == "__main__":
    simulate()