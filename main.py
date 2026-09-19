"""
Entry point for Offline AI Human Motion Simulator.
"""

import sys
import os

# Ensure root directory is on python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.application import MotionSimulatorApp
from app.logger import logger
from ui.main_window import MainWindow

def main():
    try:
        app = MotionSimulatorApp(sys.argv)
        sys.exit(app.run(MainWindow))
    except Exception as e:
        logger.exception(f"Unhandled exception in main application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
