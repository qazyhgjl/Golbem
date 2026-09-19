"""
Animation Controller managing motion keyframing, sequence queuing, speed adjustment, and transitions.
"""

from animation.motion_library import MOTION_PRESETS, POSE_IDLE
from animation.interpolation import interpolate_poses

# Standard cycle durations (seconds per full motion loop)
BASE_CYCLE_DURATIONS = {
    "walk": 1.2,
    "run": 0.8,
    "squat": 2.0,
    "push_up": 2.0,
    "sit_up": 2.0,
    "jump": 1.0,
    "bend_forward": 2.0,
    "stretching": 3.0,
    "arm_raise": 1.5,
    "arm_rotation": 1.5,
    "leg_raise": 1.5,
}

class AnimationController:
    def __init__(self, skeleton):
        self.skeleton = skeleton
        self.queue = [] # Queue of MotionAction objects
        self.current_action = None
        self.is_playing = False
        self.is_paused = False

        self.speed = 1.0 # Playback speed multiplier
        self.elapsed_time = 0.0 # Time spent in current motion
        self.action_duration = 0.0 # Total target duration for current action
        self.cycle_duration = 1.0 # Duration per cycle loop

        self.start_pose = POSE_IDLE.copy()
        self.current_motion_name = "Idle"

    def enqueue_action(self, action):
        """Enqueues a new MotionAction."""
        self.queue.append(action)
        if not self.is_playing and not self.is_paused:
            self.play_next()

    def set_sequence(self, actions_list):
        """Replaces motion queue with new sequence of actions."""
        self.stop()
        self.queue = list(actions_list)
        self.play_next()

    def play_next(self):
        if not self.queue:
            self.is_playing = False
            self.current_action = None
            self.current_motion_name = "Idle"
            return

        self.current_action = self.queue.pop(0)
        self.is_playing = True
        self.is_paused = False
        self.elapsed_time = 0.0
        self.start_pose = self.skeleton.get_pose_dict()
        self.current_motion_name = self.current_action.action_type.replace("_", " ").title()

        act_type = self.current_action.action_type
        base_cycle = BASE_CYCLE_DURATIONS.get(act_type, 1.5)
        self.cycle_duration = base_cycle

        preset_keyframes = MOTION_PRESETS.get(act_type, [POSE_IDLE])

        if self.current_action.duration is not None:
            self.action_duration = float(self.current_action.duration)
        else:
            reps = max(1, self.current_action.repetitions)
            self.action_duration = float(base_cycle * reps)

    def pause(self):
        self.is_paused = True

    def resume(self):
        if self.current_action:
            self.is_paused = False
            self.is_playing = True

    def stop(self):
        self.queue.clear()
        self.current_action = None
        self.is_playing = False
        self.is_paused = False
        self.elapsed_time = 0.0
        self.current_motion_name = "Idle"
        self.skeleton.reset_pose()

    def update(self, delta_time: float):
        if not self.is_playing or self.is_paused or self.current_action is None:
            return

        self.elapsed_time += delta_time * self.speed

        if self.elapsed_time >= self.action_duration:
            # Action finished
            self.play_next()
            return

        preset_keyframes = MOTION_PRESETS.get(self.current_action.action_type, [POSE_IDLE])
        num_frames = len(preset_keyframes)

        if num_frames == 1:
            # Static pose (e.g. Idle, Sit, Stand, Turn)
            t = min(1.0, self.elapsed_time / 0.5) # 0.5s transition
            blended = interpolate_poses(self.start_pose, preset_keyframes[0], t)
            self.skeleton.set_pose_dict(blended)
        else:
            # Multi-frame motion loop (Walk, Run, Squat, Push-up, Sit-up, etc.)
            cycle_progress = (self.elapsed_time % self.cycle_duration) / self.cycle_duration

            frame_float = cycle_progress * (num_frames - 1)
            frame_idx1 = int(frame_float)
            frame_idx2 = min(num_frames - 1, frame_idx1 + 1)
            t = frame_float - frame_idx1

            pose_a = preset_keyframes[frame_idx1]
            pose_b = preset_keyframes[frame_idx2]
            blended = interpolate_poses(pose_a, pose_b, t)
            self.skeleton.set_pose_dict(blended)
