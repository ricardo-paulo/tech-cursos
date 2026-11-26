from typing import List

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from models.course import Course
from resources.icons.vector_assets import AvatarWidget, TechLogoIcon
from views.widgets import ClickableCourseCard, make_nav_pill


class HomeView(QWidget):
    search_changed = Signal(str, bool)
    course_selected = Signal(object)
    go_my_courses = Signal()
    logout_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RootPage")
        self._only_under_100 = False

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        topbar = QFrame()
        topbar.setObjectName("TopBar")
        topbar.setFixedHeight(74)
        top_layout = QHBoxLayout(topbar)
        top_layout.setContentsMargins(32, 0, 32, 0)

        brand_wrap = QHBoxLayout()
        brand_wrap.setSpacing(10)
        brand_wrap.addWidget(TechLogoIcon())
        brand_texts = QVBoxLayout()
        brand_texts.setSpacing(0)
        brand_title = QLabel("Tech Cursos")
        brand_title.setStyleSheet("font-size: 20px; font-weight: 800; color: #6155F5;")
        # brand_sub = QLabel("Cursos de informática")
        # brand_sub.setStyleSheet("font-size: 12px; color: #6155F5;")
        brand_texts.addWidget(brand_title)
        # brand_texts.addWidget(brand_sub)
        brand_wrap.addLayout(brand_texts)
        top_layout.addLayout(brand_wrap)
        top_layout.addStretch()

        nav_home = make_nav_pill("🏠  Início", active=True)
        nav_explore = make_nav_pill("🔍  Explorar")
        nav_explore.clicked.connect(lambda: self.search_input.setFocus())

        agenda_wrap = QWidget()
        agenda_layout = QHBoxLayout(agenda_wrap)
        agenda_layout.setContentsMargins(0, 0, 0, 0)
        agenda_layout.setSpacing(0)
        nav_agenda = make_nav_pill("📅  Agenda")
        nav_agenda.setStyleSheet("padding-right: 0px;")
        nav_agenda.clicked.connect(self.go_my_courses.emit)
        self.badge_lbl = QLabel("1")
        self.badge_lbl.setAlignment(Qt.AlignCenter)
        self.badge_lbl.setFixedSize(18, 18)
        self.badge_lbl.setStyleSheet(
            "background-color: #B80D57; color: #FFFFFF; font-size: 10px; "
            "font-weight: 700; border-radius: 9px;"
        )
        agenda_layout.addWidget(nav_agenda)
        agenda_layout.addWidget(self.badge_lbl, 0, Qt.AlignTop)

        nav_profile = make_nav_pill("👤  Sair")
        nav_profile.clicked.connect(self.logout_requested.emit)

        top_layout.addWidget(nav_home)
        top_layout.addWidget(nav_explore)
        top_layout.addWidget(agenda_wrap)
        top_layout.addWidget(nav_profile)
        top_layout.addStretch()

        avatar = AvatarWidget()
        avatar.clicked.connect(self.go_my_courses.emit)
        top_layout.addWidget(avatar)
        root.addWidget(topbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_content.setObjectName("ScrollContent")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(40, 28, 40, 48)
        scroll_layout.setAlignment(Qt.AlignTop)

        inner = QWidget()
        inner.setMaximumWidth(1120)
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(26)

        search_bar = QFrame()
        search_bar.setObjectName("SearchBar")
        search_bar.setFixedHeight(52)
        search_layout = QHBoxLayout(search_bar)
        search_layout.setContentsMargins(18, 0, 10, 0)
        search_layout.setSpacing(10)

        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("color: #B80D57; font-size: 16px;")
        self.search_input = QLineEdit()
        self.search_input.setObjectName("SearchInput")
        self.search_input.setPlaceholderText("Buscar cursos...")
        self.search_input.textChanged.connect(self._emit_search)

        self.filter_btn = QPushButton("☰")
        self.filter_btn.setObjectName("FilterBtn")
        self.filter_btn.setToolTip("Filtrar cursos até R$ 100,00")
        self.filter_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.filter_btn.clicked.connect(self._toggle_filter)

        search_layout.addWidget(search_icon)
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(self.filter_btn)
        inner_layout.addWidget(search_bar)

        title_row = QHBoxLayout()
        heading = QLabel("Cursos em Destaque")
        heading.setStyleSheet("font-size: 26px; font-weight: 800; color: #18181B;")
        self.filter_hint = QLabel("")
        self.filter_hint.setStyleSheet("font-size: 13px; font-weight: 600; color: #B80D57;")
        title_row.addWidget(heading)
        title_row.addStretch()
        title_row.addWidget(self.filter_hint)
        inner_layout.addLayout(title_row)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setHorizontalSpacing(22)
        self.grid_layout.setVerticalSpacing(22)
        inner_layout.addWidget(self.grid_widget)

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(inner, 1)
        center_row.addStretch()
        scroll_layout.addLayout(center_row)

        scroll.setWidget(scroll_content)
        root.addWidget(scroll, 1)

    def _toggle_filter(self):
        self._only_under_100 = not self._only_under_100
        self.filter_btn.setProperty("active", self._only_under_100)
        self.filter_btn.style().unpolish(self.filter_btn)
        self.filter_btn.style().polish(self.filter_btn)
        self.filter_hint.setText("Filtro ativo: até R$ 100,00" if self._only_under_100 else "")
        self._emit_search()

    def _emit_search(self):
        self.search_changed.emit(self.search_input.text(), self._only_under_100)

    def display_courses(self, courses: List[Course]):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not courses:
            empty = QLabel("Nenhum curso encontrado para a busca atual.")
            empty.setStyleSheet("font-size: 15px; color: #6B7280; padding: 20px;")
            self.grid_layout.addWidget(empty, 0, 0)
            return

        for idx, course in enumerate(courses):
            card = ClickableCourseCard(course)
            card.clicked.connect(self.course_selected.emit)
            self.grid_layout.addWidget(card, idx // 2, idx % 2)