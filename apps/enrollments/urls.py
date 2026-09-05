from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    path('enroll/<slug:slug>/', views.enroll_course, name='enroll'),
    path('course/<slug:course_slug>/classroom/', views.classroom_view, name='classroom'),
    path('course/<slug:course_slug>/lesson/<int:lesson_id>/', views.lesson_view, name='lesson_view'),
    path('course/<slug:course_slug>/lesson/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_complete'),
]
