"""
Bone definition connecting parent and child joints.
"""

import numpy as np

class Bone:
    def __init__(self, name: str, parent_joint, child_joint, radius: float = 0.03):
        self.name = name
        self.parent_joint = parent_joint
        self.child_joint = child_joint
        self.radius = radius

    @property
    def start_pos(self) -> np.ndarray:
        return self.parent_joint.world_position

    @property
    def end_pos(self) -> np.ndarray:
        return self.child_joint.world_position

    @property
    def length(self) -> float:
        return float(np.linalg.norm(self.end_pos - self.start_pos))
