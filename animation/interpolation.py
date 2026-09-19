"""
Mathematical interpolation functions for keyframe blending.
"""

import numpy as np

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation."""
    return float(a + (b - a) * t)

def lerp_array(a: np.ndarray, b: np.ndarray, t: float) -> np.ndarray:
    """Array linear interpolation."""
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    return a + (b - a) * t

def smoothstep(t: float) -> float:
    """Smooth cubic Hermite ease-in ease-out interpolation t in [0, 1]."""
    t = max(0.0, min(1.0, t))
    return float(t * t * (3.0 - 2.0 * t))

def interpolate_poses(pose_a: dict, pose_b: dict, t: float) -> dict:
    """Interpolates joint rotation dictionaries pose_a and pose_b with easing factor t."""
    eased_t = smoothstep(t)
    blended = {}
    for joint_name in pose_a:
        rot_a = pose_a[joint_name]
        rot_b = pose_b.get(joint_name, rot_a)
        blended[joint_name] = lerp_array(rot_a, rot_b, eased_t)
    return blended
