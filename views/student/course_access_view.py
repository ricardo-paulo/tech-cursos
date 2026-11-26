from typing import List, Set

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from models.class_model import Lesson
from models.course import Course
from resources.icons.vector_assets import create_course_pixmap
from views.widgets import AccordionCard, make_nav_pill


class CourseAccessView(QWidget):
    go_home = Signal()
    lesson_toggled = Signal(int, bool)
    watch_lesson = Signal(str)

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
        back_btn.clicked.connect(self.go_home.emit)

        title = QLabel("Meus cursos")
        title.setStyleSheet("font-size: 17px; font-weight: 700; color: #18181B;")

        nav_home = make_nav_pill("🏠  Início")
        nav_home.clicked.connect(self.go_home.emit)
        nav_courses = make_nav_pill("📖  Meus cursos", active=True)
        nav_profile = make_nav_pill("👤  Perfil")

        top_layout.addWidget(back_btn)
        top_layout.addSpacing(8)
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(nav_home)
        top_layout.addWidget(nav_courses)
        top_layout.addWidget(nav_profile)
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
        cols.setSpacing(38)
        cols.setAlignment(Qt.AlignTop)

        left_col = QVBoxLayout()
        left_col.setSpacing(12)

        self.hero_label = QLabel()
        self.hero_label.setFixedSize(500, 310)
        left_col.addWidget(self.hero_label)

        self.course_title_lbl = QLabel()
        self.course_title_lbl.setWordWrap(True)
        self.course_title_lbl.setStyleSheet(
            'font-family: Georgia, "Times New Roman", serif; '
            "font-size: 22px; font-weight: 700; color: #18181B; margin-top: 8px;"
        )

        self.progress_lbl = QLabel("0% concluído")
        self.progress_lbl.setStyleSheet("font-size: 13px; font-weight: 600; color: #374151;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("CourseProgress")
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

        left_col.addWidget(self.course_title_lbl)
        left_col.addWidget(self.progress_lbl)
        left_col.addWidget(self.progress_bar)
        left_col.addStretch()

        modules_box = QFrame()
        modules_box.setObjectName("ModulesContainer")
        modules_layout = QVBoxLayout(modules_box)
        modules_layout.setContentsMargins(0, 4, 0, 4)
        modules_layout.setSpacing(0)

        self.mod_lessons = AccordionCard("Conteúdos e aulas", icon_prefix="📄", standalone=False)
        self.mod_materials = AccordionCard("Materiais de apoio", icon_prefix="⬇️", standalone=False)

        self.mod_materials.set_bullet_items([
            "Apostila completa em PDF",
            "Checklist prático e modelos editáveis",
            "Links recomendados pelo instrutor",
        ])

        for idx, mod in enumerate([self.mod_lessons, self.mod_materials]):
            modules_layout.addWidget(mod)
            if idx < 1:
                divider = QFrame()
                divider.setFixedHeight(1)
                divider.setStyleSheet("background-color: #F2E8EA;")
                modules_layout.addWidget(divider)

        cols.addLayout(left_col, 1)
        cols.addWidget(modules_box, 1, Qt.AlignTop)

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(inner, 1)
        center_row.addStretch()
        content_layout.addLayout(center_row)

        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def set_course_data(self, course: Course, lessons: List[Lesson], completed_ids: Set[int], progress_pct: int):
        self.hero_label.setPixmap(create_course_pixmap(course.art_key, 500, 310, radius=18))
        self.course_title_lbl.setText(course.name)

        lessons_container = QWidget()
        lessons_layout = QVBoxLayout(lessons_container)
        lessons_layout.setContentsMargins(12, 4, 4, 4)
        lessons_layout.setSpacing(10)

        for lesson in lessons:
            row = QHBoxLayout()
            row.setSpacing(10)

            cb = QCheckBox(f"{lesson.title} ({lesson.duration_minutes} min)")
            cb.setChecked(lesson.lesson_id in completed_ids)
            cb.toggled.connect(lambda checked, lid=lesson.lesson_id: self.lesson_toggled.emit(lid, checked))
            row.addWidget(cb, 1)

            if lesson.video_url:
                watch_btn = QPushButton("▶ Assistir")
                watch_btn.setObjectName("WatchBtn")
                watch_btn.setCursor(QCursor(Qt.PointingHandCursor))
                watch_btn.clicked.connect(lambda _=False, url=lesson.video_url: self.watch_lesson.emit(url))
                row.addWidget(watch_btn)

            lessons_layout.addLayout(row)

        self.mod_lessons.set_custom_widget(lessons_container)
        self.update_progress(progress_pct)

    def update_progress(self, pct: int):
        self.progress_bar.setValue(pct)
        self.progress_lbl.setText(f"{pct}% concluído")