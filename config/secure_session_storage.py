import hashlib

import keyring
from keyring.errors import PasswordDeleteError


class SecureSessionStorage:
    _SERVICE_NAME = "tech-cursos.supabase"
    _SECURE_BACKEND_MODULES = (
        "keyring.backends.Windows",
        "keyring.backends.SecretService",
        "keyring.backends.kwallet",
    )

    def __init__(self, project_url: str) -> None:
        self._account_name = hashlib.sha256(project_url.strip().lower().encode("utf-8")).hexdigest()

    @classmethod
    def _require_secure_backend(cls):
        backend = keyring.get_keyring()
        module = type(backend).__module__
        if not any(module.startswith(prefix) for prefix in cls._SECURE_BACKEND_MODULES):
            raise RuntimeError(
                "O armazenamento seguro do sistema não está disponível. "
                "Configure o Gerenciador de Credenciais do Windows ou um cofre "
                "Secret Service/KWallet no Linux."
            )
        return keyring

    def load_refresh_token(self) -> str | None:
        secure_store = self._require_secure_backend()
        return secure_store.get_password(self._SERVICE_NAME, self._account_name)

    def save_refresh_token(self, refresh_token: str) -> None:
        if not refresh_token:
            raise ValueError("Não foi possível salvar uma sessão sem refresh token.")
        secure_store = self._require_secure_backend()
        secure_store.set_password(self._SERVICE_NAME, self._account_name, refresh_token)

    def clear(self) -> None:
        secure_store = self._require_secure_backend()
        try:
            secure_store.delete_password(self._SERVICE_NAME, self._account_name)
        except PasswordDeleteError:
            pass
