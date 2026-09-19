"""
Main Window integrating 3D Viewport, Persian Chat Panel, Manual Joint Control Panel, Menu Bar, and Status Bar.
"""

import sys
import time
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QComboBox, QLabel, QSlider, QPushButton, QStatusBar, QMenuBar, QMenu
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction

from app.settings import APP_NAME, APP_VERSION, DISPLAY_MODES, MODE_SKIN
from app.logger import logger
from engine.scene import Scene
from animation.animation_controller import AnimationController
from command.executor import CommandExecutor
from ui.viewport import ViewportWidget
from ui.chat_panel import ChatPanel
from ui.control_panel import ControlPanel
from ui.theme import DARK_THEME_STYLESHEET

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1360, 850)
        self.setStyleSheet(DARK_THEME_STYLESHEET)

        # Initialize Core Engines
        self.scene = Scene()
        self.animation_controller = AnimationController(self.scene.skeleton)
        self.command_executor = CommandExecutor(self.animation_controller)

        # Build UI Components
        self._setup_menu_bar()
        self._setup_central_widget()
        self._setup_status_bar()

        # Timer for animation loop
        self.last_update_time = time.time()
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self._on_animation_tick)
        self.anim_timer.start(16) # ~60 FPS update

    def _setup_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File / فایل")
        exit_action = QAction("خروج", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View Menu
        view_menu = menubar.addMenu("View / نمای ۳بعدی")
        mode_menu = QMenu("حالت‌های نمایش", self)
        for mode_name in DISPLAY_MODES:
            act = QAction(mode_name, self)
            act.triggered.connect(lambda checked=False, m=mode_name: self._set_display_mode(m))
            mode_menu.addAction(act)
        view_menu.addMenu(mode_menu)

        grid_action = QAction("نمایش/مخفی‌سازی گرید", self)
        grid_action.triggered.connect(self._toggle_grid)
        view_menu.addAction(grid_action)

        # Skeleton Menu
        skel_menu = menubar.addMenu("Skeleton / اسکلت")
        reset_skel_action = QAction("بازنشانی حالت اولیه (Idle)", self)
        reset_skel_action.triggered.connect(self._reset_skeleton)
        skel_menu.addAction(reset_skel_action)

        # Chat Menu
        chat_menu = menubar.addMenu("Chat / چت")
        clear_chat_action = QAction("پاک‌کردن تاریخچه", self)
        clear_chat_action.triggered.connect(lambda: self.chat_panel.clear_history())
        chat_menu.addAction(clear_chat_action)

        # Help Menu
        help_menu = menubar.addMenu("Help / راهنما")
        about_action = QAction("درباره برنامه", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_central_widget(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(4, 4, 4, 4)

        splitter = QSplitter(Qt.Horizontal)

        # Left/Center: Viewport + Controls Top Toolbar
        viewport_container = QWidget()
        vp_layout = QVBoxLayout(viewport_container)
        vp_layout.setContentsMargins(0, 0, 0, 0)

        # Viewport Toolbar
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("حالت نمایش:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(DISPLAY_MODES)
        self.combo_mode.currentTextChanged.connect(self._set_display_mode)
        toolbar.addWidget(self.combo_mode)

        toolbar.addWidget(QLabel("دید دوربین:"))
        combo_cam = QComboBox()
        combo_cam.addItems(["جلو", "پشت", "چپ", "راست", "سه چهارم"])
        combo_cam.currentTextChanged.connect(lambda name: self.scene.camera.set_view_preset(name))
        toolbar.addWidget(combo_cam)

        btn_reset_cam = QPushButton("ریست دوربین")
        btn_reset_cam.clicked.connect(lambda: self.scene.camera.reset())
        toolbar.addWidget(btn_reset_cam)

        toolbar.addStretch()
        vp_layout.addLayout(toolbar)

        # 3D Viewport Widget
        self.viewport_widget = ViewportWidget(self.scene)
        vp_layout.addWidget(self.viewport_widget)

        splitter.addWidget(viewport_container)

        # Right: Tab/Splitter for Persian Chat & Manual Control Panel
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)

        right_splitter = QSplitter(Qt.Vertical)

        # Persian Chat Panel
        self.chat_panel = ChatPanel()
        self.chat_panel.command_submitted.connect(self._on_persian_command)
        self.chat_panel.stop_clicked.connect(self._on_stop_animation)
        right_splitter.addWidget(self.chat_panel)

        # Manual Joint Control Panel
        self.control_panel = ControlPanel(self.scene.skeleton)
        right_splitter.addWidget(self.control_panel)

        right_layout.addWidget(right_splitter)
        splitter.addWidget(right_container)

        # Set proportions: Viewport 65%, Side panel 35%
        splitter.setSizes([850, 450])
        main_layout.addWidget(splitter)

    def _setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.lbl_fps = QLabel("FPS: 60.0")
        self.lbl_motion = QLabel("حرکت فعلی: Idle")
        self.lbl_speed = QLabel("سرعت پخش: 1.0x")

        # Play / Pause / Speed controls
        self.btn_pause = QPushButton("⏸️ توقف موقت")
        self.btn_pause.clicked.connect(self._toggle_pause)

        slider_speed = QSlider(Qt.Horizontal)
        slider_speed.setRange(1, 30) # 0.1x to 3.0x
        slider_speed.setValue(10)
        slider_speed.setMaximumWidth(120)
        slider_speed.valueChanged.connect(self._on_speed_changed)

        self.status_bar.addPermanentWidget(self.lbl_fps)
        self.status_bar.addPermanentWidget(self.lbl_motion)
        self.status_bar.addPermanentWidget(self.btn_pause)
        self.status_bar.addPermanentWidget(QLabel("سرعت:"))
        self.status_bar.addPermanentWidget(slider_speed)
        self.status_bar.addPermanentWidget(self.lbl_speed)

    def _set_display_mode(self, mode: str):
        self.scene.set_display_mode(mode)
        self.combo_mode.setCurrentText(mode)

    def _toggle_grid(self):
        self.scene.show_grid = not self.scene.show_grid

    def _reset_skeleton(self):
        self.animation_controller.stop()
        self.control_panel.update_sliders_from_skeleton()
        self.chat_panel.append_system_message("حالت اسکلت به Idle بازنشانی شد.")

    def _show_about(self):
        self.chat_panel.append_system_message(
            f"<b>{APP_NAME}</b><br>نسخه {APP_VERSION}<br>سیستم شبیه‌سازی ۳بعدی بدن انسان با کنترل دستورات فارسی (آفلاین)"
        )

    def _on_persian_command(self, text: str):
        res = self.command_executor.execute_text_command(text)
        if res["success"]:
            self.chat_panel.append_system_message(res["message"])
            self.chat_panel.set_status(f"در حال اجرای {self.animation_controller.current_motion_name}")
        else:
            self.chat_panel.append_system_message(res["message"], is_error=True)
            self.chat_panel.set_status("خطا در تفسیر دستور")

    def _on_stop_animation(self):
        self.animation_controller.stop()
        self.chat_panel.set_status("حرکات متوقف شدند.")

    def _toggle_pause(self):
        if self.animation_controller.is_paused:
            self.animation_controller.resume()
            self.btn_pause.setText("⏸️ توقف موقت")
        else:
            self.animation_controller.pause()
            self.btn_pause.setText("▶️ ادامه")

    def _on_speed_changed(self, val: int):
        speed = val / 10.0
        self.animation_controller.speed = speed
        self.lbl_speed.setText(f"سرعت پخش: {speed:.1f}x")

    def _on_animation_tick(self):
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        # Update animation step
        self.animation_controller.update(dt)

        # Update manual joint slider UI if animation is active
        if self.animation_controller.is_playing:
            self.control_panel.update_sliders_from_skeleton()

        # Update status labels
        self.lbl_motion.setText(f"حرکت فعلی: {self.animation_controller.current_motion_name}")
        if dt > 0:
            self.lbl_fps.setText(f"FPS: {min(60.0, 1.0 / dt):.1f}")
