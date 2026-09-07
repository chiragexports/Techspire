from django.urls import path
from . import views
from . import admin_views
from apps.notes import views as notes_views

app_name = 'dashboard'

urlpatterns = [
    # Student Views
    path('', views.student_dashboard, name='student_dashboard'),
    path('my-courses/', views.my_courses_view, name='my_courses'),
    path('my-notes/', notes_views.my_notes_view, name='my_notes'),
    path('my-orders/', notes_views.my_orders_view, name='my_orders'),

    # Admin Management & Analytics Suite
    path('admin-portal/', admin_views.admin_overview, name='admin_overview'),
    path('admin-portal', admin_views.admin_overview),
    path('admin-portal/users/', admin_views.admin_users_list, name='admin_users_list'),
    path('admin-portal/users/<int:user_id>/', admin_views.admin_user_detail, name='admin_user_detail'),
    path('admin-portal/users/<int:user_id>/toggle-status/', admin_views.admin_user_toggle_status, name='admin_user_toggle_status'),
    path('admin-portal/analytics/courses/', admin_views.admin_course_analytics, name='admin_course_analytics'),
    path('admin-portal/analytics/courses/<int:course_id>/lessons/', admin_views.admin_lesson_analytics, name='admin_lesson_analytics'),
    path('admin-portal/content/courses/', admin_views.admin_content_courses, name='admin_content_courses'),
    path('admin-portal/content/courses/create/', admin_views.admin_course_editor, name='admin_course_create'),
    path('admin-portal/content/courses/<int:course_id>/edit/', admin_views.admin_course_editor, name='admin_course_edit'),
    path('admin-portal/content/courses/<int:course_id>/lessons/create/', admin_views.admin_lesson_editor, name='admin_lesson_create'),
    path('admin-portal/content/courses/<int:course_id>/lessons/<int:lesson_id>/edit/', admin_views.admin_lesson_editor, name='admin_lesson_edit'),
    path('admin-portal/export/<str:report_type>/', admin_views.admin_export_csv, name='admin_export_csv'),
]

