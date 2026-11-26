from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from resources.icons.vector_assets import TechLogoIcon


class LoginView(QWidget):
    login_submitted = Signal(str, str)
    register_submitted = Signal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("RootPage")
        self._register_mode = False

        outer = QVBoxLayout(self)
        outer.setContentsMargins(32, 32, 32, 32)
        outer.addStretch()

        card = QFrame()
        card.setObjectName("LoginCard")
        card.setFixedWidth(440)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 36, 36, 34)
        card_layout.setSpacing(14)

        brand_row = QHBoxLayout()
        brand_row.setAlignment(Qt.AlignCenter)
        brand_row.setSpacing(10)
        brand_row.addWidget(TechLogoIcon())

        brand_texts = QVBoxLayout()
        brand_texts.setSpacing(0)
        brand_title = QLabel("Tech Cursos")
        brand_title.setStyleSheet("font-size: 22px; font-weight: 800; color: #6155F5;")
        brand_sub = QLabel("Cursos de informática")
        brand_sub.setStyleSheet("font-size: 12px; color: #6155F5;")
        brand_texts.addWidget(brand_title)
        brand_texts.addWidget(brand_sub)
        brand_row.addLayout(brand_texts)
        card_layout.addLayout(brand_row)

        self.heading_lbl = QLabel("Acesse sua conta")
        self.heading_lbl.setAlignment(Qt.AlignCenter)
        self.heading_lbl.setStyleSheet("font-size: 20px; font-weight: 800; color: #18181B; margin-top: 6px;")
        card_layout.addWidget(self.heading_lbl)

        self.name_input = QLineEdit()
        self.name_input.setObjectName("FormInput")
        self.name_input.setPlaceholderText("Nome completo")
        self.name_input.setVisible(False)
        card_layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setObjectName("FormInput")
        self.email_input.setPlaceholderText("E-mail")
        card_layout.addWidget(self.email_input)

        self.pass_input = QLineEdit()
        self.pass_input.setObjectName("FormInput")
        self.pass_input.setPlaceholderText("Senha")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.returnPressed.connect(self._handle_submit)
        card_layout.addWidget(self.pass_input)

        self.feedback_lbl = QLabel("")
        self.feedback_lbl.setWordWrap(True)
        self.feedback_lbl.setAlignment(Qt.AlignCenter)
        self.feedback_lbl.setStyleSheet("font-size: 12px; font-weight: 600; color: #B80D57;")
        card_layout.addWidget(self.feedback_lbl)

        self.submit_btn = QPushButton("ENTRAR")
        self.submit_btn.setObjectName("PrimaryBtn")
        self.submit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.submit_btn.setMinimumHeight(46)
        self.submit_btn.clicked.connect(self._handle_submit)
        card_layout.addWidget(self.submit_btn)

        self.toggle_btn = QPushButton("Criar nova conta")
        self.toggle_btn.setObjectName("SecondaryBtn")
        self.toggle_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.toggle_btn.setMinimumHeight(42)
        self.toggle_btn.clicked.connect(self._toggle_mode)
        card_layout.addWidget(self.toggle_btn)

        center_row = QHBoxLayout()
        center_row.addStretch()
        center_row.addWidget(card)
        center_row.addStretch()
        outer.addLayout(center_row)
        outer.addStretch()

    def _toggle_mode(self):
        self._register_mode = not self._register_mode
        self.name_input.setVisible(self._register_mode)
        self.feedback_lbl.setText("")
        if self._register_mode:
            self.heading_lbl.setText("Crie sua conta")
            self.submit_btn.setText("CADASTRAR")
            self.toggle_btn.setText("Já tenho conta")
            self.email_input.clear()
            self.pass_input.clear()
        else:
            self.heading_lbl.setText("Acesse sua conta")
            self.submit_btn.setText("ENTRAR")
            self.toggle_btn.setText("Criar nova conta")
            self.email_input.clear()
            self.pass_input.clear()

    def reset_fields(self):
        self.name_input.clear()
        self.email_input.clear()
        self.pass_input.clear()
        self.feedback_lbl.setText("")

    def _handle_submit(self):
        self.feedback_lbl.setText("")
        email = self.email_input.text().strip()
        password = self.pass_input.text()
        if self._register_mode:
            self.register_submitted.emit(self.name_input.text().strip(), email, password)
        else:
            self.login_submitted.emit(email, password)

    def show_error(self, message: str):
        self.feedback_lbl.setText(message)