import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from controllers.course_controller import CourseController
from controllers.login_controller import LoginController
from controllers.student_controller import StudentController
from models.user import User
from repositories.course_repository import CourseRepository
from repositories.registry_repository import RegistryRepository
from repositories.user_repository import UserRepository
from services.course_service import CourseService
from services.registry_service import RegistryService
from services.user_service import UserService
from views.courses.checkout_view import CheckoutView
from views.courses.course_details_view import CourseDetailsView
from views.home.home_view import HomeView
from views.login.login_view import LoginView
from views.student.confirmation_view import ConfirmationView
from views.student.course_access_view import CourseAccessView


class TechCursosWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tech Cursos — Plataforma de Informática")
        self.resize(1240, 800)
        self.setMinimumSize(980, 660)

        # 1. Repositórios
        user_repo = UserRepository()
        course_repo = CourseRepository()
        registry_repo = RegistryRepository()

        # 2. Serviços
        user_service = UserService(user_repo)
        course_service = CourseService(course_repo)
        registry_service = RegistryService(registry_repo)

        # 3. Views
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_view = LoginView()
        self.home_view = HomeView()
        self.details_view = CourseDetailsView()
        self.checkout_view = CheckoutView()
        self.confirmation_view = ConfirmationView()
        self.access_view = CourseAccessView()

        for view in (
            self.login_view,
            self.home_view,
            self.details_view,
            self.checkout_view,
            self.confirmation_view,
            self.access_view,
        ):
            self.stack.addWidget(view)

        # 4. Controllers
        self.login_controller = LoginController(self.login_view, user_service)
        self.course_controller = CourseController(
            home_view=self.home_view,
            details_view=self.details_view,
            checkout_view=self.checkout_view,
            course_service=course_service,
        )
        self.student_controller = StudentController(
            confirmation_view=self.confirmation_view,
            access_view=self.access_view,
            course_service=course_service,
            registry_service=registry_service,
        )

        # 5. Roteamento entre Controllers e Telas
        self.login_controller.authenticated.connect(self._on_user_authenticated)

        self.course_controller.open_home_requested.connect(lambda: self.stack.setCurrentWidget(self.home_view))
        self.course_controller.open_details_requested.connect(lambda: self.stack.setCurrentWidget(self.details_view))
        self.course_controller.open_checkout_requested.connect(lambda: self.stack.setCurrentWidget(self.checkout_view))
        self.course_controller.purchase_finalized.connect(self.student_controller.confirm_enrollment)
        self.course_controller.open_my_courses_requested.connect(self.student_controller.open_active_course)
        self.course_controller.logout_requested.connect(self._on_logout)

        self.student_controller.open_confirmation_requested.connect(
            lambda: self.stack.setCurrentWidget(self.confirmation_view)
        )
        self.student_controller.open_access_requested.connect(
            lambda: self.stack.setCurrentWidget(self.access_view)
        )
        self.student_controller.open_home_requested.connect(
            lambda: self.stack.setCurrentWidget(self.home_view)
        )

        self.stack.setCurrentWidget(self.login_view)
        self.login_controller.restore_session()

    def _on_user_authenticated(self, user: User) -> None:
        if not user.user_id:
            self.login_view.show_error("Não foi possível validar a identidade da conta.")
            self.login_controller.logout()
            return
        self.student_controller.set_current_user(user)
        self.course_controller.set_current_user(user.user_id)
        self.course_controller.load_home()
        self.stack.setCurrentWidget(self.home_view)

    def _on_logout(self) -> None:
        self.login_controller.logout()
        self.student_controller.reset_session()
        self.course_controller.set_current_user(None)
        self.stack.setCurrentWidget(self.login_view)


def load_stylesheet() -> str:
    qss_path = Path(__file__).resolve().parent / "resources" / "styles" / "style.qss"
    return qss_path.read_text(encoding="utf-8") if qss_path.exists() else ""


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())

    window = TechCursosWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()