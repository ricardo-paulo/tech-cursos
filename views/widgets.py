from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models.course import Course
from resources.icons.vector_assets import RadioIndicator, create_course_pixmap


def make_nav_pill(text: str, active: bool = False) -> QPushButton:
    btn = QPushButton(text)
    btn.setObjectName("NavPill")
    btn.setCursor(QCursor(Qt.PointingHandCursor))
    btn.setProperty("active", active)
    return btn


class AccordionCard(QFrame):
    def __init__(self, title: str, icon_prefix: str = "", standalone: bool = True, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        if standalone:
            self.setObjectName("AccordionCard")

        self._expanded = False

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.trigger_btn = QPushButton()
        self.trigger_btn.setObjectName("AccordionTrigger")
        self.trigger_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.trigger_btn.setMinimumHeight(52)

        btn_layout = QHBoxLayout(self.trigger_btn)
        btn_layout.setContentsMargins(18, 14, 18, 14)

        left_text = f"{icon_prefix}   {title}" if icon_prefix else title
        self.title_lbl = QLabel(left_text)
        self.title_lbl.setStyleSheet("font-size: 13px; font-weight: 700; color: #18181B;")
        self.arrow_lbl = QLabel("⌄")
        self.arrow_lbl.setStyleSheet("font-size: 16px; color: #374151;")

        btn_layout.addWidget(self.title_lbl)
        btn_layout.addStretch()
        btn_layout.addWidget(self.arrow_lbl)

        self.trigger_btn.clicked.connect(self.toggle)
        layout.addWidget(self.trigger_btn)

        self.body_widget = QWidget()
        self.body_layout = QVBoxLayout(self.body_widget)
        self.body_layout.setContentsMargins(20, 4, 20, 16)
        self.body_layout.setSpacing(8)
        self.body_widget.setVisible(False)
        layout.addWidget(self.body_widget)

    def toggle(self):
        self._expanded = not self._expanded
        self.body_widget.setVisible(self._expanded)
        self.arrow_lbl.setText("⌃" if self._expanded else "⌄")

    def set_bullet_items(self, items: List[str]):
        self._clear_body()
        for item in items:
            lbl = QLabel(f"•  {item}")
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 13px; color: #4B5563;")
            self.body_layout.addWidget(lbl)

    def set_custom_widget(self, widget: QWidget):
        self._clear_body()
        self.body_layout.addWidget(widget)

    def _clear_body(self):
        while self.body_layout.count():
            child = self.body_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


class ClickableCourseCard(QFrame):
    clicked = Signal(object)

    def __init__(self, course: Course, parent=None):
        super().__init__(parent)
        self.course = course
        self.setObjectName("CourseCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 18, 20, 18)
        layout.setSpacing(20)

        thumb = QLabel()
        thumb.setPixmap(create_course_pixmap(course.art_key, 168, 126, radius=14))
        thumb.setFixedSize(168, 126)
        layout.addWidget(thumb)

        info_col = QVBoxLayout()
        info_col.setSpacing(6)
        info_col.setAlignment(Qt.AlignVCenter)

        title = QLabel(course.name)
        title.setWordWrap(True)
        title.setStyleSheet("font-size: 17px; font-weight: 700; color: #18181B;")

        desc = QLabel(course.summary or course.description)
        desc.setWordWrap(True)
        desc.setStyleSheet("font-size: 13px; color: #6B7280;")

        price = QLabel(course.formatted_price)
        price.setStyleSheet("font-size: 18px; font-weight: 800; color: #0080FF; margin-top: 6px;")

        info_col.addWidget(title)
        info_col.addWidget(desc)
        info_col.addWidget(price)
        layout.addLayout(info_col, 1)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.course)


class SelectableCard(QFrame):
    clicked = Signal(object)

    def __init__(self, icon_text: str, title: str, subtitle: str = "", value=None, icon_color: str = "#18181B", parent=None):
        super().__init__(parent)
        self.value = value
        self.setObjectName("SelectableCard")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setProperty("selected", False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(14)

        icon_lbl = QLabel(icon_text)
        icon_lbl.setStyleSheet(f"font-size: 20px; color: {icon_color}; font-weight: 700;")
        icon_lbl.setFixedWidth(30)
        icon_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_lbl)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #18181B;")
        text_col.addWidget(title_lbl)

        if subtitle:
            sub_lbl = QLabel(subtitle)
            sub_lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: #4B5563;")
            text_col.addWidget(sub_lbl)

        layout.addLayout(text_col, 1)

        self.radio = RadioIndicator(False)
        layout.addWidget(self.radio)

    def set_selected(self, selected: bool):
        self.setProperty("selected", selected)
        self.radio.set_selected(selected)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self)