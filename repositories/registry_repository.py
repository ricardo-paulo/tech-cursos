from datetime import datetime
from typing import Dict, List, Optional, Tuple

from config.database import get_supabase_client
from models.registry import Enrollment, Progress


class RegistryRepository:
    def __init__(self) -> None:
        self._client = get_supabase_client()
        self._local_enrollments: List[Enrollment] = []
        self._local_progress: Dict[Tuple[int, int], Progress] = {}
        self._next_enrollment_id = 1
        self._next_progress_id = 1

    def find_enrollment(self, user_id: str, course_id: int) -> Optional[Enrollment]:
        if self._client:
            try:
                resp = (
                    self._client.table("matricula")
                    .select("*")
                    .eq("id_usuario", user_id)
                    .eq("id_curso", course_id)
                    .limit(1)
                    .execute()
                )
                if resp.data:
                    return Enrollment.from_dict(resp.data[0])
                return None
            except Exception as exc:
                print(f"[RegistryRepository] Erro Supabase em find_matricula: {exc}")

        for enrollment in self._local_enrollments:
            if enrollment.user_id == user_id and enrollment.course_id == course_id:
                return enrollment
        return None

    def list_enrollments_by_user(self, user_id: str) -> List[Enrollment]:
        if self._client:
            try:
                resp = (
                    self._client.table("matricula")
                    .select("*")
                    .eq("id_usuario", user_id)
                    .execute()
                )
                if resp.data is not None:
                    return [Enrollment.from_dict(row) for row in resp.data]
            except Exception as exc:
                print(f"[RegistryRepository] Erro Supabase em list_matriculas_by_user: {exc}")

        return [e for e in self._local_enrollments if e.user_id == user_id]

    def create_enrollment(
        self,
        user_id: str,
        course_id: int,
        course_class: str = "",
        payment_method: str = "",
        status: str = "Ativa",
    ) -> Enrollment:
        existing = self.find_enrollment(user_id, course_id)
        if existing:
            if (course_class or payment_method) and existing.enrollment_id is not None:
                update_payload: Dict[str, str] = {}
                if course_class:
                    update_payload["turma"] = course_class
                    existing.course_class = course_class
                if payment_method:
                    update_payload["forma_pagamento"] = payment_method
                    existing.payment_method = payment_method
                if self._client and update_payload:
                    try:
                        resp = (
                            self._client.table("matricula")
                            .update(update_payload)
                            .eq("id_matricula", existing.enrollment_id)
                            .execute()
                        )
                        if resp.data:
                            return Enrollment.from_dict(resp.data[0])
                    except Exception as exc:
                        print(f"[RegistryRepository] Erro Supabase em update_matricula: {exc}")
            return existing

        now = datetime.now()
        if self._client:
            try:
                payload = {
                    "id_usuario": user_id,
                    "id_curso": course_id,
                    "turma": course_class,
                    "forma_pagamento": payment_method,
                    "data_matricula": now.isoformat(),
                    "status": status,
                }
                resp = self._client.table("matricula").insert(payload).execute()
                if resp.data:
                    return Enrollment.from_dict(resp.data[0])
            except Exception as exc:
                print(f"[RegistryRepository] Erro Supabase em create_matricula: {exc}")

        enrollment = Enrollment(
            enrollment_id=self._next_enrollment_id,
            user_id=user_id,
            course_id=course_id,
            course_class=course_class,
            payment_method=payment_method,
            enrollment_date=now,
            status=status,
        )
        self._next_enrollment_id += 1
        self._local_enrollments.append(enrollment)
        return enrollment

    def list_progress(self, enrollment_id: int) -> List[Progress]:
        if self._client:
            try:
                resp = (
                    self._client.table("progresso")
                    .select("*")
                    .eq("id_matricula", enrollment_id)
                    .execute()
                )
                if resp.data is not None:
                    return [Progress.from_dict(row) for row in resp.data]
            except Exception as exc:
                print(f"[RegistryRepository] Erro Supabase em list_progresso: {exc}")

        return [
            p for (eid, _), p in self._local_progress.items()
            if eid == enrollment_id
        ]

    def set_lesson_completed(self, enrollment_id: int, lesson_id: int, completed: bool) -> Progress:
        now = datetime.now() if completed else None

        if self._client:
            try:
                existing = (
                    self._client.table("progresso")
                    .select("*")
                    .eq("id_matricula", enrollment_id)
                    .eq("id_aula", lesson_id)
                    .limit(1)
                    .execute()
                )
                payload = {
                    "concluida": completed,
                    "data_conclusao": now.isoformat() if now else None,
                }
                if existing.data:
                    pid = existing.data[0]["id_progresso"]
                    resp = (
                        self._client.table("progresso")
                        .update(payload)
                        .eq("id_progresso", pid)
                        .execute()
                    )
                    if resp.data:
                        return Progress.from_dict(resp.data[0])
                else:
                    payload["id_matricula"] = enrollment_id
                    payload["id_aula"] = lesson_id
                    resp = self._client.table("progresso").insert(payload).execute()
                    if resp.data:
                        return Progress.from_dict(resp.data[0])
            except Exception as exc:
                print(f"[RegistryRepository] Erro Supabase em set_aula_concluida: {exc}")

        key = (enrollment_id, lesson_id)
        if key in self._local_progress:
            prog = self._local_progress[key]
            prog.completed = completed
            prog.completion_date = now
            return prog

        prog = Progress(
            progress_id=self._next_progress_id,
            enrollment_id=enrollment_id,
            lesson_id=lesson_id,
            completed=completed,
            completion_date=now,
        )
        self._next_progress_id += 1
        self._local_progress[key] = prog
        return prog