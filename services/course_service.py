"""Regras de negócio relacionadas a catálogo, busca e detalhes de cursos."""

from __future__ import annotations

from models.class_model import CourseClass, Lesson
from models.course import Category, Course
from repositories.course_repository import CourseRepository


class CourseService:
    """Encapsula regras de filtragem e consulta de cursos e aulas."""

    def __init__(self, repository: CourseRepository) -> None:
        self._repository = repository
        self._current_user_id: str | None = None
        self._favorites: set[int] = set()

    def set_current_user(self, user_id: str | None) -> None:
        self._current_user_id = user_id
        if user_id:
            self._favorites = self._repository.list_favorite_course_ids(user_id)
        else:
            self._favorites = set()

    def get_available_course_classes(self) -> list[CourseClass]:
        return self._repository.list_course_classes()

    def get_featured_courses(
        self,
        query: str = "",
        only_under_100: bool = False,
    ) -> list[Course]:
        courses = self._repository.list_active_courses()
        term = query.strip().lower()

        result: list[Course] = []
        for course in courses:
            if only_under_100 and course.price > 100.0:
                continue
            if (
                term
                and term not in course.name.lower()
                and term not in course.description.lower()
                and term not in course.summary.lower()
            ):
                continue
            result.append(course)

        return result

    def get_course_by_id(self, course_id: int) -> Course | None:
        return self._repository.get_course_by_id(course_id)

    def get_course_lessons(self, course_id: int) -> list[Lesson]:
        return self._repository.list_lessons_by_course(course_id)

    def is_favorite(self, course_id: int) -> bool:
        return course_id in self._favorites

    def toggle_favorite(self, course_id: int) -> bool:
        if course_id in self._favorites:
            if self._current_user_id:
                self._repository.remove_favorite(self._current_user_id, course_id)
            self._favorites.remove(course_id)
            return False
        if self._current_user_id:
            self._repository.add_favorite(self._current_user_id, course_id)
        self._favorites.add(course_id)
        return True

    def get_categories(self) -> list[Category]:
        return self._repository.list_categories()

    def filter_courses(
        self,
        search_term: str = "",
        category_id: int | None = None,
        level: str = "Todos",
    ) -> list[Course]:
        """Filtra cursos ativos por nome/descrição, categoria e nível."""
        courses = self._repository.list_active_courses()
        term = search_term.strip().lower()

        result: list[Course] = []
        for course in courses:
            if category_id is not None and course.category_id != category_id:
                continue
            if level != "Todos" and course.level != level:
                continue
            if term and term not in course.name.lower() and term not in course.description.lower():
                continue
            result.append(course)

        return result

    def get_course_details(self, course_id: int) -> tuple[Course, list[Lesson]]:
        """Retorna o curso e sua lista ordenada de aulas, validando existência."""
        course = self._repository.get_course_by_id(course_id)
        if course is None:
            raise ValueError(f"Curso com ID {course_id} não encontrado ou inativo.")
        lessons = self._repository.list_lessons_by_course(course_id)
        return course, lessons