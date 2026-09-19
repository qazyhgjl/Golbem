"""
Shader Manager for compiling, linking, and managing GLSL shaders in OpenGL.
Includes fallback support if shaders are not available or unsupported.
"""

from OpenGL.GL import *
from OpenGL.GL import shaders
import os
import numpy as np
from app.logger import logger

class ShaderManager:
    def __init__(self, vert_path="assets/shaders/medical_pbr.vert", frag_path="assets/shaders/medical_pbr.frag"):
        self.vert_path = vert_path
        self.frag_path = frag_path
        self.program = None
        self.is_compiled = False
        self.uniform_locs = {}

    def compile_shaders(self) -> bool:
        """Compiles GLSL vertex and fragment shaders."""
        if not os.path.exists(self.vert_path) or not os.path.exists(self.frag_path):
            logger.warning("Shader files not found. Using fixed-function pipeline fallback.")
            self.is_compiled = False
            return False

        try:
            with open(self.vert_path, "r", encoding="utf-8") as f:
                vert_code = f.read()
            with open(self.frag_path, "r", encoding="utf-8") as f:
                frag_code = f.read()

            vert_shader = shaders.compileShader(vert_code, GL_VERTEX_SHADER)
            frag_shader = shaders.compileShader(frag_code, GL_FRAGMENT_SHADER)
            self.program = shaders.compileProgram(vert_shader, frag_shader)
            self.is_compiled = True
            self._cache_uniform_locations()
            logger.info("GLSL Sci-Fi Medical Shaders compiled successfully!")
            return True
        except Exception as e:
            logger.warning(f"Shader compilation failed: {e}. Falling back to enhanced fixed-function pipeline.")
            self.is_compiled = False
            return False

    def _cache_uniform_locations(self):
        if not self.is_compiled or not self.program:
            return
        glUseProgram(self.program)
        uniforms = [
            "uMaterialColor", "uKeyLightDir", "uKeyLightColor",
            "uFillLightColor", "uRimColor", "uFresnelPower",
            "uSpecularShininess", "uAlpha"
        ]
        for u in uniforms:
            self.uniform_locs[u] = glGetUniformLocation(self.program, u)

    def use(self):
        if self.is_compiled and self.program:
            glUseProgram(self.program)

    def unbind(self):
        glUseProgram(0)

    def set_material_color(self, r, g, b, a=1.0):
        if not self.is_compiled:
            glColor4f(r, g, b, a)
            return
        loc = self.uniform_locs.get("uMaterialColor", -1)
        if loc != -1:
            glUniform4f(loc, float(r), float(g), float(b), float(a))

    def set_lighting(self, key_dir=(0.5, 1.0, 0.8), key_color=(0.0, 0.85, 1.0), fill_color=(0.2, 0.3, 0.6), rim_color=(0.0, 0.9, 1.0)):
        if not self.is_compiled:
            return
        loc_dir = self.uniform_locs.get("uKeyLightDir", -1)
        loc_key = self.uniform_locs.get("uKeyLightColor", -1)
        loc_fill = self.uniform_locs.get("uFillLightColor", -1)
        loc_rim = self.uniform_locs.get("uRimColor", -1)

        if loc_dir != -1: glUniform3f(loc_dir, *key_dir)
        if loc_key != -1: glUniform3f(loc_key, *key_color)
        if loc_fill != -1: glUniform3f(loc_fill, *fill_color)
        if loc_rim != -1: glUniform3f(loc_rim, *rim_color)

    def set_pbr_params(self, fresnel_power=2.5, specular_shininess=32.0, alpha=1.0):
        if not self.is_compiled:
            return
        loc_fresnel = self.uniform_locs.get("uFresnelPower", -1)
        loc_spec = self.uniform_locs.get("uSpecularShininess", -1)
        loc_alpha = self.uniform_locs.get("uAlpha", -1)

        if loc_fresnel != -1: glUniform1f(loc_fresnel, float(fresnel_power))
        if loc_spec != -1: glUniform1f(loc_spec, float(specular_shininess))
        if loc_alpha != -1: glUniform1f(loc_alpha, float(alpha))
