import sys
import os

# Ensure parent directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from main import run_simulation
import asyncio

if __name__ == "__main__":
    asyncio.run(run_simulation())
