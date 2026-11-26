from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class User:
    user_id: Optional[str]
    name: str
    email: str
    role: str = "Aluno"  # "Aluno" ou "Admin"
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        return cls(
            user_id=data.get("id_usuario"),
            name=data.get("nome", ""),
            email=data.get("email", ""),
            role=data.get("tipo", "Aluno"),
            created_at=data.get("data_cadastro"),
        )

    @classmethod
    def from_auth_user(cls, auth_user: Any) -> User:
        meta = getattr(auth_user, "user_metadata", None) or {}
        email = getattr(auth_user, "email", None) or ""
        name = meta.get("nome") or meta.get("name") or (email.split("@")[0] if email else "")
        return cls(
            user_id=getattr(auth_user, "id", None),
            name=name,
            email=email,
            role=meta.get("tipo", "Aluno"),
            created_at=getattr(auth_user, "created_at", None),
        )