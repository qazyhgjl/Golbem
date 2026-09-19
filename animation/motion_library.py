"""
Motion Library defining keyframes for Body States and Exercise Motions.
"""

# Pose Definitions (Joint name: (rx, ry, rz))
POSE_IDLE = {
    "Pelvis": (0, 0, 0),
    "Spine": (0, 0, 0),
    "Chest": (0, 0, 0),
    "Neck": (0, 0, 0),
    "Head": (0, 0, 0),
    "Left_UpperArm": (-10, 0, -10),
    "Left_Forearm": (-15, 0, 0),
    "Right_UpperArm": (-10, 0, 10),
    "Right_Forearm": (-15, 0, 0),
    "Left_UpperLeg": (0, 0, 0),
    "Left_LowerLeg": (0, 0, 0),
    "Right_UpperLeg": (0, 0, 0),
    "Right_LowerLeg": (0, 0, 0),
}

POSE_LOOK_CAMERA = {
    **POSE_IDLE,
    "Head": (-10, 0, 0),
    "Chest": (5, 0, 0),
}

POSE_TURN_LEFT = {
    **POSE_IDLE,
    "Pelvis": (0, 30, 0),
    "Spine": (0, 25, 0),
    "Chest": (0, 20, 0),
    "Head": (0, 15, 0),
}

POSE_TURN_RIGHT = {
    **POSE_IDLE,
    "Pelvis": (0, -30, 0),
    "Spine": (0, -25, 0),
    "Chest": (0, -20, 0),
    "Head": (0, -15, 0),
}

POSE_WALK_1 = {
    "Pelvis": (0, 5, 0),
    "Left_UpperLeg": (-30, 0, 0),
    "Left_LowerLeg": (15, 0, 0),
    "Right_UpperLeg": (25, 0, 0),
    "Right_LowerLeg": (35, 0, 0),
    "Left_UpperArm": (25, 0, 0),
    "Right_UpperArm": (-25, 0, 0),
}

POSE_WALK_2 = {
    "Pelvis": (0, -5, 0),
    "Left_UpperLeg": (25, 0, 0),
    "Left_LowerLeg": (35, 0, 0),
    "Right_UpperLeg": (-30, 0, 0),
    "Right_LowerLeg": (15, 0, 0),
    "Left_UpperArm": (-25, 0, 0),
    "Right_UpperArm": (25, 0, 0),
}

POSE_RUN_1 = {
    "Pelvis": (-5, 10, 0),
    "Left_UpperLeg": (-50, 0, 0),
    "Left_LowerLeg": (30, 0, 0),
    "Right_UpperLeg": (45, 0, 0),
    "Right_LowerLeg": (80, 0, 0),
    "Left_UpperArm": (60, 0, 0),
    "Left_Forearm": (-60, 0, 0),
    "Right_UpperArm": (-50, 0, 0),
    "Right_Forearm": (-70, 0, 0),
}

POSE_RUN_2 = {
    "Pelvis": (-5, -10, 0),
    "Left_UpperLeg": (45, 0, 0),
    "Left_LowerLeg": (80, 0, 0),
    "Right_UpperLeg": (-50, 0, 0),
    "Right_LowerLeg": (30, 0, 0),
    "Left_UpperArm": (-50, 0, 0),
    "Left_Forearm": (-70, 0, 0),
    "Right_UpperArm": (60, 0, 0),
    "Right_Forearm": (-60, 0, 0),
}

POSE_SIT = {
    "Pelvis": (-10, 0, 0),
    "Spine": (10, 0, 0),
    "Left_UpperLeg": (-85, 0, 0),
    "Left_LowerLeg": (90, 0, 0),
    "Right_UpperLeg": (-85, 0, 0),
    "Right_LowerLeg": (90, 0, 0),
    "Left_UpperArm": (-10, 0, -15),
    "Right_UpperArm": (-10, 0, 15),
}

POSE_LIE_DOWN = {
    "Pelvis": (-80, 0, 0),
    "Spine": (0, 0, 0),
    "Chest": (0, 0, 0),
    "Head": (5, 0, 0),
    "Left_UpperLeg": (0, 0, 0),
    "Right_UpperLeg": (0, 0, 0),
}

POSE_SQUAT_DOWN = {
    "Pelvis": (15, 0, 0),
    "Spine": (20, 0, 0),
    "Left_UpperLeg": (-80, 0, 0),
    "Left_LowerLeg": (100, 0, 0),
    "Right_UpperLeg": (-80, 0, 0),
    "Right_LowerLeg": (100, 0, 0),
    "Left_UpperArm": (-70, 0, 0),
    "Right_UpperArm": (-70, 0, 0),
}

POSE_PUSHUP_DOWN = {
    "Pelvis": (-80, 0, 0),
    "Spine": (0, 0, 0),
    "Left_UpperArm": (-80, 0, -45),
    "Left_Forearm": (-90, 0, 0),
    "Right_UpperArm": (-80, 0, 45),
    "Right_Forearm": (-90, 0, 0),
}

POSE_PUSHUP_UP = {
    "Pelvis": (-80, 0, 0),
    "Spine": (0, 0, 0),
    "Left_UpperArm": (-80, 0, -10),
    "Left_Forearm": (-10, 0, 0),
    "Right_UpperArm": (-80, 0, 10),
    "Right_Forearm": (-10, 0, 0),
}

POSE_SITUP_UP = {
    "Pelvis": (-60, 0, 0),
    "Spine": (45, 0, 0),
    "Chest": (25, 0, 0),
    "Left_UpperLeg": (-45, 0, 0),
    "Left_LowerLeg": (60, 0, 0),
    "Right_UpperLeg": (-45, 0, 0),
    "Right_LowerLeg": (60, 0, 0),
    "Left_UpperArm": (-100, 0, -30),
    "Right_UpperArm": (-100, 0, 30),
}

POSE_JUMP_UP = {
    "Pelvis": (10, 0, 0),
    "Left_UpperLeg": (-20, 0, 0),
    "Left_LowerLeg": (30, 0, 0),
    "Right_UpperLeg": (-20, 0, 0),
    "Right_LowerLeg": (30, 0, 0),
    "Left_UpperArm": (-150, 0, 0),
    "Right_UpperArm": (-150, 0, 0),
}

POSE_BEND_FORWARD = {
    "Pelvis": (30, 0, 0),
    "Spine": (45, 0, 0),
    "Chest": (30, 0, 0),
    "Head": (15, 0, 0),
    "Left_UpperArm": (-30, 0, 0),
    "Right_UpperArm": (-30, 0, 0),
}

POSE_ARM_RAISE = {
    **POSE_IDLE,
    "Left_UpperArm": (-160, 0, 0),
    "Right_UpperArm": (-160, 0, 0),
}

POSE_ARM_ROTATION_1 = {
    **POSE_IDLE,
    "Left_UpperArm": (-90, 0, 0),
    "Right_UpperArm": (-90, 0, 0),
}

POSE_ARM_ROTATION_2 = {
    **POSE_IDLE,
    "Left_UpperArm": (-90, 90, 0),
    "Right_UpperArm": (-90, -90, 0),
}

POSE_LEG_RAISE = {
    **POSE_IDLE,
    "Left_UpperLeg": (-75, 0, 0),
}


MOTION_PRESETS = {
    "idle": [POSE_IDLE],
    "look_camera": [POSE_LOOK_CAMERA],
    "turn_left": [POSE_TURN_LEFT],
    "turn_right": [POSE_TURN_RIGHT],
    "walk": [POSE_WALK_1, POSE_WALK_2],
    "run": [POSE_RUN_1, POSE_RUN_2],
    "sit": [POSE_SIT],
    "lie_down": [POSE_LIE_DOWN],
    "stand": [POSE_IDLE],
    "squat": [POSE_IDLE, POSE_SQUAT_DOWN, POSE_IDLE],
    "push_up": [POSE_PUSHUP_UP, POSE_PUSHUP_DOWN, POSE_PUSHUP_UP],
    "sit_up": [POSE_LIE_DOWN, POSE_SITUP_UP, POSE_LIE_DOWN],
    "jump": [POSE_IDLE, POSE_JUMP_UP, POSE_IDLE],
    "bend_forward": [POSE_IDLE, POSE_BEND_FORWARD, POSE_IDLE],
    "stretching": [POSE_IDLE, POSE_ARM_RAISE, POSE_BEND_FORWARD, POSE_IDLE],
    "arm_raise": [POSE_IDLE, POSE_ARM_RAISE, POSE_IDLE],
    "arm_rotation": [POSE_ARM_ROTATION_1, POSE_ARM_ROTATION_2],
    "leg_raise": [POSE_IDLE, POSE_LEG_RAISE, POSE_IDLE],
}
