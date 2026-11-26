from PySide6.QtCore import QObject, Signal

from services.user_service import UserService
from views.login.login_view import LoginView


class LoginController(QObject):
    authenticated = Signal(object)

    def __init__(self, view: LoginView, user_service: UserService) -> None:
        super().__init__()
        self.view = view
        self.user_service = user_service

        self.view.login_submitted.connect(self.handle_login)
        self.view.register_submitted.connect(self.handle_register)

    def handle_login(self, email: str, password: str) -> None:
        try:
            user = self.user_service.authenticate(email, password)
        except Exception as err:
            self.view.show_error(self._format_auth_error(err))
            return
        self.authenticated.emit(user)

    def handle_register(self, name: str, email: str, password: str) -> None:
        try:
            user = self.user_service.register(name=name, email=email, password=password)
        except Exception as err:
            self.view.show_error(self._format_auth_error(err))
            return
        self.authenticated.emit(user)

    def restore_session(self) -> None:
        try:
            user = self.user_service.restore_session()
        except Exception as err:
            self.view.show_error(
                "Não foi possível validar a sessão salva. Faça login novamente. "
                + self._format_auth_error(err)
            )
            return
        if user:
            self.authenticated.emit(user)

    def logout(self) -> None:
        try:
            self.user_service.logout()
        except Exception as err:
            self.view.show_error(
                "A sessão local foi encerrada, mas houve um erro ao concluir a saída: "
                + self._format_auth_error(err)
            )
        finally:
            self.view.reset_fields()

    @staticmethod
    def _format_auth_error(err: Exception) -> str:
        msg = str(err)
        low = msg.lower()
        if "invalid login credentials" in low:
            return "E-mail ou senha inválidos."
        if "email not confirmed" in low:
            return "Confirme seu e-mail antes de fazer login."
        if "user already registered" in low:
            return "Já existe uma conta cadastrada com este e-mail."
        if "password should be at least" in low:
            return "A senha deve ter pelo menos 6 caracteres."
        if "unable to validate email address" in low or "invalid email" in low:
            return "Informe um endereço de e-mail válido."
        return msg