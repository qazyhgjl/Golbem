"""
Scene state management for Golbem Simulator.
"""

from skeleton.skeleton import Skeleton
from engine.camera import Camera
from engine.lighting import Lighting
from engine.asset_pipeline import AssetPipeline
from app.settings import MODE_SKIN

class Scene:
    def __init__(self):
        self.skeleton = Skeleton()
        self.camera = Camera()
        self.lighting = Lighting()
        self.asset_pipeline = AssetPipeline()
        self.display_mode = MODE_SKIN
        self.show_grid = True
        self.selected_item_name = None # Selected joint, bone, muscle, or organ

    def set_display_mode(self, mode: str):
        self.display_mode = mode

    def select_item(self, item_name: str):
        self.selected_item_name = item_name
