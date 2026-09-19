"""
3D Camera Controller with Orbit, Pan, Zoom, and Preset Views.
"""

import numpy as np

class Camera:
    def __init__(self):
        self.distance = 3.5
        self.pitch = 5.0    # Degrees around X axis
        self.yaw = 0.0      # Degrees around Y axis
        self.target = np.array([0.0, 0.95, 0.0], dtype=np.float32) # Focus point (Pelvis/Chest)
        self.fov = 45.0
        self.near = 0.1
        self.far = 100.0

    def reset(self):
        self.distance = 3.5
        self.pitch = 5.0
        self.yaw = 0.0
        self.target = np.array([0.0, 0.95, 0.0], dtype=np.float32)

    def set_view_preset(self, preset_name: str):
        preset_name = preset_name.lower()
        self.target = np.array([0.0, 0.95, 0.0], dtype=np.float32)
        if preset_name in ["front", "جلو"]:
            self.pitch = 5.0
            self.yaw = 0.0
        elif preset_name in ["back", "پشت"]:
            self.pitch = 5.0
            self.yaw = 180.0
        elif preset_name in ["left", "چپ"]:
            self.pitch = 5.0
            self.yaw = 90.0
        elif preset_name in ["right", "راست"]:
            self.pitch = 5.0
            self.yaw = -90.0
        elif preset_name in ["three_quarter", "3/4", "سه چهارم"]:
            self.pitch = 15.0
            self.yaw = 35.0

    def orbit(self, delta_yaw: float, delta_pitch: float):
        self.yaw += delta_yaw
        self.pitch = float(np.clip(self.pitch + delta_pitch, -85.0, 85.0))

    def pan(self, delta_x: float, delta_y: float):
        rad_yaw = np.radians(self.yaw)
        right = np.array([np.cos(rad_yaw), 0.0, -np.sin(rad_yaw)], dtype=np.float32)
        up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.target += right * delta_x + up * delta_y

    def zoom(self, delta: float):
        self.distance = float(np.clip(self.distance - delta, 0.5, 15.0))

    def get_eye_position(self) -> np.ndarray:
        rad_pitch = np.radians(self.pitch)
        rad_yaw = np.radians(self.yaw)

        x = self.distance * np.cos(rad_pitch) * np.sin(rad_yaw)
        y = self.distance * np.sin(rad_pitch)
        z = self.distance * np.cos(rad_pitch) * np.cos(rad_yaw)

        return self.target + np.array([x, y, z], dtype=np.float32)
