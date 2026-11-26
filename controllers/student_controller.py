from typing import Optional

from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtGui import QDesktopServices

from models.class_model import CourseClass
from models.course import Course
from models.registry import Enrollment
from models.user import User
from services.course_service import CourseService
from services.registry_service import RegistryService
from views.student.confirmation_view import ConfirmationView
from views.student.course_access_view import CourseAccessView


class StudentController(QObject):
    open_confirmation_requested = Signal()
    open_access_requested = Signal()
    open_home_requested = Signal()

    def __init__(
        self,
        confirmation_view: ConfirmationView,
        access_view: CourseAccessView,
        course_service: CourseService,
        registry_service: RegistryService,
    ) -> None:
        super().__init__()
        self.confirmation_view = confirmation_view
        self.access_view = access_view
        self.course_service = course_service
        self.registry_service = registry_service

        self.current_user: Optional[User] = None
        self.active_course: Optional[Course] = None
        self.active_enrollment: Optional[Enrollment] = None

        self.confirmation_view.go_course_access.connect(self.open_active_course)
        self.access_view.go_home.connect(self.open_home_requested.emit)
        self.access_view.lesson_toggled.connect(self.handle_lesson_toggle)
        self.access_view.watch_lesson.connect(self.open_video_url)

    def set_current_user(self, user: User) -> None:
        self.current_user = user
        self.active_course = None
        self.active_enrollment = None

    def reset_session(self) -> None:
        self.current_user = None
        self.active_course = None
        self.active_enrollment = None

    def confirm_enrollment(self, course: Course, course_class: CourseClass, payment_method: str) -> None:
        if not self.current_user or self.current_user.user_id is None:
            return
        self.active_course = course
        self.active_enrollment = self.registry_service.enroll_student(
            user_id=self.current_user.user_id,
            course_id=course.course_id,
            course_class=course_class.title,
            payment_method=payment_method,
        )
        self.confirmation_view.set_confirmation_data(course, course_class)
        self.open_confirmation_requested.emit()

    def open_active_course(self) -> None:
        if not self.current_user or self.current_user.user_id is None:
            return

        if not self.active_course:
            enrollments = self.registry_service.get_student_enrollments(self.current_user.user_id)
            if enrollments:
                self.active_enrollment = enrollments[-1]
                self.active_course = self.course_service.get_course_by_id(self.active_enrollment.course_id)
            else:
                featured = self.course_service.get_featured_courses()
                if not featured:
                    return
                self.active_course = featured[0]
                self.active_enrollment = self.registry_service.enroll_student(
                    user_id=self.current_user.user_id,
                    course_id=self.active_course.course_id,
                )

        if not self.active_course or not self.active_enrollment or self.active_enrollment.enrollment_id is None:
            return

        lessons = self.course_service.get_course_lessons(self.active_course.course_id)
        completed_ids = self.registry_service.get_completed_lesson_ids(self.active_enrollment.enrollment_id)
        pct = self.registry_service.calculate_progress_percentage(
            self.active_enrollment.enrollment_id,
            len(lessons),
        )
        self.access_view.set_course_data(self.active_course, lessons, completed_ids, pct)
        self.open_access_requested.emit()

    def handle_lesson_toggle(self, lesson_id: int, completed: bool) -> None:
        if not self.active_course or not self.active_enrollment or self.active_enrollment.enrollment_id is None:
            return
        self.registry_service.set_lesson_completed(
            enrollment_id=self.active_enrollment.enrollment_id,
            lesson_id=lesson_id,
            completed=completed,
        )
        lessons = self.course_service.get_course_lessons(self.active_course.course_id)
        pct = self.registry_service.calculate_progress_percentage(
            self.active_enrollment.enrollment_id,
            len(lessons),
        )
        self.access_view.update_progress(pct)

    @staticmethod
    def open_video_url(url: str) -> None:
        if url:
            QDesktopServices.openUrl(QUrl(url))