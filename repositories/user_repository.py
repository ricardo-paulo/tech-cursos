import os
from typing import Optional

from config.database import get_supabase_client
from config.secure_session_storage import SecureSessionStorage
from models.user import User


class UserRepository:
    def __init__(self) -> None:
        self._client = get_supabase_client()
        self._session_storage = SecureSessionStorage(os.getenv("SUPABASE_URL", ""))

    def _require_client(self):
        if not self._client:
            raise RuntimeError(
                "Supabase não configurado. Defina SUPABASE_URL e SUPABASE_KEY no arquivo .env."
            )
        return self._client

    def sign_in(self, email: str, password: str) -> User:
        client = self._require_client()
        email_norm = email.strip().lower()
        resp = client.auth.sign_in_with_password(
            {"email": email_norm, "password": password}
        )
        if not resp.user or not resp.session:
            raise ValueError("E-mail ou senha inválidos.")

        self._save_refresh_token(resp.session.refresh_token)
        profile = self._fetch_profile(resp.user.id)
        return profile or User.from_auth_user(resp.user)

    def sign_up(
        self,
        name: str,
        email: str,
        password: str,
        role: str = "Aluno",
    ) -> User:
        client = self._require_client()
        email_norm = email.strip().lower()
        resp = client.auth.sign_up(
            {
                "email": email_norm,
                "password": password,
                "options": {
                    "data": {
                        "nome": name.strip(),
                        "tipo": role,
                    }
                },
            }
        )
        if not resp.user:
            raise ValueError("Não foi possível criar a conta.")
        if not resp.session:
            raise ValueError(
                "Conta criada! Confirme seu e-mail antes de fazer login."
            )

        self._save_refresh_token(resp.session.refresh_token)
        profile = self._fetch_profile(resp.user.id)
        return profile or User.from_auth_user(resp.user)

    def restore_session(self) -> Optional[User]:
        client = self._require_client()
        refresh_token = self._session_storage.load_refresh_token()
        if not refresh_token:
            return None

        response = client.auth.refresh_session(refresh_token)
        if not response.user or not response.session:
            self._session_storage.clear()
            return None

        self._session_storage.save_refresh_token(response.session.refresh_token)
        profile = self._fetch_profile(response.user.id)
        return profile or User.from_auth_user(response.user)

    def sign_out(self) -> None:
        try:
            if self._client:
                self._client.auth.sign_out({"scope": "local"})
        finally:
            self._session_storage.clear()

    def _save_refresh_token(self, refresh_token: str) -> None:
        try:
            self._session_storage.save_refresh_token(refresh_token)
        except Exception as storage_error:
            cleanup_errors = []
            try:
                self._session_storage.clear()
            except Exception as clear_error:
                cleanup_errors.append(str(clear_error))
            if self._client:
                try:
                    self._client.auth.sign_out({"scope": "local"})
                except Exception as sign_out_error:
                    cleanup_errors.append(str(sign_out_error))
            if cleanup_errors:
                raise RuntimeError(
                    "Não foi possível salvar a sessão com segurança. "
                    "A limpeza local também apresentou erro: "
                    + "; ".join(cleanup_errors)
                ) from storage_error
            raise RuntimeError(
                "Não foi possível salvar a sessão no cofre seguro do sistema."
            ) from storage_error

    def _fetch_profile(self, user_id: str) -> Optional[User]:
        if not self._client:
            return None
        try:
            resp = (
                self._client.table("usuario")
                .select("*")
                .eq("id_usuario", user_id)
                .limit(1)
                .execute()
            )
            if resp.data:
                return User.from_dict(resp.data[0])
        except Exception as exc:
            print(f"[UserRepository] Erro Supabase em _fetch_profile: {exc}")
        return None