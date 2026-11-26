from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from models.class_model import Lesson
from models.course import Course
from resources.icons.vector_assets import create_course_pixmap
from views.widgets import AccordionCard, make_nav_pill


class CourseDetailsView(QWidget):
    go_back = Signal()
    go_checkout = Signal()
    toggle_favorite_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RootPage")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        topbar = QFrame()
        topbar.setObjectName("SubTopBar")
        topbar.setFixedHeight(68)
        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(28, 0, 32, 0)

        back_btn = QPushButton("<")
        back_btn.setObjectName("BackBtn")
        back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        back_btn.clicked.connect(self.go_back.emit)

        page_title = QLabel("DETALHES DO CURSO")
        page_title.setStyleSheet("font-size: 16px; font-weight: 800; letter-spacing: 0.6px; color: #18181B;")

        explore_btn = make_nav_pill("🔍  Explorar")
        explore_btn.clicked.connect(self.go_back.emit)

        self.heart_btn = QPushButton("♥")
        self.heart_btn.setObjectName("HeartBtn")
        self.heart_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.heart_btn.clicked.connect(self.toggle_favorite_requested.emit)

        top_layout.addWidget(back_btn)
        top_layout.addSpacing(8)
        top_layout.addWidget(page_title)
        top_layout.addStretch()
        top_layout.addWidget(explore_btn)
        top_layout.addSpacing(8)
        top_layout.addWidget(self.heart_btn)
        root.addWidget(topbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setObjectName("ScrollContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 34, 40, 48)
        content_layout.setAlignment(Qt.AlignTop)

        inner = QWidget()
        inner.setMaximumWidth(1100)
        cols = QHBoxLayout(inner)
        cols.setContentsMargins(0, 0, 0, 0)
        cols.setSpacing(40)
        cols.setAlignment(Qt.AlignTop)

        left_col = QVBoxLayout()
        left_col.setSpacing(16)

        self.hero_label = QLabel()
        self.hero_label.setFixedSize(500, 310)
        left_col.addWidget(self.hero_label)

        self.acc_syllabus = AccordionCard("CONTEÚDO DO CURSO")
        self.acc_learn = AccordionCard("O QUE VOCÊ VAI APRENDER")
        left_col.addWidget(self.acc_syllabus)
        left_col.addWidget(self.acc_learn)
        left_col.addStretch()

        right_col = QVBoxLayout()
        right_col.setSpacing(14)
        right_col.setAlignment(Qt.AlignTop)

        self.title_lbl = QLabel()
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setStyleSheet("font-size: 27px; font-weight: 800; color: #18181B;")

        self.price_lbl = QLabel()
        self.price_lbl.setStyleSheet("font-size: 21px; font-weight: 800; color: #0080FF;")

        self.desc_lbl = QLabel()
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setStyleSheet("font-size: 15px; color: #374151;")

        self.meta_lbl = QLabel()
        self.meta_lbl.setStyleSheet("font-size: 12px; font-weight: 700; color: #1F2937; margin-top: 6px;")

        cta_btn = QPushButton("ESCOLHER TURMA")
        cta_btn.setObjectName("PrimaryBtn")
        cta_btn.setCursor(QCursor(Qt.PointingHandCursor))
        cta_btn.setMinimumHeight(48)
        cta_btn.setMaximumWidth(420)
        cta_btn.clicked.connect(self.go_checkout.emit)

        right_col.addWidget(self.title_lbl)
        right_col.addWidget(self.price_lbl)
        right_col.addWidget(self.desc_lbl)
        right_col.addWidget(self.meta_lbl)
        right_col.addSpacing(12)
        right_col.addWidget(cta_btn)
        right_col.addStretch()

        cols.addLayout(left_col, 1)
        cols.addLayout(right_col, 1)

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(inner, 1)
        center_row.addStretch()
        content_layout.addLayout(center_row)

        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def set_course(self, course: Course, lessons: List[Lesson], is_favorite: bool):
        self.hero_label.setPixmap(create_course_pixmap(course.art_key, 500, 310, radius=18))
        self.title_lbl.setText(course.name.upper())
        self.price_lbl.setText(course.formatted_price)
        self.desc_lbl.setText(course.description)
        self.meta_lbl.setText(course.formatted_meta)
        self.acc_syllabus.set_bullet_items(
            [f"{lesson.title} ({lesson.duration_minutes} min)" for lesson in lessons]
        )
        self.acc_learn.set_bullet_items(course.learnings)
        self.set_favorite(is_favorite)

    def set_favorite(self, is_favorite: bool):
        self.heart_btn.setText("♥" if is_favorite else "♡")