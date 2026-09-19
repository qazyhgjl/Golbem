"""
Skeleton representation with full human anatomical structure and forward kinematics solver.
"""

import numpy as np
from skeleton.joint import Joint
from skeleton.bone import Bone

class Skeleton:
    def __init__(self):
        self.joints = {}
        self.bones = []
        self.root = None
        self._build_skeleton()

    def _build_skeleton(self):
        """Constructs the complete hierarchical 3D human skeleton."""
        # Root / Pelvis
        self.root = Joint("Pelvis", offset=(0.0, 0.95, 0.0), min_limits=(-45, -45, -45), max_limits=(45, 45, 45))
        self.joints["Pelvis"] = self.root

        # Spine & Torso Hierarchy
        spine = Joint("Spine", offset=(0.0, 0.15, 0.0), min_limits=(-30, -30, -30), max_limits=(45, 30, 30))
        chest = Joint("Chest", offset=(0.0, 0.22, 0.0), min_limits=(-30, -30, -30), max_limits=(45, 30, 30))
        neck = Joint("Neck", offset=(0.0, 0.18, 0.0), min_limits=(-45, -45, -45), max_limits=(45, 45, 45))
        head = Joint("Head", offset=(0.0, 0.12, 0.0), min_limits=(-45, -60, -30), max_limits=(45, 60, 30))

        self.root.add_child(spine)
        spine.add_child(chest)
        chest.add_child(neck)
        neck.add_child(head)

        self.joints["Spine"] = spine
        self.joints["Chest"] = chest
        self.joints["Neck"] = neck
        self.joints["Head"] = head

        # Left Arm Hierarchy
        clav_l = Joint("Left_Clavicle", offset=(0.08, 0.16, 0.0), min_limits=(-15, -15, -15), max_limits=(20, 20, 20))
        arm_l = Joint("Left_UpperArm", offset=(0.14, -0.02, 0.0), min_limits=(-180, -90, -90), max_limits=(90, 90, 180))
        forearm_l = Joint("Left_Forearm", offset=(0.26, 0.0, 0.0), min_limits=(-150, -10, -10), max_limits=(0, 10, 10))
        hand_l = Joint("Left_Hand", offset=(0.24, 0.0, 0.0), min_limits=(-60, -30, -45), max_limits=(60, 30, 45))
        fingers_l = Joint("Left_Fingers", offset=(0.08, 0.0, 0.0), min_limits=(-90, 0, 0), max_limits=(15, 0, 0))

        chest.add_child(clav_l)
        clav_l.add_child(arm_l)
        arm_l.add_child(forearm_l)
        forearm_l.add_child(hand_l)
        hand_l.add_child(fingers_l)

        self.joints["Left_Clavicle"] = clav_l
        self.joints["Left_UpperArm"] = arm_l
        self.joints["Left_Forearm"] = forearm_l
        self.joints["Left_Hand"] = hand_l
        self.joints["Left_Fingers"] = fingers_l

        # Right Arm Hierarchy
        clav_r = Joint("Right_Clavicle", offset=(-0.08, 0.16, 0.0), min_limits=(-15, -20, -20), max_limits=(20, 15, 15))
        arm_r = Joint("Right_UpperArm", offset=(-0.14, -0.02, 0.0), min_limits=(-180, -90, -180), max_limits=(90, 90, 90))
        forearm_r = Joint("Right_Forearm", offset=(-0.26, 0.0, 0.0), min_limits=(-150, -10, -10), max_limits=(0, 10, 10))
        hand_r = Joint("Right_Hand", offset=(-0.24, 0.0, 0.0), min_limits=(-60, -30, -45), max_limits=(60, 30, 45))
        fingers_r = Joint("Right_Fingers", offset=(-0.08, 0.0, 0.0), min_limits=(-90, 0, 0), max_limits=(15, 0, 0))

        chest.add_child(clav_r)
        clav_r.add_child(arm_r)
        arm_r.add_child(forearm_r)
        forearm_r.add_child(hand_r)
        hand_r.add_child(fingers_r)

        self.joints["Right_Clavicle"] = clav_r
        self.joints["Right_UpperArm"] = arm_r
        self.joints["Right_Forearm"] = forearm_r
        self.joints["Right_Hand"] = hand_r
        self.joints["Right_Fingers"] = fingers_r

        # Left Leg Hierarchy
        hip_l = Joint("Left_UpperLeg", offset=(0.11, -0.05, 0.0), min_limits=(-120, -45, -45), max_limits=(45, 45, 45))
        leg_l = Joint("Left_LowerLeg", offset=(0.0, -0.42, 0.0), min_limits=(0, 0, 0), max_limits=(150, 0, 0))
        foot_l = Joint("Left_Foot", offset=(0.0, -0.40, 0.0), min_limits=(-45, -20, -20), max_limits=(45, 20, 20))
        toes_l = Joint("Left_Toes", offset=(0.0, -0.05, 0.14), min_limits=(-30, 0, 0), max_limits=(30, 0, 0))

        self.root.add_child(hip_l)
        hip_l.add_child(leg_l)
        leg_l.add_child(foot_l)
        foot_l.add_child(toes_l)

        self.joints["Left_UpperLeg"] = hip_l
        self.joints["Left_LowerLeg"] = leg_l
        self.joints["Left_Foot"] = foot_l
        self.joints["Left_Toes"] = toes_l

        # Right Leg Hierarchy
        hip_r = Joint("Right_UpperLeg", offset=(-0.11, -0.05, 0.0), min_limits=(-120, -45, -45), max_limits=(45, 45, 45))
        leg_r = Joint("Right_LowerLeg", offset=(0.0, -0.42, 0.0), min_limits=(0, 0, 0), max_limits=(150, 0, 0))
        foot_r = Joint("Right_Foot", offset=(0.0, -0.40, 0.0), min_limits=(-45, -20, -20), max_limits=(45, 20, 20))
        toes_r = Joint("Right_Toes", offset=(0.0, -0.05, 0.14), min_limits=(-30, 0, 0), max_limits=(30, 0, 0))

        self.root.add_child(hip_r)
        hip_r.add_child(leg_r)
        leg_r.add_child(foot_r)
        foot_r.add_child(toes_r)

        self.joints["Right_UpperLeg"] = hip_r
        self.joints["Right_LowerLeg"] = leg_r
        self.joints["Right_Foot"] = foot_r
        self.joints["Right_Toes"] = toes_r

        # Create Bone connections
        self._build_bones()
        self.update_kinematics()

    def _build_bones(self):
        """Creates bone structures between parent and child joints."""
        self.bones.clear()
        for joint in self.joints.values():
            for child in joint.children:
                bone_name = f"{joint.name}_to_{child.name}"
                self.bones.append(Bone(bone_name, joint, child))

    def update_kinematics(self, parent_matrix=None, current_joint=None):
        """Forward Kinematics solver: Computes global transformation matrices for all joints."""
        if current_joint is None:
            current_joint = self.root
            parent_matrix = np.eye(4, dtype=np.float32)

        global_matrix = parent_matrix @ current_joint.local_matrix
        current_joint.global_matrix = global_matrix
        current_joint.world_position = global_matrix[:3, 3]

        for child in current_joint.children:
            self.update_kinematics(global_matrix, child)

    def set_joint_rotation(self, joint_name: str, rx: float, ry: float, rz: float):
        if joint_name in self.joints:
            self.joints[joint_name].set_rotation(rx, ry, rz)
            self.update_kinematics()

    def reset_pose(self):
        for joint in self.joints.values():
            joint.reset_rotation()
        self.update_kinematics()

    def get_pose_dict(self) -> dict:
        return {name: j.rotation.copy() for name, j in self.joints.items()}

    def set_pose_dict(self, pose_dict: dict):
        for name, rot in pose_dict.items():
            if name in self.joints:
                self.joints[name].set_rotation(rot[0], rot[1], rot[2])
        self.update_kinematics()
