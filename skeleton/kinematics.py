"""
Forward and Inverse Kinematics (FK/IK) Solver helpers for Golbem Skeleton.
"""

import numpy as np

class KinematicsSolver:
    def __init__(self, skeleton):
        self.skeleton = skeleton

    def solve_limb_ik_2link(self, hip_or_shoulder_name: str, target_pos: np.ndarray):
        """2-Link Inverse Kinematics solver adjusting upper & lower joint rotations to reach target_pos."""
        joint_1 = self.skeleton.joints.get(hip_or_shoulder_name)
        if not joint_1 or not joint_1.children:
            return

        joint_2 = joint_1.children[0]
        if not joint_2.children:
            return

        joint_3 = joint_2.children[0]

        p1 = joint_1.world_position
        p3_target = np.array(target_pos, dtype=np.float32)

        l1 = float(np.linalg.norm(joint_2.offset))
        l2 = float(np.linalg.norm(joint_3.offset))
        dist = float(np.linalg.norm(p3_target - p1))

        # Clamp distance within reach
        dist = max(abs(l1 - l2) + 1e-4, min(l1 + l2 - 1e-4, dist))

        # Cosine rule for joint angle
        cos_angle2 = (l1**2 + l2**2 - dist**2) / (2.0 * l1 * l2)
        angle2_deg = float(np.degrees(np.arccos(np.clip(cos_angle2, -1.0, 1.0))))

        # Apply flex rotation to lower joint
        current_rot2 = joint_2.rotation
        joint_2.set_rotation(180.0 - angle2_deg, current_rot2[1], current_rot2[2])
        self.skeleton.update_kinematics()
