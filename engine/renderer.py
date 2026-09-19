"""
3D Sci-Fi Medical Renderer supporting Shaders, PBR-lite Materials, GLTF/OBJ assets,
and 7 Display Modes for Golbem Simulator.
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
from engine.shader import ShaderManager
from models.body_generator import (
    draw_sphere, draw_cylinder, draw_ellipsoid, draw_ribcage, draw_vertebrae,
    draw_heart, draw_lungs, draw_liver, draw_stomach, draw_kidneys
)

class Renderer:
    def __init__(self, scene):
        self.scene = scene
        self.shader_manager = ShaderManager()

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

        # Attempt compiling GLSL Shader Manager
        self.shader_manager.compile_shaders()

        if not self.shader_manager.is_compiled:
            # Fixed-function lighting fallback
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

        # Update shader lighting uniforms
        if self.shader_manager.is_compiled:
            self.shader_manager.use()
            self.shader_manager.set_lighting(
                key_dir=self.scene.lighting.key_light_dir,
                key_color=self.scene.lighting.key_light_color,
                fill_color=self.scene.lighting.fill_light_color,
                rim_color=(0.0, 0.9, 1.0)
            )
        else:
            glLightfv(GL_LIGHT0, GL_POSITION, [*self.scene.lighting.key_light_dir, 0.0])
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [*self.scene.lighting.key_light_color, 1.0])
            glLightfv(GL_LIGHT0, GL_AMBIENT, [*self.scene.lighting.ambient_color, 1.0])

        if self.scene.show_grid:
            self.draw_grid()

        # Render imported custom GLB/OBJ model if active
        if self.scene.asset_pipeline.is_custom_model_loaded:
            self.shader_manager.set_material_color(*COLOR_SKIN)
            self.scene.asset_pipeline.render_loaded_model(self.scene.skeleton)
            if self.shader_manager.is_compiled:
                self.shader_manager.unbind()
            return

        # Otherwise render procedural anatomical human model
        mode = self.scene.display_mode
        skel = self.scene.skeleton

        if mode == MODE_SKELETON:
            self.draw_bones(skel)
            self.draw_joints(skel)
        elif mode == MODE_MUSCLES:
            self.draw_muscles(skel)
            self.draw_bones(skel)
        elif mode == MODE_SKIN:
            self.draw_skin(skel, alpha=0.92)
        elif mode == MODE_TRANSPARENT_SKIN:
            self.draw_bones(skel)
            self.draw_skin(skel, alpha=0.30)
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

        if self.shader_manager.is_compiled:
            self.shader_manager.unbind()

    def draw_grid(self):
        if self.shader_manager.is_compiled:
            self.shader_manager.unbind()
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

        if not self.shader_manager.is_compiled:
            glEnable(GL_LIGHTING)
        else:
            self.shader_manager.use()

    def draw_bones(self, skel):
        self.shader_manager.set_material_color(*COLOR_BONES)
        self.shader_manager.set_pbr_params(fresnel_power=3.0, specular_shininess=48.0, alpha=0.95)

        for bone in skel.bones:
            draw_cylinder(bone.start_pos, bone.end_pos, radius=0.026)

        # Anatomical Skull
        head_pos = skel.joints["Head"].world_position
        glPushMatrix()
        glTranslatef(head_pos[0], head_pos[1] + 0.06, head_pos[2])
        glScalef(0.10, 0.12, 0.11)
        draw_sphere(radius=1.0)
        glPopMatrix()

        # Vertebral Column & Ribcage
        pelvis_pos = skel.joints["Pelvis"].world_position
        chest_pos = skel.joints["Chest"].world_position
        draw_vertebrae(pelvis_pos, chest_pos, count=14)

        if self.shader_manager.is_compiled:
            self.shader_manager.unbind()
        glDisable(GL_LIGHTING)
        glColor4f(0.82, 0.95, 1.0, 0.88)
        glLineWidth(1.5)
        draw_ribcage(chest_pos, num_ribs=10, width=0.20, height=0.28, depth=0.16)

        if not self.shader_manager.is_compiled:
            glEnable(GL_LIGHTING)
        else:
            self.shader_manager.use()

    def draw_joints(self, skel, debug_axes=False):
        for joint in skel.joints.values():
            glPushMatrix()
            glTranslatef(*joint.world_position)

            if self.scene.selected_item_name == joint.name:
                self.shader_manager.set_material_color(*COLOR_HIGHLIGHT)
                draw_sphere(radius=0.055)
            else:
                self.shader_manager.set_material_color(*COLOR_JOINTS)
                draw_sphere(radius=0.038)

            if debug_axes:
                if self.shader_manager.is_compiled:
                    self.shader_manager.unbind()
                glDisable(GL_LIGHTING)
                glLineWidth(2.0)
                glBegin(GL_LINES)
                glColor3f(1.0, 0.0, 0.0) # X axis
                glVertex3f(0, 0, 0)
                glVertex3f(0.12, 0, 0)
                glColor3f(0.0, 1.0, 0.0) # Y axis
                glVertex3f(0, 0, 0)
                glVertex3f(0, 0.12, 0)
                glColor3f(0.0, 0.5, 1.0) # Z axis
                glVertex3f(0, 0, 0)
                glVertex3f(0, 0, 0.12)
                glEnd()
                if not self.shader_manager.is_compiled:
                    glEnable(GL_LIGHTING)
                else:
                    self.shader_manager.use()

            glPopMatrix()

    def draw_muscles(self, skel):
        self.shader_manager.set_material_color(*COLOR_MUSCLES)
        self.shader_manager.set_pbr_params(fresnel_power=2.0, specular_shininess=24.0, alpha=0.82)

        chest_pos = skel.joints["Chest"].world_position
        spine_pos = skel.joints["Spine"].world_position
        pelvis_pos = skel.joints["Pelvis"].world_position

        draw_ellipsoid(chest_pos, 0.22, 0.15, 0.14)
        draw_ellipsoid(spine_pos, 0.18, 0.14, 0.12)
        draw_ellipsoid(pelvis_pos, 0.19, 0.12, 0.13)

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
        """Renders 3D Internal Organs with distinct shader material highlights."""
        chest_pos = skel.joints["Chest"].world_position
        spine_pos = skel.joints["Spine"].world_position

        self.shader_manager.set_pbr_params(fresnel_power=1.8, specular_shininess=36.0, alpha=0.95)
        draw_heart(chest_pos)
        draw_lungs(chest_pos)
        draw_liver(spine_pos)
        draw_stomach(spine_pos)
        draw_kidneys(spine_pos)

    def draw_skin(self, skel, alpha=0.85):
        color = (COLOR_SKIN[0], COLOR_SKIN[1], COLOR_SKIN[2], alpha)
        self.shader_manager.set_material_color(*color)
        self.shader_manager.set_pbr_params(fresnel_power=2.2, specular_shininess=32.0, alpha=alpha)

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
