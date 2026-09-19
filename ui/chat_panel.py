"""
Persian Chat Panel widget supporting RTL layout, history, status, quick buttons, and stop command.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QGroupBox
)
from PySide6.QtCore import Qt, Signal

class ChatPanel(QWidget):
    command_submitted = Signal(str)
    stop_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayoutDirection(Qt.RightToLeft)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Title Group
        group = QGroupBox("پنل چت و دستورات فارسی")
        group_layout = QVBoxLayout(group)

        # Chat History Window
        self.history_display = QTextEdit()
        self.history_display.setReadOnly(True)
        self.history_display.setPlaceholderText("تاریخچه پیام‌ها و دستورات...")
        group_layout.addWidget(self.history_display)

        # Status Label
        self.status_label = QLabel("وضعیت: آماده دریافت دستور")
        self.status_label.setStyleSheet("color: #38BDF8; font-weight: bold;")
        group_layout.addWidget(self.status_label)

        # Quick Command Buttons
        quick_btn_layout = QHBoxLayout()
        btn_stop = QPushButton("🛑 توقف کامل")
        btn_stop.setStyleSheet("background-color: #7F1D1D; color: #FCA5A5; font-weight: bold;")
        btn_stop.clicked.connect(self._on_stop_clicked)

        btn_clear = QPushButton("🗑️ پاک کردن چت")
        btn_clear.clicked.connect(self.clear_history)

        quick_btn_layout.addWidget(btn_stop)
        quick_btn_layout.addWidget(btn_clear)
        group_layout.addLayout(quick_btn_layout)

        # Input Row
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("دستور فارسی را وارد کنید... (مثال: ۳۰ ثانیه بدو)")
        self.input_field.returnPressed.connect(self._on_send_clicked)

        btn_send = QPushButton("ارسال ↵")
        btn_send.clicked.connect(self._on_send_clicked)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(btn_send)
        group_layout.addLayout(input_layout)

        layout.addWidget(group)

        # Initial Welcome Message
        self.append_system_message("سیستم شبیه‌ساز حرکت انسان آماده است. می‌توانید به زبان فارسی دستور دهید.")

    def _on_send_clicked(self):
        text = self.input_field.text().strip()
        if text:
            self.append_user_message(text)
            self.input_field.clear()
            self.command_submitted.emit(text)

    def _on_stop_clicked(self):
        self.stop_clicked.emit()
        self.append_system_message("🛑 دستور توقف توسط کاربر صادر شد.")

    def append_user_message(self, text: str):
        formatted = f"<div align='right' style='color:#38BDF8;'><b>کاربر:</b> {text}</div>"
        self.history_display.append(formatted)

    def append_system_message(self, text: str, is_error: bool = False):
        color = "#F87171" if is_error else "#34D399"
        formatted = f"<div align='right' style='color:{color};'><b>سیستم:</b> {text}</div>"
        self.history_display.append(formatted)

    def set_status(self, text: str):
        self.status_label.setText(f"وضعیت: {text}")

    def clear_history(self):
        self.history_display.clear()
        self.append_system_message("تاریخچه چت پاک شد.")
