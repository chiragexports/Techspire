from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('<int:quiz_id>/', views.quiz_detail_view, name='quiz_detail'),
    path('<int:quiz_id>/take/', views.take_quiz_view, name='take_quiz'),
    path('result/<int:attempt_id>/', views.quiz_result_view, name='quiz_result'),
]
