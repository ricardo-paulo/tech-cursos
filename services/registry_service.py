from typing import List, Set

from models.registry import Enrollment
from repositories.registry_repository import RegistryRepository


class RegistryService:
    def __init__(self, registry_repo: RegistryRepository) -> None:
        self._repo = registry_repo

    def enroll_student(
        self,
        user_id: str,
        course_id: int,
        course_class: str = "",
        payment_method: str = "",
    ) -> Enrollment:
        return self._repo.create_enrollment(
            user_id=user_id,
            course_id=course_id,
            course_class=course_class,
            payment_method=payment_method,
            status="Ativa",
        )

    def get_student_enrollments(self, user_id: str) -> List[Enrollment]:
        return self._repo.list_enrollments_by_user(user_id)

    def get_completed_lesson_ids(self, enrollment_id: int) -> Set[int]:
        items = self._repo.list_progress(enrollment_id)
        return {item.lesson_id for item in items if item.completed}

    def set_lesson_completed(self, enrollment_id: int, lesson_id: int, completed: bool) -> None:
        self._repo.set_lesson_completed(enrollment_id, lesson_id, completed)

    def calculate_progress_percentage(self, enrollment_id: int, total_lessons: int) -> int:
        if total_lessons <= 0:
            return 0
        done = len(self.get_completed_lesson_ids(enrollment_id))
        return int(round((done / total_lessons) * 100))