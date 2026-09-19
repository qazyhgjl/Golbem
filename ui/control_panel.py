"""
Manual Joint Control Panel widget with bone tree, XYZ rotation sliders, and reset buttons.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QSlider, QLabel, QPushButton, QGroupBox
)
from PySide6.QtCore import Qt

class ControlPanel(QWidget):
    def __init__(self, skeleton, parent=None):
        super().__init__(parent)
        self.skeleton = skeleton
        self.selected_joint_name = "Pelvis"
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        group = QGroupBox("کنترل دستی مفاصل و اسکلت")
        group_layout = QVBoxLayout(group)

        # Joint Tree Widget
        group_layout.addWidget(QLabel("انتخاب مفصل:"))
        self.joint_tree = QTreeWidget()
        self.joint_tree.setHeaderLabel("ساختار اسکلت")
        self.joint_tree.itemClicked.connect(self._on_joint_selected)
        self._populate_joint_tree()
        group_layout.addWidget(self.joint_tree)

        # Joint Info Label
        self.lbl_joint_info = QLabel("مفصل انتخاب‌شده: Pelvis")
        self.lbl_joint_info.setStyleSheet("color: #38BDF8; font-weight: bold;")
        group_layout.addWidget(self.lbl_joint_info)

        # XYZ Sliders
        self.sliders = {}
        self.labels = {}

        for axis in ['X', 'Y', 'Z']:
            row = QHBoxLayout()
            lbl_axis = QLabel(f"چرخش {axis}:")
            lbl_val = QLabel("0°")

            slider = QSlider(Qt.Horizontal)
            slider.setRange(-180, 180)
            slider.setValue(0)
            slider.valueChanged.connect(self._on_slider_changed)

            row.addWidget(lbl_axis)
            row.addWidget(slider)
            row.addWidget(lbl_val)
            group_layout.addLayout(row)

            self.sliders[axis] = slider
            self.labels[axis] = lbl_val

        # Reset Buttons
        btn_layout = QHBoxLayout()
        btn_reset_joint = QPushButton("ریست مفصل")
        btn_reset_joint.clicked.connect(self._on_reset_joint)

        btn_reset_all = QPushButton("ریست کامل اسکلت")
        btn_reset_all.clicked.connect(self._on_reset_all)

        btn_layout.addWidget(btn_reset_joint)
        btn_layout.addWidget(btn_reset_all)
        group_layout.addLayout(btn_layout)

        layout.addWidget(group)

    def _populate_joint_tree(self):
        self.joint_tree.clear()
        if self.skeleton.root:
            root_item = QTreeWidgetItem([self.skeleton.root.name])
            self.joint_tree.addTopLevelItem(root_item)
            self._add_joint_children_to_tree(self.skeleton.root, root_item)
            self.joint_tree.expandAll()

    def _add_joint_children_to_tree(self, joint, parent_item):
        for child in joint.children:
            child_item = QTreeWidgetItem([child.name])
            parent_item.addChild(child_item)
            self._add_joint_children_to_tree(child, child_item)

    def _on_joint_selected(self, item, column):
        self.selected_joint_name = item.text(0)
        self.lbl_joint_info.setText(f"مفصل انتخاب‌شده: {self.selected_joint_name}")
        self.update_sliders_from_skeleton()

    def update_sliders_from_skeleton(self):
        if self.selected_joint_name in self.skeleton.joints:
            joint = self.skeleton.joints[self.selected_joint_name]
            rx, ry, rz = joint.rotation
            self.sliders['X'].blockSignals(True)
            self.sliders['Y'].blockSignals(True)
            self.sliders['Z'].blockSignals(True)

            self.sliders['X'].setValue(int(rx))
            self.sliders['Y'].setValue(int(ry))
            self.sliders['Z'].setValue(int(rz))

            self.labels['X'].setText(f"{int(rx)}°")
            self.labels['Y'].setText(f"{int(ry)}°")
            self.labels['Z'].setText(f"{int(rz)}°")

            self.sliders['X'].blockSignals(False)
            self.sliders['Y'].blockSignals(False)
            self.sliders['Z'].blockSignals(False)

    def _on_slider_changed(self):
        rx = self.sliders['X'].value()
        ry = self.sliders['Y'].value()
        rz = self.sliders['Z'].value()

        self.labels['X'].setText(f"{rx}°")
        self.labels['Y'].setText(f"{ry}°")
        self.labels['Z'].setText(f"{rz}°")

        self.skeleton.set_joint_rotation(self.selected_joint_name, rx, ry, rz)

    def _on_reset_joint(self):
        if self.selected_joint_name in self.skeleton.joints:
            self.skeleton.joints[self.selected_joint_name].reset_rotation()
            self.skeleton.update_kinematics()
            self.update_sliders_from_skeleton()

    def _on_reset_all(self):
        self.skeleton.reset_pose()
        self.update_sliders_from_skeleton()
