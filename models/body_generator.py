"""
Procedural 3D Mesh Generator for Bones, Muscle Volumes, and Outer Semi-Transparent Skin.
"""

import numpy as np
from OpenGL.GL import *

def draw_sphere(radius=1.0, slices=16, stacks=16):
    """Draws a 3D sphere using OpenGL for joint markers."""
    for i in range(stacks):
        lat0 = np.pi * (-0.5 + float(i) / stacks)
        z0 = radius * np.sin(lat0)
        zr0 = radius * np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(i + 1) / stacks)
        z1 = radius * np.sin(lat1)
        zr1 = radius * np.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * np.pi * float(j) / slices
            x = np.cos(lng)
            y = np.sin(lng)

            glNormal3f(x * zr0 / radius, y * zr0 / radius, z0 / radius)
            glVertex3f(x * zr0, y * zr0, z0)

            glNormal3f(x * zr1 / radius, y * zr1 / radius, z1 / radius)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def draw_cylinder(p1, p2, radius=0.03, slices=12):
    """Draws a 3D cylinder connecting two 3D points p1 and p2."""
    p1 = np.array(p1, dtype=np.float32)
    p2 = np.array(p2, dtype=np.float32)
    v = p2 - p1
    height = float(np.linalg.norm(v))

    if height < 1e-6:
        return

    # Calculate local orientation axes where local Z aligns with vector v
    z_axis = v / height
    if abs(z_axis[2]) > 0.999:
        x_axis = np.array([1, 0, 0], dtype=np.float32)
    else:
        x_axis = np.cross(np.array([0, 0, 1], dtype=np.float32), z_axis)
        x_axis /= np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)

    glPushMatrix()
    # Construct 4x4 matrix in OpenGL column-major order:
    # Column 0: x_axis (with w=0)
    # Column 1: y_axis (with w=0)
    # Column 2: z_axis (with w=0)
    # Column 3: p1 translation (with w=1)
    M = np.array([
        [x_axis[0], x_axis[1], x_axis[2], 0.0],
        [y_axis[0], y_axis[1], y_axis[2], 0.0],
        [z_axis[0], z_axis[1], z_axis[2], 0.0],
        [p1[0],     p1[1],     p1[2],     1.0]
    ], dtype=np.float32)

    glMultMatrixf(M)

    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        angle = 2.0 * np.pi * i / slices
        nx = np.cos(angle)
        ny = np.sin(angle)

        glNormal3f(nx, ny, 0.0)
        glVertex3f(radius * nx, radius * ny, 0.0)
        glVertex3f(radius * nx, radius * ny, height)
    glEnd()

    glPopMatrix()

def draw_ellipsoid(center, rx, ry, rz, slices=16, stacks=16):
    """Draws a 3D ellipsoid for anatomical muscle volumes and skin contours."""
    glPushMatrix()
    glTranslatef(center[0], center[1], center[2])
    glScalef(rx, ry, rz)
    draw_sphere(radius=1.0, slices=slices, stacks=stacks)
    glPopMatrix()
