"""
Dark Sci-Fi Cyberpunk Qt Stylesheet for PySide6 interface.
"""

DARK_THEME_STYLESHEET = """
QMainWindow {
    background-color: #0B0E14;
    color: #E0F2FE;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

QWidget {
    background-color: #0B0E14;
    color: #E0F2FE;
    font-size: 13px;
}

QGroupBox {
    border: 1px solid #1E293B;
    border-radius: 6px;
    margin-top: 12px;
    font-weight: bold;
    color: #38BDF8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top right;
    padding: 0 8px;
}

QPushButton {
    background-color: #1E293B;
    color: #38BDF8;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #0EA5E9;
    color: #FFFFFF;
    border-color: #38BDF8;
}

QPushButton:pressed {
    background-color: #0284C7;
}

QLineEdit {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 6px 10px;
    color: #F8FAFC;
}

QLineEdit:focus {
    border: 1px solid #38BDF8;
}

QTextEdit, QListWidget, QTreeWidget {
    background-color: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 4px;
    color: #F8FAFC;
}

QSlider::groove:horizontal {
    border: 1px solid #334155;
    height: 6px;
    background: #0F172A;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #38BDF8;
    border: 1px solid #0EA5E9;
    width: 14px;
    margin-top: -4px;
    margin-bottom: -4px;
    border-radius: 7px;
}

QComboBox {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 4px;
    padding: 4px 8px;
    color: #38BDF8;
}

QComboBox QAbstractItemView {
    background-color: #0F172A;
    selection-background-color: #0EA5E9;
    color: #F8FAFC;
}

QStatusBar {
    background-color: #020617;
    border-top: 1px solid #1E293B;
    color: #94A3B8;
}

QMenuBar {
    background-color: #020617;
    color: #E0F2FE;
    border-bottom: 1px solid #1E293B;
}

QMenuBar::item:selected {
    background-color: #1E293B;
    color: #38BDF8;
}

QMenu {
    background-color: #0F172A;
    border: 1px solid #334155;
    color: #E0F2FE;
}

QMenu::item:selected {
    background-color: #0EA5E9;
    color: #FFFFFF;
}
"""
