"""
High-Detail Anatomical Mesh and Internal Organs Generator for Golbem Simulator.
Generates vertex, normal, and anatomical geometry for Skin, Skeletal Bones, Muscle Groups,
and Internal Organs (Heart, Lungs, Liver, Kidneys, Stomach).
"""

import numpy as np
from OpenGL.GL import *

def draw_sphere(radius=1.0, slices=16, stacks=16):
    """Draws a 3D sphere using OpenGL for joints and spherical organ bases."""
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

def draw_cylinder(p1, p2, radius=0.03, slices=16):
    """Draws a 3D cylinder connecting two 3D points p1 and p2."""
    p1 = np.array(p1, dtype=np.float32)
    p2 = np.array(p2, dtype=np.float32)
    v = p2 - p1
    height = float(np.linalg.norm(v))

    if height < 1e-6:
        return

    z_axis = v / height
    if abs(z_axis[2]) > 0.999:
        x_axis = np.array([1, 0, 0], dtype=np.float32)
    else:
        x_axis = np.cross(np.array([0, 0, 1], dtype=np.float32), z_axis)
        x_axis /= np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)

    glPushMatrix()
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

def draw_ellipsoid(center, rx, ry, rz, slices=20, stacks=20):
    """Draws a 3D ellipsoid for anatomical muscle volumes and organ shapes."""
    glPushMatrix()
    glTranslatef(center[0], center[1], center[2])
    glScalef(rx, ry, rz)
    draw_sphere(radius=1.0, slices=slices, stacks=stacks)
    glPopMatrix()

def draw_ribcage(center, num_ribs=10, width=0.20, height=0.28, depth=0.16):
    """Draws detailed thoracic ribcage ribs."""
    cx, cy, cz = center
    for i in range(num_ribs):
        t = i / float(num_ribs)
        ry = cy + (0.5 - t) * height
        r_width = width * np.sin(np.pi * (t * 0.8 + 0.1))
        r_depth = depth * np.sin(np.pi * (t * 0.8 + 0.1))

        glBegin(GL_LINE_LOOP)
        for a in range(24):
            angle = 2.0 * np.pi * a / 24.0
            x = cx + r_width * np.cos(angle)
            z = cz + r_depth * np.sin(angle)
            glNormal3f(np.cos(angle), 0, np.sin(angle))
            glVertex3f(x, ry, z)
        glEnd()

def draw_vertebrae(p_start, p_end, count=12):
    """Draws spinal vertebrae column along spine path."""
    p_start = np.array(p_start, dtype=np.float32)
    p_end = np.array(p_end, dtype=np.float32)
    for i in range(count):
        t = i / float(count)
        pos = p_start + (p_end - p_start) * t
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        draw_sphere(radius=0.035, slices=12, stacks=12)
        glPopMatrix()

# --- Internal Organs 3D Geometry ---

def draw_heart(center):
    """Draws 3D anatomical Heart mesh model inside chest."""
    cx, cy, cz = center
    glPushMatrix()
    glTranslatef(cx - 0.03, cy + 0.02, cz + 0.03) # Left thoracic chest orientation
    glRotatef(15, 0, 0, 1)
    glRotatef(-10, 1, 0, 0)

    # Crimson/Dark Red Heart
    glColor4f(0.85, 0.1, 0.15, 0.95)
    draw_ellipsoid((0, 0, 0), 0.055, 0.075, 0.055)

    # Aorta & Major Vessels
    glColor4f(0.9, 0.2, 0.2, 0.95)
    draw_cylinder((0, 0.04, 0), (0, 0.09, -0.01), radius=0.018)
    glColor4f(0.2, 0.3, 0.8, 0.95) # Vena Cava (Blue)
    draw_cylinder((0.02, 0.03, 0.01), (0.02, 0.08, 0.01), radius=0.015)
    glPopMatrix()

def draw_lungs(center):
    """Draws 3D anatomical Left and Right Lungs."""
    cx, cy, cz = center
    # Pinkish / Coral Lungs
    glColor4f(0.9, 0.5, 0.55, 0.85)

    # Right Lung (Slightly larger, 3 lobes)
    glPushMatrix()
    glTranslatef(cx + 0.08, cy + 0.02, cz + 0.01)
    draw_ellipsoid((0, 0, 0), 0.065, 0.12, 0.075)
    glPopMatrix()

    # Left Lung (Cardiac notch)
    glPushMatrix()
    glTranslatef(cx - 0.08, cy + 0.02, cz + 0.01)
    draw_ellipsoid((0, 0, 0), 0.055, 0.115, 0.070)
    glPopMatrix()

def draw_liver(center):
    """Draws 3D Liver mesh model inside upper right abdomen."""
    cx, cy, cz = center
    glPushMatrix()
    glTranslatef(cx + 0.05, cy - 0.08, cz + 0.02)
    glRotatef(-10, 0, 0, 1)
    # Dark Brownish-Red Liver
    glColor4f(0.55, 0.18, 0.15, 0.95)
    draw_ellipsoid((0, 0, 0), 0.095, 0.055, 0.08)
    glPopMatrix()

def draw_stomach(center):
    """Draws 3D Stomach mesh model inside upper left abdomen."""
    cx, cy, cz = center
    glPushMatrix()
    glTranslatef(cx - 0.06, cy - 0.09, cz + 0.02)
    glRotatef(20, 0, 1, 0)
    # Pinkish-Beige Stomach J-shape
    glColor4f(0.85, 0.55, 0.5, 0.95)
    draw_ellipsoid((0, 0, 0), 0.055, 0.075, 0.05)
    glPopMatrix()

def draw_kidneys(center):
    """Draws 3D Left and Right Kidneys near posterior abdominal wall."""
    cx, cy, cz = center
    # Dark Red-Violet Kidneys
    glColor4f(0.5, 0.15, 0.25, 0.95)

    # Right Kidney (Slightly lower due to liver)
    glPushMatrix()
    glTranslatef(cx + 0.07, cy - 0.14, cz - 0.05)
    draw_ellipsoid((0, 0, 0), 0.035, 0.05, 0.03)
    glPopMatrix()

    # Left Kidney
    glPushMatrix()
    glTranslatef(cx - 0.07, cy - 0.12, cz - 0.05)
    draw_ellipsoid((0, 0, 0), 0.035, 0.05, 0.03)
    glPopMatrix()
