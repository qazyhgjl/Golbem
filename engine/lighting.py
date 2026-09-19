"""
Lighting controller for Sci-Fi Sci-Medical 3D viewport.
"""

class Lighting:
    def __init__(self):
        # Sci-Fi Cyan/Blue key light & fill light
        self.key_light_dir = (0.5, 1.0, 0.8)
        self.key_light_color = (0.0, 0.85, 1.0) # Bright Cyan
        self.fill_light_dir = (-0.5, 0.5, -0.5)
        self.fill_light_color = (0.2, 0.3, 0.6) # Deep Blue
        self.ambient_color = (0.1, 0.12, 0.18) # Dark sci-fi background ambient
        self.intensity = 1.0

    def set_intensity(self, val: float):
        self.intensity = max(0.1, min(2.0, val))
