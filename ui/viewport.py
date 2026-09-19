"""
PySide6 3D OpenGL Viewport widget with interactive mouse camera controls.
"""

from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QMouseEvent, QWheelEvent

from engine.renderer import Renderer
from app.settings import TARGET_FPS

class ViewportWidget(QOpenGLWidget):
    fps_updated = Signal(float)

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.renderer = Renderer(scene)

        self.last_mouse_pos = None
        self.fps_timer = QTimer(self)
        self.fps_timer.timeout.connect(self.update_viewport)
        self.fps_timer.start(int(1000 / TARGET_FPS))

        self.frame_count = 0
        self.last_fps_time = 0

    def initializeGL(self):
        self.renderer.setup_gl(self.width(), self.height())

    def resizeGL(self, width, height):
        self.renderer.setup_gl(width, height)

    def paintGL(self):
        self.renderer.render()

    def update_viewport(self):
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        self.last_mouse_pos = event.position()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_mouse_pos is None:
            return

        delta = event.position() - self.last_mouse_pos
        self.last_mouse_pos = event.position()

        if event.buttons() & Qt.LeftButton:
            # Orbit camera
            self.scene.camera.orbit(delta.x() * 0.5, delta.y() * 0.5)
        elif event.buttons() & Qt.RightButton:
            # Pan camera
            self.scene.camera.pan(-delta.x() * 0.005, delta.y() * 0.005)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.last_mouse_pos = None

    def wheelEvent(self, event: QWheelEvent):
        # Zoom camera
        delta_angle = event.angleDelta().y() / 120.0
        self.scene.camera.zoom(delta_angle * 0.25)
