"""
Pose Library management, Preset Poses, and Local JSON Pose Save/Load for Golbem Simulator.
"""

import json
import os
from animation.motion_library import (
    POSE_IDLE, POSE_LOOK_CAMERA, POSE_TURN_LEFT, POSE_TURN_RIGHT,
    POSE_SIT, POSE_LIE_DOWN, POSE_SQUAT_DOWN, POSE_BEND_FORWARD, POSE_ARM_RAISE
)

POSE_NEUTRAL_A = {
    **POSE_IDLE,
    "Left_UpperArm": (-15, 0, -35),
    "Right_UpperArm": (-15, 0, 35),
}

POSE_T_POSE = {
    **POSE_IDLE,
    "Left_UpperArm": (0, 0, -90),
    "Right_UpperArm": (0, 0, 90),
    "Left_Forearm": (0, 0, 0),
    "Right_Forearm": (0, 0, 0),
}

POSE_RELAXED_STANDING = {
    **POSE_IDLE,
    "Pelvis": (0, 5, 0),
    "Left_UpperLeg": (-5, 0, 5),
    "Right_UpperLeg": (5, 0, -5),
    "Left_UpperArm": (-10, 0, -15),
    "Right_UpperArm": (-10, 0, 15),
}

POSE_KNEELING = {
    "Pelvis": (-15, 0, 0),
    "Left_UpperLeg": (-90, 0, 0),
    "Left_LowerLeg": (135, 0, 0),
    "Right_UpperLeg": (-90, 0, 0),
    "Right_LowerLeg": (135, 0, 0),
    "Left_UpperArm": (-15, 0, -10),
    "Right_UpperArm": (-15, 0, 10),
}

POSE_PRESETS = {
    "standing": POSE_IDLE,
    "idle": POSE_IDLE,
    "neutral_a": POSE_NEUTRAL_A,
    "t_pose": POSE_T_POSE,
    "relaxed": POSE_RELAXED_STANDING,
    "look_camera": POSE_LOOK_CAMERA,
    "sitting": POSE_SIT,
    "lying_down": POSE_LIE_DOWN,
    "kneeling": POSE_KNEELING,
    "bending": POSE_BEND_FORWARD,
    "arm_raise": POSE_ARM_RAISE,
}

class PoseLibrary:
    def __init__(self, poses_dir="models/poses"):
        self.poses_dir = poses_dir
        if not os.path.exists(self.poses_dir):
            os.makedirs(self.poses_dir, exist_ok=True)

    def get_preset_pose(self, name: str) -> dict:
        key = name.lower().replace(" ", "_")
        return POSE_PRESETS.get(key, POSE_IDLE)

    def save_pose_to_file(self, pose_dict: dict, filename: str) -> str:
        if not filename.endswith(".json"):
            filename += ".json"
        path = os.path.join(self.poses_dir, filename)

        serializable_pose = {k: list(v) for k, v in pose_dict.items()}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable_pose, f, indent=4, ensure_ascii=False)
        return path

    def load_pose_from_file(self, filename: str) -> dict:
        if not filename.endswith(".json"):
            filename += ".json"
        path = os.path.join(self.poses_dir, filename)
        if not os.path.exists(path):
            return POSE_IDLE

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {k: tuple(v) for k, v in data.items()}
