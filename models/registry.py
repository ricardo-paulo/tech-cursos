from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Enrollment:
    enrollment_id: Optional[int]
    user_id: str
    course_id: int
    course_class: str = ""
    payment_method: str = ""
    enrollment_date: Optional[datetime] = None
    status: str = "Ativa"

    @classmethod
    def from_dict(cls, data: dict) -> Enrollment:
        return cls(
            enrollment_id=data.get("id_matricula"),
            user_id=str(data["id_usuario"]),
            course_id=int(data["id_curso"]),
            course_class=data.get("turma") or "",
            payment_method=data.get("forma_pagamento") or "",
            enrollment_date=data.get("data_matricula"),
            status=data.get("status", "Ativa"),
        )


@dataclass
class Progress:
    progress_id: Optional[int]
    enrollment_id: int
    lesson_id: int
    completed: bool = False
    completion_date: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict) -> Progress:
        return cls(
            progress_id=data.get("id_progresso"),
            enrollment_id=int(data["id_matricula"]),
            lesson_id=int(data["id_aula"]),
            completed=bool(data.get("concluida", False)),
            completion_date=data.get("data_conclusao"),
        )