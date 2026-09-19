"""
Global application settings and constants.
"""

import os

# Application Metadata
APP_NAME = "Offline AI Human Motion Simulator"
APP_VERSION = "1.0.0"
ORGANIZATION_NAME = "BioMotion Dynamics"

# Display Settings
DEFAULT_WINDOW_WIDTH = 1280
DEFAULT_WINDOW_HEIGHT = 800
TARGET_FPS = 60

# Colors (RGBA) - Sci-Fi Cyberpunk Dark Theme
COLOR_BG_DARK = (0.05, 0.07, 0.10, 1.0)
COLOR_GRID = (0.15, 0.25, 0.35, 0.5)
COLOR_SKIN = (0.2, 0.6, 0.8, 0.85)             # Semi-transparent sci-fi cyan skin
COLOR_SKIN_TRANSPARENT = (0.2, 0.6, 0.8, 0.25) # Highly transparent skin
COLOR_BONES = (0.85, 0.92, 1.0, 0.95)          # Bright whitish-blue skeletal bones
COLOR_MUSCLES = (0.85, 0.25, 0.3, 0.75)        # Crimson/magenta semi-translucent muscles
COLOR_JOINTS = (1.0, 0.55, 0.0, 1.0)           # High-visibility glowing orange joint markers
COLOR_HIGHLIGHT = (0.0, 0.9, 1.0, 1.0)         # Bright cyan highlight

# Rendering Display Modes
MODE_SKIN = "Skin Mode"
MODE_TRANSPARENT_SKIN = "Transparent Skin Mode"
MODE_SKELETON = "Skeleton Mode"
MODE_MUSCLES = "Muscles Mode"
MODE_XRAY = "X-Ray Mode"
MODE_JOINT_DEBUG = "Joint Debug Mode"

DISPLAY_MODES = [
    MODE_SKIN,
    MODE_TRANSPARENT_SKIN,
    MODE_SKELETON,
    MODE_MUSCLES,
    MODE_XRAY,
    MODE_JOINT_DEBUG,
]

# Path Constants
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
MODELS_DIR = os.path.join(ROOT_DIR, "models")
