"""
Motion action representation.
"""

class MotionAction:
    def __init__(self, action_type: str, duration: float = None, repetitions: int = 1):
        self.action_type = action_type # Key in MOTION_PRESETS
        self.duration = duration       # Execution time in seconds (if specified)
        self.repetitions = repetitions # Number of loops (if specified)

    def __repr__(self):
        return f"<MotionAction type='{self.action_type}' duration={self.duration} reps={self.repetitions}>"
