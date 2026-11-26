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

from models.class_model import CourseClass
from models.course import Course
from resources.icons.vector_assets import create_course_pixmap
from views.widgets import SelectableCard


class CheckoutView(QWidget):
    go_back = Signal()
    course_class_selected = Signal(object)
    payment_selected = Signal(str)
    purchase_completed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RootPage")
        self._course_class_cards: List[SelectableCard] = []
        self._payment_cards: List[SelectableCard] = []

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

        page_title = QLabel("ESCOLHER TURMA")
        page_title.setStyleSheet("font-size: 16px; font-weight: 800; letter-spacing: 0.6px; color: #18181B;")

        top_layout.addWidget(back_btn)
        top_layout.addSpacing(8)
        top_layout.addWidget(page_title)
        top_layout.addStretch()
        root.addWidget(topbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setObjectName("ScrollContent")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 32, 40, 48)
        content_layout.setAlignment(Qt.AlignTop)

        shell = QFrame()
        shell.setObjectName("CheckoutShell")
        shell.setMaximumWidth(1100)
        shell_layout = QHBoxLayout(shell)
        shell_layout.setContentsMargins(36, 34, 36, 34)
        shell_layout.setSpacing(42)
        shell_layout.setAlignment(Qt.AlignTop)

        left_col = QVBoxLayout()
        left_col.setSpacing(14)

        lbl_course_class = QLabel("Selecione a turma")
        lbl_course_class.setStyleSheet("font-size: 21px; font-weight: 800; color: #18181B;")
        left_col.addWidget(lbl_course_class)

        self._course_classes_layout = QVBoxLayout()
        self._course_classes_layout.setSpacing(12)
        left_col.addLayout(self._course_classes_layout)

        left_col.addSpacing(14)

        lbl_pay = QLabel("Formas de pagamento")
        lbl_pay.setStyleSheet("font-size: 21px; font-weight: 800; color: #18181B;")
        left_col.addWidget(lbl_pay)

        payments = [
            ("💳", "Cartão de crédito", "#18181B"),
            ("❖", "Pix", "#00B5AD"),
            ("||||", "Boleto", "#18181B"),
        ]
        for icon, name, color in payments:
            card = SelectableCard(icon_text=icon, title=name, value=name, icon_color=color)
            card.clicked.connect(self._on_payment_clicked)
            self._payment_cards.append(card)
            left_col.addWidget(card)

        left_col.addStretch()

        summary_box = QFrame()
        summary_box.setObjectName("SoftSummaryBox")
        summary_box.setFixedWidth(360)
        summary_layout = QVBoxLayout(summary_box)
        summary_layout.setContentsMargins(22, 22, 22, 24)
        summary_layout.setSpacing(14)

        self.summary_art = QLabel()
        self.summary_art.setFixedSize(316, 196)
        summary_layout.addWidget(self.summary_art)

        self.summary_title = QLabel()
        self.summary_title.setWordWrap(True)
        self.summary_title.setStyleSheet("font-size: 18px; font-weight: 800; color: #18181B; margin-top: 6px;")

        self.summary_price = QLabel()
        self.summary_price.setStyleSheet("font-size: 20px; font-weight: 800; color: #0080FF;")

        finish_btn = QPushButton("FINALIZAR COMPRA")
        finish_btn.setObjectName("PrimaryBtn")
        finish_btn.setCursor(QCursor(Qt.PointingHandCursor))
        finish_btn.setMinimumHeight(48)
        finish_btn.clicked.connect(self.purchase_completed.emit)

        summary_layout.addWidget(self.summary_title)
        summary_layout.addWidget(self.summary_price)
        summary_layout.addSpacing(8)
        summary_layout.addWidget(finish_btn)

        shell_layout.addLayout(left_col, 1)
        shell_layout.addWidget(summary_box, 0, Qt.AlignTop)

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(shell, 1)
        center_row.addStretch()
        content_layout.addLayout(center_row)

        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def set_checkout_data(self, course: Course, course_classes: List[CourseClass], selected_course_class: CourseClass, payment_method: str):
        self.summary_art.setPixmap(create_course_pixmap(course.art_key, 316, 196, radius=14))
        self.summary_title.setText(course.name.upper())
        self.summary_price.setText(course.formatted_price)

        while self._course_classes_layout.count():
            child = self._course_classes_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self._course_class_cards.clear()

        for idx, course_class in enumerate(course_classes):
            card = SelectableCard(
                icon_text="📅",
                title=course_class.title,
                subtitle=course_class.short_schedule,
                value=course_class,
                icon_color="#E879A8" if idx == 0 else "#18181B",
            )
            card.set_selected(course_class.code == selected_course_class.code)
            card.clicked.connect(self._on_course_class_clicked)
            self._course_class_cards.append(card)
            self._course_classes_layout.addWidget(card)

        for card in self._payment_cards:
            card.set_selected(card.value == payment_method)

    def _on_course_class_clicked(self, clicked_card: SelectableCard):
        for card in self._course_class_cards:
            card.set_selected(card is clicked_card)
        self.course_class_selected.emit(clicked_card.value)

    def _on_payment_clicked(self, clicked_card: SelectableCard):
        for card in self._payment_cards:
            card.set_selected(card is clicked_card)
        self.payment_selected.emit(clicked_card.value)