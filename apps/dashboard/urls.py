from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.student_dashboard, name='student_dashboard'),
    path('my-courses/', views.my_courses_view, name='my_courses'),
]
