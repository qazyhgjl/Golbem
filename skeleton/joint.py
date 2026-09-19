"""
Hierarchical Joint representation with 3D rotation, limits, and transformation matrices.
"""

import numpy as np

def rotation_matrix_xyz(rx, ry, rz):
    """Calculates 3D rotation matrix from Euler angles in degrees (X then Y then Z)."""
    rad_x, rad_y, rad_z = np.radians([rx, ry, rz])

    cx, sx = np.cos(rad_x), np.sin(rad_x)
    cy, sy = np.cos(rad_y), np.sin(rad_y)
    cz, sz = np.cos(rad_z), np.sin(rad_z)

    Rx = np.array([
        [1, 0, 0, 0],
        [0, cx, -sx, 0],
        [0, sx, cx, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    Ry = np.array([
        [cy, 0, sy, 0],
        [0, 1, 0, 0],
        [-sy, 0, cy, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    Rz = np.array([
        [cz, -sz, 0, 0],
        [sz, cz, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

    return Rz @ Ry @ Rx

def translation_matrix(x, y, z):
    """Calculates 4x4 translation matrix."""
    T = np.eye(4, dtype=np.float32)
    T[0, 3] = x
    T[1, 3] = y
    T[2, 3] = z
    return T


class Joint:
    def __init__(self, name: str, offset: tuple, min_limits: tuple = (-180, -180, -180), max_limits: tuple = (180, 180, 180)):
        self.name = name
        self.offset = np.array(offset, dtype=np.float32) # (x, y, z) relative to parent
        self.rotation = np.array([0.0, 0.0, 0.0], dtype=np.float32) # (rx, ry, rz) in degrees
        self.min_limits = np.array(min_limits, dtype=np.float32)
        self.max_limits = np.array(max_limits, dtype=np.float32)

        self.parent = None
        self.children = []

        self.local_matrix = np.eye(4, dtype=np.float32)
        self.global_matrix = np.eye(4, dtype=np.float32)
        self.world_position = np.array([0.0, 0.0, 0.0], dtype=np.float32)

        self.update_local_matrix()

    def add_child(self, child_joint):
        child_joint.parent = self
        self.children.append(child_joint)

    def set_rotation(self, rx: float, ry: float, rz: float):
        """Sets rotation with limit clamping."""
        clamped_r = np.clip([rx, ry, rz], self.min_limits, self.max_limits)
        self.rotation = clamped_r.astype(np.float32)
        self.update_local_matrix()

    def update_local_matrix(self):
        T = translation_matrix(*self.offset)
        R = rotation_matrix_xyz(*self.rotation)
        self.local_matrix = T @ R

    def reset_rotation(self):
        self.set_rotation(0.0, 0.0, 0.0)
