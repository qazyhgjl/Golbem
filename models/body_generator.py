"""
High-Detail Anatomical Mesh and Internal Organs Generator for Golbem Simulator.
Generates vertex, normal, and anatomical geometry for Skin, Skeletal Bones, Muscle Groups,
and Sculpted 3D Internal Organs (Heart, Lungs, Liver, Kidneys, Stomach) with surface normals.
"""

import numpy as np
from OpenGL.GL import *

def draw_sphere(radius=1.0, slices=20, stacks=20):
    """Draws a 3D sphere with vertex normals for smooth GL lighting."""
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

def draw_cylinder(p1, p2, radius=0.03, slices=20):
    """Draws a 3D cylinder connecting two 3D points p1 and p2 with smooth normals."""
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

def draw_ellipsoid(center, rx, ry, rz, slices=24, stacks=24):
    """Draws a 3D ellipsoid for anatomical muscle volumes and organ shapes."""
    glPushMatrix()
    glTranslatef(center[0], center[1], center[2])
    glScalef(rx, ry, rz)
    draw_sphere(radius=1.0, slices=slices, stacks=stacks)
    glPopMatrix()

def draw_ribcage(center, num_ribs=10, width=0.20, height=0.28, depth=0.16):
    """Draws thoracic ribcage with 3D anatomical rib rings."""
    cx, cy, cz = center
    for i in range(num_ribs):
        t = i / float(num_ribs)
        ry = cy + (0.5 - t) * height
        r_width = width * np.sin(np.pi * (t * 0.8 + 0.1))
        r_depth = depth * np.sin(np.pi * (t * 0.8 + 0.1))

        glBegin(GL_LINE_LOOP)
        for a in range(28):
            angle = 2.0 * np.pi * a / 28.0
            x = cx + r_width * np.cos(angle)
            z = cz + r_depth * np.sin(angle)
            glNormal3f(np.cos(angle), 0, np.sin(angle))
            glVertex3f(x, ry, z)
        glEnd()

def draw_vertebrae(p_start, p_end, count=14):
    """Draws spinal vertebrae column along spine path."""
    p_start = np.array(p_start, dtype=np.float32)
    p_end = np.array(p_end, dtype=np.float32)
    for i in range(count):
        t = i / float(count)
        pos = p_start + (p_end - p_start) * t
        glPushMatrix()
        glTranslatef(pos[0], pos[1], pos[2])
        draw_sphere(radius=0.036, slices=14, stacks=14)
        glPopMatrix()

# --- Sculpted 3D Anatomical Organs ---

def draw_heart(center):
    """Draws sculpted 3D anatomical Heart with ventricles, atria, and major vascular arches."""
    cx, cy, cz = center
    glPushMatrix()
    glTranslatef(cx - 0.03, cy + 0.02, cz + 0.03) # Left thoracic cavity position
    glRotatef(18, 0, 0, 1)
    glRotatef(-12, 1, 0, 0)

    # Ventricular muscular body
    draw_ellipsoid((0, 0, 0), 0.058, 0.078, 0.058)

    # Left & Right Atrial appendages
    draw_ellipsoid((-0.02, 0.04, 0.01), 0.032, 0.032, 0.032)
    draw_ellipsoid((0.02, 0.04, 0.01), 0.030, 0.030, 0.030)

    # Aortic arch & Pulmonary artery
    draw_cylinder((0, 0.04, 0), (0, 0.09, -0.01), radius=0.018)
    draw_cylinder((0.02, 0.03, 0.01), (0.02, 0.08, 0.01), radius=0.015)
    glPopMatrix()

def draw_lungs(center):
    """Draws 3D anatomical Left and Right Lungs with lobed surfaces."""
    cx, cy, cz = center

    # Right Lung (3 anatomical lobes)
    glPushMatrix()
    glTranslatef(cx + 0.085, cy + 0.02, cz + 0.01)
    draw_ellipsoid((0, 0.03, 0), 0.065, 0.05, 0.075)   # Superior lobe
    draw_ellipsoid((0, -0.01, 0), 0.068, 0.04, 0.078)  # Middle lobe
    draw_ellipsoid((0, -0.05, 0), 0.062, 0.05, 0.072)  # Inferior lobe
    glPopMatrix()

    # Left Lung (2 anatomical lobes + Cardiac notch)
    glPushMatrix()
    glTranslatef(cx - 0.085, cy + 0.02, cz + 0.01)
    draw_ellipsoid((0, 0.025, 0), 0.056, 0.055, 0.070) # Superior lobe
    draw_ellipsoid((0, -0.04, 0), 0.054, 0.050, 0.068) # Inferior lobe
    glPopMatrix()

def draw_liver(center):
    """Draws 3D anatomical Liver with distinct right and left lobes."""
    cx, cy, cz = center
    glPushMatrix()
    glTranslatef(cx + 0.05, cy - 0.08, cz + 0.02)
    glRotatef(-10, 0, 0, 1)

    # Right lobe (large)
    draw_ellipsoid((0.02, 0, 0), 0.085, 0.055, 0.080)
    # Left lobe (tapered)
    draw_ellipsoid((-0.05, 0.01, 0), 0.055, 0.040, 0.060)
    glPopMatrix()

def draw_stomach(center):
    """Draws 3D J-curved anatomical Stomach with fundus and pylorus."""
    cx, cy, cz = center
    glPushMatrix()
    glTranslatef(cx - 0.06, cy - 0.09, cz + 0.02)
    glRotatef(22, 0, 1, 0)

    # Fundus & Body curvature
    draw_ellipsoid((0, 0.02, 0), 0.048, 0.052, 0.048)  # Fundus
    draw_ellipsoid((0, -0.03, 0), 0.058, 0.068, 0.052) # Stomach body
    draw_ellipsoid((0.03, -0.06, 0), 0.032, 0.038, 0.032) # Pylorus
    glPopMatrix()

def draw_kidneys(center):
    """Draws 3D bean-shaped Left and Right Kidneys."""
    cx, cy, cz = center

    # Right Kidney
    glPushMatrix()
    glTranslatef(cx + 0.07, cy - 0.14, cz - 0.05)
    draw_ellipsoid((0, 0, 0), 0.036, 0.052, 0.032)
    glPopMatrix()

    # Left Kidney
    glPushMatrix()
    glTranslatef(cx - 0.07, cy - 0.12, cz - 0.05)
    draw_ellipsoid((0, 0, 0), 0.036, 0.052, 0.032)
    glPopMatrix()
