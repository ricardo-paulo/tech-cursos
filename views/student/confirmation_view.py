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

from models.class_model import CourseClass
from models.course import Course
from resources.icons.vector_assets import CheckmarkBadge


class ConfirmationView(QWidget):
    go_course_access = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RootPage")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(32, 32, 32, 32)
        outer.addStretch()

        card = QFrame()
        card.setObjectName("ConfirmCard")
        card.setMaximumWidth(840)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(42, 40, 42, 38)
        card_layout.setSpacing(30)

        top_cols = QHBoxLayout()
        top_cols.setSpacing(36)

        left_col = QVBoxLayout()
        left_col.setAlignment(Qt.AlignCenter)
        left_col.setSpacing(8)

        badge_wrap = QHBoxLayout()
        badge_wrap.setAlignment(Qt.AlignCenter)
        badge_wrap.addWidget(CheckmarkBadge())
        left_col.addLayout(badge_wrap)
        left_col.addSpacing(8)

        heading = QLabel("Compra realizada com\nsucesso!")
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("font-size: 25px; font-weight: 800; color: #18181B;")

        sub1 = QLabel("Sua matrícula no curso")
        sub1.setAlignment(Qt.AlignCenter)
        sub1.setStyleSheet("font-size: 15px; color: #374151; margin-top: 6px;")

        self.course_name_lbl = QLabel()
        self.course_name_lbl.setAlignment(Qt.AlignCenter)
        self.course_name_lbl.setWordWrap(True)
        self.course_name_lbl.setStyleSheet(
            'font-family: Georgia, "Times New Roman", serif; '
            "font-size: 19px; font-weight: 700; color: #0038FF;"
        )

        sub2 = QLabel("foi confirmada")
        sub2.setAlignment(Qt.AlignCenter)
        sub2.setStyleSheet("font-size: 15px; color: #374151;")

        left_col.addWidget(heading)
        left_col.addWidget(sub1)
        left_col.addWidget(self.course_name_lbl)
        left_col.addWidget(sub2)

        details_box = QFrame()
        details_box.setObjectName("SoftSummaryBox")
        details_layout = QVBoxLayout(details_box)
        details_layout.setContentsMargins(24, 24, 24, 24)
        details_layout.setSpacing(15)

        self.lbl_course_class = QLabel()
        self.lbl_start = QLabel()
        self.lbl_schedule = QLabel()
        self.lbl_format = QLabel("🖥️   <b>Formato:</b> online")

        for lbl in (self.lbl_course_class, self.lbl_start, self.lbl_schedule, self.lbl_format):
            lbl.setWordWrap(True)
            lbl.setStyleSheet("font-size: 14px; color: #1F2937;")
            details_layout.addWidget(lbl)

        top_cols.addLayout(left_col, 1)
        top_cols.addWidget(details_box, 1)
        card_layout.addLayout(top_cols)

        actions = QHBoxLayout()
        actions.setSpacing(24)

        btn_access = QPushButton("Acessar o curso")
        btn_access.setObjectName("PrimaryBtn")
        btn_access.setCursor(QCursor(Qt.PointingHandCursor))
        btn_access.setMinimumHeight(48)
        btn_access.clicked.connect(self.go_course_access.emit)

        btn_my_courses = QPushButton("Ver meus cursos")
        btn_my_courses.setObjectName("SecondaryBtn")
        btn_my_courses.setCursor(QCursor(Qt.PointingHandCursor))
        btn_my_courses.setMinimumHeight(48)
        btn_my_courses.clicked.connect(self.go_course_access.emit)

        actions.addWidget(btn_access, 1)
        actions.addWidget(btn_my_courses, 1)
        card_layout.addLayout(actions)

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(card, 1)
        center_row.addStretch()
        outer.addLayout(center_row)
        outer.addStretch()

    def set_confirmation_data(self, course: Course, course_class: CourseClass):
        self.course_name_lbl.setText(course.name)
        self.lbl_course_class.setText(f"📅   <b>Turma:</b> {course_class.code}")
        self.lbl_start.setText(f"📅   <b>Início:</b> {course_class.start_date}")
        self.lbl_schedule.setText(f"🕒   <b>Horário:</b> {course_class.full_schedule}")