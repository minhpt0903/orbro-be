import multiprocessing
import uvicorn
import signal
import sys
import os
from api import app  # Import FastAPI app from api.py
from tag_simulator import simulate  # Import simulate function from tag_simulator.py

def run_api():
    """Run the FastAPI server."""
    uvicorn.run(app, host="0.0.0.0", port=8100)

def run_simulator():
    """Run the tag simulator."""
    try:
        simulate()
    except SystemExit:
        print("Simulator process terminated.")

def signal_handler(sig, frame):
    """Handle SIGINT (Ctrl+C) to terminate both processes gracefully."""
    print("\nShutting down both API and simulator...")
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    # Ensure log directory exists (as required by tag_simulator.py)
    os.makedirs("./log", exist_ok=True)

    # Create processes for API and simulator
    api_process = multiprocessing.Process(target=run_api, name="FastAPI")
    simulator_process = multiprocessing.Process(target=run_simulator, name="Simulator")

    # Start both processes
    api_process.start()
    simulator_process.start()

    try:
        # Wait for both processes to complete (they won't unless terminated)
        api_process.join()
        simulator_process.join()
    except KeyboardInterrupt:
        # Terminate processes on Ctrl+C
        print("\nTerminating processes...")
        api_process.terminate()
        simulator_process.terminate()
        api_process.join()
        simulator_process.join()
        print("All processes terminated.")