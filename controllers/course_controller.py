from typing import Optional

from PySide6.QtCore import QObject, Signal

from models.class_model import CourseClass
from models.course import Course
from services.course_service import CourseService
from views.courses.checkout_view import CheckoutView
from views.courses.course_details_view import CourseDetailsView
from views.home.home_view import HomeView


class CourseController(QObject):
    open_home_requested = Signal()
    open_details_requested = Signal()
    open_checkout_requested = Signal()
    purchase_finalized = Signal(object, object, str)  # curso, turma, metodo_pagamento
    open_my_courses_requested = Signal()
    logout_requested = Signal()

    def __init__(
        self,
        home_view: HomeView,
        details_view: CourseDetailsView,
        checkout_view: CheckoutView,
        course_service: CourseService,
    ) -> None:
        super().__init__()
        self.home_view = home_view
        self.details_view = details_view
        self.checkout_view = checkout_view
        self.course_service = course_service

        course_classes = self.course_service.get_available_course_classes()
        courses = self.course_service.get_featured_courses()

        self.selected_course: Optional[Course] = courses[0] if courses else None
        self.selected_course_class: CourseClass = course_classes[0]
        self.payment_method: str = "Cartão de crédito"

        # Sinais da Home
        self.home_view.search_changed.connect(self.filter_courses)
        self.home_view.course_selected.connect(self.select_course)
        self.home_view.go_my_courses.connect(self.open_my_courses_requested.emit)
        self.home_view.logout_requested.connect(self.logout_requested.emit)

        # Sinais de Detalhes
        self.details_view.go_back.connect(self.open_home_requested.emit)
        self.details_view.go_checkout.connect(self.prepare_checkout)
        self.details_view.toggle_favorite_requested.connect(self.toggle_favorite)

        # Sinais de Checkout
        self.checkout_view.go_back.connect(self.open_details_requested.emit)
        self.checkout_view.course_class_selected.connect(self._set_course_class)
        self.checkout_view.payment_selected.connect(self._set_payment)
        self.checkout_view.purchase_completed.connect(self._finish_purchase)

        self.load_home()

    def set_current_user(self, user_id: Optional[str]) -> None:
        self.course_service.set_current_user(user_id)

    def load_home(self) -> None:
        courses = self.course_service.get_featured_courses()
        self.home_view.display_courses(courses)

    def filter_courses(self, query: str, only_under_100: bool) -> None:
        courses = self.course_service.get_featured_courses(query=query, only_under_100=only_under_100)
        self.home_view.display_courses(courses)

    def select_course(self, course: Course) -> None:
        self.selected_course = course
        lessons = self.course_service.get_course_lessons(course.course_id)
        is_fav = self.course_service.is_favorite(course.course_id)
        self.details_view.set_course(course, lessons, is_fav)
        self.open_details_requested.emit()

    def toggle_favorite(self) -> None:
        if not self.selected_course:
            return
        is_fav = self.course_service.toggle_favorite(self.selected_course.course_id)
        self.details_view.set_favorite(is_fav)

    def prepare_checkout(self) -> None:
        if not self.selected_course:
            return
        course_classes = self.course_service.get_available_course_classes()
        self.checkout_view.set_checkout_data(
            course=self.selected_course,
            course_classes=course_classes,
            selected_course_class=self.selected_course_class,
            payment_method=self.payment_method,
        )
        self.open_checkout_requested.emit()

    def _set_course_class(self, course_class: CourseClass) -> None:
        self.selected_course_class = course_class

    def _set_payment(self, method: str) -> None:
        self.payment_method = method

    def _finish_purchase(self) -> None:
        if self.selected_course:
            self.purchase_finalized.emit(self.selected_course, self.selected_course_class, self.payment_method)