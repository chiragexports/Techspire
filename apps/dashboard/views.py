from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.enrollments.models import Enrollment, LessonProgress
from apps.certificates.models import Certificate
from apps.quizzes.models import QuizAttempt

@login_required
def student_dashboard(request):
    user = request.user
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__category')
    
    total_enrolled = enrollments.count()
    completed_courses = enrollments.filter(status='completed').count()
    in_progress_courses = enrollments.filter(status='active').count()
    
    certificates = Certificate.objects.filter(user=user).select_related('course')
    total_certificates = certificates.count()

    recent_attempts = QuizAttempt.objects.filter(user=user).select_related('quiz', 'quiz__course')[:5]

    # Get recent in-progress enrollments
    active_enrollments = enrollments.filter(status='active')[:4]

    context = {
        'total_enrolled': total_enrolled,
        'completed_courses': completed_courses,
        'in_progress_courses': in_progress_courses,
        'total_certificates': total_certificates,
        'active_enrollments': active_enrollments,
        'certificates': certificates[:4],
        'recent_attempts': recent_attempts,
        'title': 'Student Dashboard - TECHSPIRE Learning',
    }
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def my_courses_view(request):
    user = request.user
    status_filter = request.GET.get('status', 'all')
    
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__category')
    
    if status_filter == 'in_progress':
        enrollments = enrollments.filter(status='active')
    elif status_filter == 'completed':
        enrollments = enrollments.filter(status='completed')

    context = {
        'enrollments': enrollments,
        'current_status': status_filter,
        'title': 'My Enrolled Courses - TECHSPIRE Learning',
    }
    return render(request, 'dashboard/my_courses.html', context)
