"""
Unit tests for Skeleton hierarchy, Joint rotations, limits, and Kinematics.
"""

import unittest
import numpy as np
from skeleton.skeleton import Skeleton

class TestSkeleton(unittest.TestCase):
    def setUp(self):
        self.skeleton = Skeleton()

    def test_skeleton_structure(self):
        self.assertGreater(len(self.skeleton.joints), 20)
        self.assertGreater(len(self.skeleton.bones), 20)
        self.assertIn("Pelvis", self.skeleton.joints)
        self.assertIn("Head", self.skeleton.joints)

    def test_joint_limits(self):
        spine = self.skeleton.joints["Spine"]
        # Max limit for Spine X is 45, trying to set 90
        spine.set_rotation(90, 0, 0)
        self.assertLessEqual(spine.rotation[0], 45.0)

    def test_kinematics_propagation(self):
        head_pos_initial = self.skeleton.joints["Head"].world_position.copy()
        self.skeleton.set_joint_rotation("Spine", 30, 0, 0)
        head_pos_after = self.skeleton.joints["Head"].world_position.copy()

        # Position should change after spine rotation
        self.assertFalse(np.array_equal(head_pos_initial, head_pos_after))

    def test_reset_pose(self):
        self.skeleton.set_joint_rotation("Spine", 30, 0, 0)
        self.skeleton.reset_pose()
        self.assertEqual(list(self.skeleton.joints["Spine"].rotation), [0.0, 0.0, 0.0])

if __name__ == "__main__":
    unittest.main()
