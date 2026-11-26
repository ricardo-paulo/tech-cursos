from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Lesson:
    lesson_id: int
    course_id: int
    title: str
    description: str
    order: int
    duration_minutes: int
    # Link de vídeo não listado no YouTube (opcional no banco)
    video_url: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> Lesson:
        return cls(
            lesson_id=int(data["id_aula"]),
            course_id=int(data["id_curso"]),
            title=data.get("titulo", ""),
            description=data.get("descricao", ""),
            order=int(data.get("ordem", 1)),
            duration_minutes=int(data.get("duracao_minutos", 0)),
            video_url=data.get("video_url", ""),
        )


@dataclass
class CourseClass:
    code: str
    title: str
    short_schedule: str
    start_date: str
    full_schedule: str