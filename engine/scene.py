"""
Scene state management.
"""

from skeleton.skeleton import Skeleton
from engine.camera import Camera
from engine.lighting import Lighting
from app.settings import MODE_SKIN

class Scene:
    def __init__(self):
        self.skeleton = Skeleton()
        self.camera = Camera()
        self.lighting = Lighting()
        self.display_mode = MODE_SKIN
        self.show_grid = True

    def set_display_mode(self, mode: str):
        self.display_mode = mode
