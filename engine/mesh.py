"""
3D Mesh Data Structure for Golbem Simulator.
Stores vertex positions, normals, UVs, indices, and bone skin weights.
"""

import numpy as np
from OpenGL.GL import *

class Mesh:
    def __init__(self, name="Mesh"):
        self.name = name
        self.vertices = np.array([], dtype=np.float32) # (N, 3)
        self.normals = np.array([], dtype=np.float32)  # (N, 3)
        self.indices = np.array([], dtype=np.uint32)   # (M,)
        self.bone_names = []
        self.bone_weights = [] # List of tuples: [(bone_name, weight), ...] per vertex

        self.display_list = None

    def build_display_list(self):
        """Compiles mesh vertex array into an OpenGL Display List for fast offline rendering."""
        if len(self.vertices) == 0:
            return

        if self.display_list is None:
            self.display_list = glGenLists(1)

        glNewList(self.display_list, GL_COMPILE)

        has_normals = len(self.normals) == len(self.vertices)

        if len(self.indices) > 0:
            glBegin(GL_TRIANGLES)
            for idx in self.indices:
                if idx < len(self.vertices):
                    if has_normals:
                        glNormal3fv(self.normals[idx])
                    glVertex3fv(self.vertices[idx])
            glEnd()
        else:
            glBegin(GL_TRIANGLES)
            for i in range(len(self.vertices)):
                if has_normals:
                    glNormal3fv(self.normals[i])
                glVertex3fv(self.vertices[i])
            glEnd()

        glEndList()

    def render(self):
        """Renders the compiled OpenGL display list or draws array directly."""
        if self.display_list is not None:
            glCallList(self.display_list)
        elif len(self.vertices) > 0:
            self.build_display_list()
            if self.display_list is not None:
                glCallList(self.display_list)
