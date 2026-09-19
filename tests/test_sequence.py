"""
Integration tests for Command Execution Pipeline (Persian Text -> CommandExecutor -> Scene/AnimationController -> Skeleton).
"""

import unittest
from engine.scene import Scene
from animation.animation_controller import AnimationController
from command.executor import CommandExecutor

class TestSequenceIntegration(unittest.TestCase):
    def setUp(self):
        self.scene = Scene()
        self.controller = AnimationController(self.scene.skeleton)
        self.executor = CommandExecutor(self.scene, self.controller)

    def test_end_to_end_command_execution(self):
        res = self.executor.execute_text_command("به مدت ۲۰ ثانیه راه برو و بعد بنشین")
        self.assertTrue(res["success"])
        self.assertEqual(len(self.controller.queue) + (1 if self.controller.current_action else 0), 2)
        self.assertEqual(self.controller.current_motion_name, "Walk")

    def test_stop_command_execution(self):
        self.executor.execute_text_command("۳۰ ثانیه بدو")
        self.assertTrue(self.controller.is_playing)

        stop_res = self.executor.execute_text_command("تمام حرکات را متوقف کن")
        self.assertTrue(stop_res["success"])
        self.assertFalse(self.controller.is_playing)

if __name__ == "__main__":
    unittest.main()
