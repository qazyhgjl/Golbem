"""
3D Sci-Fi Human Renderer supporting 7 high-detail display modes for Golbem Simulator.
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt

from app.settings import (
    COLOR_BG_DARK, COLOR_GRID, COLOR_SKIN, COLOR_SKIN_TRANSPARENT,
    COLOR_BONES, COLOR_MUSCLES, COLOR_JOINTS, COLOR_HIGHLIGHT,
    MODE_SKIN, MODE_TRANSPARENT_SKIN, MODE_SKELETON,
    MODE_MUSCLES, MODE_XRAY, MODE_ORGANS, MODE_JOINT_DEBUG
)
from models.body_generator import (
    draw_sphere, draw_cylinder, draw_ellipsoid, draw_ribcage, draw_vertebrae,
    draw_heart, draw_lungs, draw_liver, draw_stomach, draw_kidneys
)

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

        # Sci-Fi Medical Lighting setup
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Camera position
        eye = self.scene.camera.get_eye_position()
        target = self.scene.camera.target
        gluLookAt(eye[0], eye[1], eye[2], target[0], target[1], target[2], 0, 1, 0)

        # Set Key & Fill lights
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
            self.draw_organs(skel)
            self.draw_skin(skel, alpha=0.22)
            self.draw_joints(skel)
        elif mode == MODE_ORGANS:
            self.draw_bones(skel)
            self.draw_organs(skel)
            self.draw_skin(skel, alpha=0.18)
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

        # Skull bone structure
        head_pos = skel.joints["Head"].world_position
        glPushMatrix()
        glTranslatef(head_pos[0], head_pos[1] + 0.06, head_pos[2])
        glScalef(0.10, 0.12, 0.11)
        draw_sphere(radius=1.0)
        glPopMatrix()

        # Vertebral Column & Ribcage
        pelvis_pos = skel.joints["Pelvis"].world_position
        chest_pos = skel.joints["Chest"].world_position
        draw_vertebrae(pelvis_pos, chest_pos, count=12)

        glDisable(GL_LIGHTING)
        glColor4f(0.8, 0.95, 1.0, 0.85)
        glLineWidth(1.5)
        draw_ribcage(chest_pos, num_ribs=10, width=0.20, height=0.28, depth=0.16)
        glEnable(GL_LIGHTING)

    def draw_joints(self, skel, debug_axes=False):
        for joint in skel.joints.values():
            glPushMatrix()
            glTranslatef(*joint.world_position)

            # Glowing orange joint marker
            if self.scene.selected_item_name == joint.name:
                glColor4f(*COLOR_HIGHLIGHT)
                draw_sphere(radius=0.055)
            else:
                glColor4f(*COLOR_JOINTS)
                draw_sphere(radius=0.038)

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

        # Pectorals & Abdominals
        chest_pos = skel.joints["Chest"].world_position
        spine_pos = skel.joints["Spine"].world_position
        pelvis_pos = skel.joints["Pelvis"].world_position

        draw_ellipsoid(chest_pos, 0.22, 0.15, 0.14)
        draw_ellipsoid(spine_pos, 0.18, 0.14, 0.12)
        draw_ellipsoid(pelvis_pos, 0.19, 0.12, 0.13)

        # Shoulder Deltoids & Arm Biceps/Triceps
        for side in ["Left", "Right"]:
            arm_start = skel.joints[f"{side}_UpperArm"].world_position
            arm_end = skel.joints[f"{side}_Forearm"].world_position
            hand_pos = skel.joints[f"{side}_Hand"].world_position

            draw_ellipsoid(arm_start, 0.08, 0.08, 0.08)
            mid_arm = (arm_start + arm_end) * 0.5
            draw_cylinder(arm_start, arm_end, radius=0.055)
            draw_ellipsoid(mid_arm, 0.07, 0.11, 0.07)

            mid_forearm = (arm_end + hand_pos) * 0.5
            draw_cylinder(arm_end, hand_pos, radius=0.045)
            draw_ellipsoid(mid_forearm, 0.05, 0.09, 0.05)

            hip_pos = skel.joints[f"{side}_UpperLeg"].world_position
            knee_pos = skel.joints[f"{side}_LowerLeg"].world_position
            foot_pos = skel.joints[f"{side}_Foot"].world_position

            draw_ellipsoid(hip_pos, 0.12, 0.12, 0.12)
            mid_thigh = (hip_pos + knee_pos) * 0.5
            draw_cylinder(hip_pos, knee_pos, radius=0.08)
            draw_ellipsoid(mid_thigh, 0.11, 0.16, 0.11)

            mid_calf = (knee_pos + foot_pos) * 0.5
            draw_cylinder(knee_pos, foot_pos, radius=0.065)
            draw_ellipsoid(mid_calf, 0.085, 0.14, 0.085)

    def draw_organs(self, skel):
        """Renders 3D Internal Organs attached to thoracic and abdominal spine/chest."""
        chest_pos = skel.joints["Chest"].world_position
        spine_pos = skel.joints["Spine"].world_position

        draw_heart(chest_pos)
        draw_lungs(chest_pos)
        draw_liver(spine_pos)
        draw_stomach(spine_pos)
        draw_kidneys(spine_pos)

    def draw_skin(self, skel, alpha=0.85):
        color = (COLOR_SKIN[0], COLOR_SKIN[1], COLOR_SKIN[2], alpha)
        glColor4f(*color)

        head_pos = skel.joints["Head"].world_position
        neck_pos = skel.joints["Neck"].world_position
        draw_ellipsoid(head_pos + np.array([0, 0.07, 0]), 0.115, 0.145, 0.125)
        draw_cylinder(neck_pos, head_pos, radius=0.065)

        pelvis_pos = skel.joints["Pelvis"].world_position
        chest_pos = skel.joints["Chest"].world_position
        spine_pos = skel.joints["Spine"].world_position

        draw_ellipsoid(chest_pos, 0.245, 0.185, 0.165)
        draw_ellipsoid(spine_pos, 0.205, 0.165, 0.145)
        draw_ellipsoid(pelvis_pos, 0.215, 0.145, 0.155)

        for bone in skel.bones:
            draw_cylinder(bone.start_pos, bone.end_pos, radius=0.068)
