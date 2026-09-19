"""
Main Application Controller.
"""

import sys
from PySide6.QtWidgets import QApplication
from app.settings import APP_NAME, APP_VERSION
from app.logger import logger

class MotionSimulatorApp:
    def __init__(self, sys_argv):
        self.app = QApplication(sys_argv)
        self.app.setApplicationName(APP_NAME)
        self.app.setApplicationVersion(APP_VERSION)
        logger.info(f"Initializing {APP_NAME} v{APP_VERSION}")

    def run(self, main_window_class):
        self.window = main_window_class()
        self.window.show()
        return self.app.exec()
