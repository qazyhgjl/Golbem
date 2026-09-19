"""
Unit tests for Animation Controller and Motion Sequences.
"""

import unittest
from skeleton.skeleton import Skeleton
from animation.motion_sequence import MotionAction
from animation.animation_controller import AnimationController

class TestAnimation(unittest.TestCase):
    def setUp(self):
        self.skeleton = Skeleton()
        self.controller = AnimationController(self.skeleton)

    def test_enqueue_and_play(self):
        act = MotionAction("walk", duration=5.0)
        self.controller.enqueue_action(act)

        self.assertTrue(self.controller.is_playing)
        self.assertEqual(self.controller.current_motion_name, "Walk")

    def test_update_tick(self):
        act = MotionAction("walk", duration=2.0)
        self.controller.enqueue_action(act)
        self.controller.update(1.0)

        self.assertTrue(self.controller.is_playing)
        self.assertEqual(self.controller.elapsed_time, 1.0)

    def test_pause_resume_stop(self):
        act = MotionAction("run", duration=10.0)
        self.controller.enqueue_action(act)

        self.controller.pause()
        self.assertTrue(self.controller.is_paused)

        self.controller.resume()
        self.assertFalse(self.controller.is_paused)

        self.controller.stop()
        self.assertFalse(self.controller.is_playing)

if __name__ == "__main__":
    unittest.main()
