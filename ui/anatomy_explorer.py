"""
Anatomy Explorer Sidebar Widget displaying interactive tree hierarchy for Bones, Joints, Muscles, and Internal Organs.
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLabel, QGroupBox, QTextEdit
)
from PySide6.QtCore import Qt, Signal

ANATOMY_INFO_DATABASE = {
    "Pelvis": {
        "farsi_name": "لگن (Pelvic Girdle)",
        "type": "Skeletal Base / Joint",
        "description": "پایه اصلی و ریشه اسکلتی بدن انسان. مفصل اتصال دهنده ستون فقرات به استخوان‌های ران چپ و راست."
    },
    "Spine": {
        "farsi_name": "ستون فقرات (Vertebral Column)",
        "type": "Skeletal Column",
        "description": "شامل ۲۴ مهره آزاد (گردنی، سینه، کمری) محافظت کننده از نخاع و محور اصلی انعطاف‌پذیری بدن."
    },
    "Chest": {
        "farsi_name": "قفسه سینه (Thoracic Cavity & Ribcage)",
        "type": "Skeletal & Organ Cavity",
        "description": "شامل ۱۲ جفت دنده و استخوان جناغ. محافظت‌کننده از اعضای حیاتی مانند قلب و ریه‌ها."
    },
    "Head": {
        "farsi_name": "جمجمه و سر (Cranium & Head)",
        "type": "Skeletal Skull",
        "description": "استخوان جمجمه محفظه نگهدارنده مغز و اندام‌های حس بینایی، شنوایی، چشایی و بویایی."
    },
    "Left_UpperArm": {
        "farsi_name": "استخوان بازوی چپ (Left Humerus)",
        "type": "Limb Bone",
        "description": "استخوان بلند بازو متصل‌کننده مفصل شانه به مفصل آرنج. دارای ۳ درجه آزادی حرکت."
    },
    "Right_UpperArm": {
        "farsi_name": "استخوان بازوی راست (Right Humerus)",
        "type": "Limb Bone",
        "description": "استخوان بلند بازوی راست متصل‌کننده مفصل شانه به آرنج."
    },
    "Left_UpperLeg": {
        "farsi_name": "استخوان ران چپ (Left Femur)",
        "type": "Limb Bone",
        "description": "بلندترین و قوی‌ترین استخوان بدن انسان. تحمل‌کننده وزن بدن هنگام ایستادن و راه رفتن."
    },
    "Right_UpperLeg": {
        "farsi_name": "استخوان ران راست (Right Femur)",
        "type": "Limb Bone",
        "description": "استخوان ران راست تحمل‌کننده وزن بدن و متصل به مفصل زانو."
    },
    "Heart": {
        "farsi_name": "قلب (Heart)",
        "type": "Internal Organ",
        "description": "عضله حیاتی پمپاژکننده خون در سمت چپ قفسه سینه. دارای ۴ حفره (دهلیزها و بطن‌ها)."
    },
    "Lungs": {
        "farsi_name": "ریه‌ها (Lungs)",
        "type": "Internal Organ",
        "description": "اندام‌های تنفسی راست و چپ مسئول تبادل اکسیژن و دی‌اکسید کربن در قفسه سینه."
    },
    "Liver": {
        "farsi_name": "کبد (Liver)",
        "type": "Internal Organ",
        "description": "بزرگ‌ترین غده بدن در بخش راست بالای شکم. مسئول سم‌زدایی، متابولیسم و تولید صفرا."
    },
    "Stomach": {
        "farsi_name": "معده (Stomach)",
        "type": "Internal Organ",
        "description": "اندام گوارشی J شکل در سمت چپ بالای شکم برای ذخیره و هضم اولیه غذا."
    },
    "Kidneys": {
        "farsi_name": "کلیه‌ها (Kidneys)",
        "type": "Internal Organ",
        "description": "اندام‌های لوبیاشکل تصفیه‌کننده خون و تنظیم‌کننده مایعات و الکترولیت‌های بدن."
    },
}

class AnatomyExplorerWidget(QWidget):
    item_selected = Signal(str)

    def __init__(self, skeleton, parent=None):
        super().__init__(parent)
        self.skeleton = skeleton
        self.setLayoutDirection(Qt.RightToLeft)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        group = QGroupBox("کاشف آناتومی (Anatomy Explorer)")
        group_layout = QVBoxLayout(group)

        # Search / Hierarchy Tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("ساختار آناتومیک")
        self.tree.itemClicked.connect(self._on_item_clicked)
        self._populate_anatomy_tree()
        group_layout.addWidget(self.tree)

        # Inspection Details Panel
        group_layout.addWidget(QLabel("اطلاعات بخش انتخاب‌شده:"))
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(180)
        self.info_text.setPlaceholderText("برای مشاهده جزئیات آناتومیک، یک بخش را انتخاب کنید...")
        group_layout.addWidget(self.info_text)

        layout.addWidget(group)

    def _populate_anatomy_tree(self):
        self.tree.clear()

        # Skeleton Branch
        skel_item = QTreeWidgetItem(["اسکلت و مفاصل (Skeleton)"])
        self.tree.addTopLevelItem(skel_item)
        if self.skeleton.root:
            self._add_joint_tree_item(self.skeleton.root, skel_item)

        # Muscles Branch
        muscles_item = QTreeWidgetItem(["عضلات و بافت نرم (Muscles)"])
        self.tree.addTopLevelItem(muscles_item)
        muscles_item.addChild(QTreeWidgetItem(["عضلات قفسه سینه و شکم"]))
        muscles_item.addChild(QTreeWidgetItem(["عضلات بازو و شانه"]))
        muscles_item.addChild(QTreeWidgetItem(["عضلات ران و ساق پا"]))

        # Internal Organs Branch
        organs_item = QTreeWidgetItem(["اندام‌های داخلی (Internal Organs)"])
        self.tree.addTopLevelItem(organs_item)
        for organ_key in ["Heart", "Lungs", "Liver", "Stomach", "Kidneys"]:
            farsi_title = ANATOMY_INFO_DATABASE.get(organ_key, {}).get("farsi_name", organ_key)
            item = QTreeWidgetItem([farsi_title])
            item.setData(0, Qt.UserRole, organ_key)
            organs_item.addChild(item)

        self.tree.expandAll()

    def _add_joint_tree_item(self, joint, parent_item):
        joint_item = QTreeWidgetItem([joint.name])
        joint_item.setData(0, Qt.UserRole, joint.name)
        parent_item.addChild(joint_item)
        for child in joint.children:
            self._add_joint_tree_item(child, joint_item)

    def _on_item_clicked(self, item, column):
        item_key = item.data(0, Qt.UserRole) or item.text(0)
        self.display_item_info(item_key)
        self.item_selected.emit(item_key)

    def display_item_info(self, item_key: str):
        info = ANATOMY_INFO_DATABASE.get(item_key)
        if info:
            text = (
                f"<b>عنوان:</b> {info['farsi_name']}<br>"
                f"<b>نوع:</b> {info['type']}<br><br>"
                f"<b>توضیحات آناتومیک:</b><br>{info['description']}"
            )
        else:
            text = f"<b>نام بخش:</b> {item_key}<br>بخش آناتومیک انتخاب‌شده."

        self.info_text.setHtml(text)
