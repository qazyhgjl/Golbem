"""
3D Sci-Fi Human Renderer supporting 6 display modes and cyan/blue aesthetic.
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

from app.settings import (
    COLOR_BG_DARK, COLOR_GRID, COLOR_SKIN, COLOR_SKIN_TRANSPARENT,
    COLOR_BONES, COLOR_MUSCLES, COLOR_JOINTS, COLOR_HIGHLIGHT,
    MODE_SKIN, MODE_TRANSPARENT_SKIN, MODE_SKELETON,
    MODE_MUSCLES, MODE_XRAY, MODE_JOINT_DEBUG
)
from models.body_generator import draw_sphere, draw_cylinder, draw_ellipsoid

class Renderer:
    def __init__(self, scene):
        self.scene = scene

    def setup_gl(self, width: int, height: int):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(max(1, height))
        gluPerspective(self.scene.camera.fov, aspect, self.scene.camera.near, self.scene.camera.far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClearColor(*COLOR_BG_DARK)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        # Lighting setup
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Camera setup
        eye = self.scene.camera.get_eye_position()
        target = self.scene.camera.target
        gluLookAt(eye[0], eye[1], eye[2], target[0], target[1], target[2], 0, 1, 0)

        # Set Key & Fill light
        glLightfv(GL_LIGHT0, GL_POSITION, [*self.scene.lighting.key_light_dir, 0.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [*self.scene.lighting.key_light_color, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [*self.scene.lighting.ambient_color, 1.0])

        if self.scene.show_grid:
            self.draw_grid()

        # Render Human Body according to current display mode
        mode = self.scene.display_mode
        skel = self.scene.skeleton

        if mode == MODE_SKELETON:
            self.draw_bones(skel)
            self.draw_joints(skel)
        elif mode == MODE_MUSCLES:
            self.draw_muscles(skel)
            self.draw_bones(skel)
        elif mode == MODE_SKIN:
            self.draw_skin(skel, alpha=0.9)
        elif mode == MODE_TRANSPARENT_SKIN:
            self.draw_bones(skel)
            self.draw_skin(skel, alpha=0.3)
        elif mode == MODE_XRAY:
            self.draw_bones(skel)
            self.draw_muscles(skel)
            self.draw_skin(skel, alpha=0.25)
            self.draw_joints(skel)
        elif mode == MODE_JOINT_DEBUG:
            self.draw_bones(skel)
            self.draw_joints(skel, debug_axes=True)

    def draw_grid(self):
        glDisable(GL_LIGHTING)
        glColor4f(*COLOR_GRID)
        glLineWidth(1.0)

        grid_size = 10
        spacing = 0.5

        glBegin(GL_LINES)
        for i in range(-grid_size, grid_size + 1):
            coord = i * spacing
            glVertex3f(coord, 0.0, -grid_size * spacing)
            glVertex3f(coord, 0.0, grid_size * spacing)

            glVertex3f(-grid_size * spacing, 0.0, coord)
            glVertex3f(grid_size * spacing, 0.0, coord)
        glEnd()
        glEnable(GL_LIGHTING)

    def draw_bones(self, skel):
        glColor4f(*COLOR_BONES)
        for bone in skel.bones:
            draw_cylinder(bone.start_pos, bone.end_pos, radius=0.025)

    def draw_joints(self, skel, debug_axes=False):
        for joint in skel.joints.values():
            glPushMatrix()
            glTranslatef(*joint.world_position)

            # Glowing orange joint marker
            glColor4f(*COLOR_JOINTS)
            draw_sphere(radius=0.04)

            if debug_axes:
                glDisable(GL_LIGHTING)
                glLineWidth(2.0)
                glBegin(GL_LINES)
                # X axis - Red
                glColor3f(1.0, 0.0, 0.0)
                glVertex3f(0, 0, 0)
                glVertex3f(0.12, 0, 0)
                # Y axis - Green
                glColor3f(0.0, 1.0, 0.0)
                glVertex3f(0, 0, 0)
                glVertex3f(0, 0.12, 0)
                # Z axis - Blue
                glColor3f(0.0, 0.5, 1.0)
                glVertex3f(0, 0, 0)
                glVertex3f(0, 0, 0.12)
                glEnd()
                glEnable(GL_LIGHTING)

            glPopMatrix()

    def draw_muscles(self, skel):
        glColor4f(*COLOR_MUSCLES)
        # Main muscle groups attached to bones/joints
        # Torso / Pectorals / Abdomen
        chest_pos = skel.joints["Chest"].world_position
        spine_pos = skel.joints["Spine"].world_position
        draw_ellipsoid(chest_pos, 0.22, 0.16, 0.14)
        draw_ellipsoid(spine_pos, 0.18, 0.14, 0.12)

        # Biceps / Triceps
        for side in ["Left", "Right"]:
            arm_start = skel.joints[f"{side}_UpperArm"].world_position
            arm_end = skel.joints[f"{side}_Forearm"].world_position
            mid_arm = (arm_start + arm_end) * 0.5
            draw_ellipsoid(mid_arm, 0.06, 0.12, 0.06)

            forearm_start = skel.joints[f"{side}_Forearm"].world_position
            forearm_end = skel.joints[f"{side}_Hand"].world_position
            mid_forearm = (forearm_start + forearm_end) * 0.5
            draw_ellipsoid(mid_forearm, 0.05, 0.10, 0.05)

            # Quadriceps / Calves
            hip_pos = skel.joints[f"{side}_UpperLeg"].world_position
            knee_pos = skel.joints[f"{side}_LowerLeg"].world_position
            mid_thigh = (hip_pos + knee_pos) * 0.5
            draw_ellipsoid(mid_thigh, 0.10, 0.18, 0.10)

            ankle_pos = skel.joints[f"{side}_Foot"].world_position
            mid_calf = (knee_pos + ankle_pos) * 0.5
            draw_ellipsoid(mid_calf, 0.08, 0.16, 0.08)

    def draw_skin(self, skel, alpha=0.85):
        color = (COLOR_SKIN[0], COLOR_SKIN[1], COLOR_SKIN[2], alpha)
        glColor4f(*color)

        # Head / Neck
        head_pos = skel.joints["Head"].world_position
        draw_ellipsoid(head_pos + np.array([0, 0.08, 0]), 0.11, 0.14, 0.12)

        # Upper Torso & Pelvis
        pelvis_pos = skel.joints["Pelvis"].world_position
        chest_pos = skel.joints["Chest"].world_position
        spine_pos = skel.joints["Spine"].world_position

        draw_ellipsoid(chest_pos, 0.24, 0.18, 0.16)
        draw_ellipsoid(spine_pos, 0.20, 0.16, 0.14)
        draw_ellipsoid(pelvis_pos, 0.21, 0.14, 0.15)

        # Limbs connection cylinders
        for bone in skel.bones:
            draw_cylinder(bone.start_pos, bone.end_pos, radius=0.065)
