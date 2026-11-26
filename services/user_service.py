from typing import Optional

from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    def authenticate(self, email: str, password: str) -> User:
        if not email.strip() or not password:
            raise ValueError("Preencha e-mail e senha.")
        return self._repo.sign_in(email=email, password=password)

    def register(self, name: str, email: str, password: str, role: str = "Aluno") -> User:
        if not name.strip() or not email.strip() or len(password) < 6:
            raise ValueError("Preencha nome, e-mail válido e senha com pelo menos 6 caracteres.")
        return self._repo.sign_up(name=name, email=email, password=password, role=role)

    def logout(self) -> None:
        self._repo.sign_out()

    def restore_session(self) -> Optional[User]:
        return self._repo.restore_session()