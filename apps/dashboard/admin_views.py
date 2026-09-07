import csv
from datetime import datetime
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.db.models import Count, Avg, Q, Sum
from django.core.paginator import Paginator
from django.utils import timezone

from apps.accounts.models import User
from apps.courses.models import Course, CourseCategory, Module, Lesson
from apps.enrollments.models import Enrollment, LessonProgress
from apps.quizzes.models import Quiz, Question, Choice, QuizAttempt, UserAnswer
from apps.certificates.models import Certificate
from apps.core.models import ActivityLog

def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.role == 'admin' or user.is_superuser)

def admin_required(view_func):
    return user_passes_test(is_admin_or_staff, login_url='accounts:login')(view_func)


@admin_required
def admin_overview(request):
    """
    Main Admin Dashboard Overview showing real-time database KPIs,
    recent activity feeds, and course performance analytics.
    """
    total_users = User.objects.count()
    active_students = User.objects.filter(role='student', is_active=True).count()
    total_courses = Course.objects.count()
    total_lessons = Lesson.objects.count()
    total_enrollments = Enrollment.objects.count()
    total_lessons_completed = LessonProgress.objects.filter(is_completed=True).count()
    total_quizzes_attempted = QuizAttempt.objects.count()
    total_courses_completed = Enrollment.objects.filter(status='completed').count()
    total_certificates = Certificate.objects.count()

    # Average Quiz Score
    avg_quiz_score = QuizAttempt.objects.aggregate(avg_score=Avg('score'))['avg_score']
    avg_quiz_score = round(avg_quiz_score, 1) if avg_quiz_score else 0

    # Course Performance Leaderboard
    courses_stats = Course.objects.annotate(
        enroll_count=Count('enrollments', distinct=True),
        complete_count=Count('enrollments', filter=Q(enrollments__status='completed'), distinct=True)
    ).order_by('-enroll_count')[:6]

    # Recent Users
    recent_users = User.objects.select_related('profile').order_by('-date_joined')[:8]

    # Recent Activity Feed
    recent_activities = ActivityLog.objects.select_related('user', 'course', 'lesson', 'quiz').order_by('-created_at')[:15]

    context = {
        'total_users': total_users,
        'active_students': active_students,
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'total_enrollments': total_enrollments,
        'total_lessons_completed': total_lessons_completed,
        'total_quizzes_attempted': total_quizzes_attempted,
        'total_courses_completed': total_courses_completed,
        'total_certificates': total_certificates,
        'avg_quiz_score': avg_quiz_score,
        'courses_stats': courses_stats,
        'recent_users': recent_users,
        'recent_activities': recent_activities,
        'title': 'Admin Operations & Learning Analytics Dashboard',
    }
    return render(request, 'dashboard/admin/overview.html', context)


@admin_required
def admin_users_list(request):
    """
    Filterable and searchable student and user directory.
    """
    users = User.objects.all().order_by('-date_joined')

    # Search filter
    q = request.GET.get('q', '').strip()
    if q:
        users = users.filter(
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(username__icontains=q)
        )

    # Role filter
    role = request.GET.get('role', 'all').strip()
    if role and role != 'all':
        users = users.filter(role=role)

    # Status filter
    status = request.GET.get('status', 'all').strip()
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)

    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Build student metrics map for page objects
    user_ids = [u.id for u in page_obj]
    enrollments = Enrollment.objects.filter(user_id__in=user_ids)
    
    user_metrics = {}
    for uid in user_ids:
        u_enrolls = [e for e in enrollments if e.user_id == uid]
        user_metrics[uid] = {
            'started': len(u_enrolls),
            'completed': sum(1 for e in u_enrolls if e.status == 'completed'),
            'quizzes_taken': QuizAttempt.objects.filter(user_id=uid).count(),
            'last_active': ActivityLog.objects.filter(user_id=uid).order_by('-created_at').first()
        }

    context = {
        'page_obj': page_obj,
        'user_metrics': user_metrics,
        'current_q': q,
        'current_role': role,
        'current_status': status,
        'total_matching': users.count(),
        'title': 'User Management & Learner Directory',
    }
    return render(request, 'dashboard/admin/users_list.html', context)


@admin_required
def admin_user_detail(request, user_id):
    """
    360-Degree Individual Learner Progress & Learning Journey Dossier.
    """
    target_user = get_object_or_404(User.objects.select_related('profile'), id=user_id)
    
    # Enrollments with detailed lesson metrics
    enrollments = Enrollment.objects.filter(user=target_user).select_related('course', 'last_accessed_lesson')
    
    enrollment_details = []
    for enroll in enrollments:
        total_lessons = Lesson.objects.filter(module__course=enroll.course).count()
        completed_lessons = enroll.lesson_progresses.filter(is_completed=True).count()
        progress_pct = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0

        # Quiz stats for this course
        attempts = QuizAttempt.objects.filter(user=target_user, quiz__course=enroll.course)
        best_score = attempts.order_by('-score').first()
        avg_score = attempts.aggregate(Avg('score'))['score__avg']

        enrollment_details.append({
            'enrollment': enroll,
            'course': enroll.course,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percentage': progress_pct,
            'last_accessed': enroll.last_accessed_lesson,
            'quiz_attempts_count': attempts.count(),
            'best_score': round(best_score.score, 1) if best_score else None,
            'avg_score': round(avg_score, 1) if avg_score else None,
            'status': enroll.status,
            'enrolled_at': enroll.enrolled_at,
            'completed_at': enroll.completed_at,
        })

    # Quiz Attempts History
    quiz_attempts = QuizAttempt.objects.filter(user=target_user).select_related('quiz', 'quiz__course').order_by('-started_at')

    # Activity Timeline
    activities = ActivityLog.objects.filter(user=target_user).select_related('course', 'lesson', 'quiz').order_by('-created_at')[:30]

    # Certificates
    certificates = Certificate.objects.filter(user=target_user).select_related('course')

    context = {
        'target_user': target_user,
        'enrollment_details': enrollment_details,
        'quiz_attempts': quiz_attempts,
        'activities': activities,
        'certificates': certificates,
        'title': f"Learner Profile: {target_user.full_name} ({target_user.email})",
    }
    return render(request, 'dashboard/admin/user_detail.html', context)


@admin_required
def admin_user_toggle_status(request, user_id):
    """
    Enable or disable a user account.
    """
    target_user = get_object_or_404(User, id=user_id)
    if target_user.is_superuser:
        messages.error(request, "Cannot modify active status of a superuser account.")
        return redirect('dashboard:admin_user_detail', user_id=target_user.id)

    target_user.is_active = not target_user.is_active
    target_user.save(update_fields=['is_active'])

    status_str = "activated" if target_user.is_active else "disabled"
    messages.success(request, f"User account '{target_user.email}' has been {status_str}.")
    
    ActivityLog.log(
        user=request.user,
        action_type='login',
        description=f"Admin {request.user.email} changed account status of {target_user.email} to {status_str}",
        request=request
    )
    return redirect('dashboard:admin_user_detail', user_id=target_user.id)


@admin_required
def admin_course_analytics(request):
    """
    Course-level aggregated analytics across enrollments, completions, and quizzes.
    """
    courses = Course.objects.all().select_related('category')

    courses_analytics = []
    for c in courses:
        enrollments = Enrollment.objects.filter(course=c)
        total_enrolled = enrollments.count()
        active_learners = enrollments.filter(status='active').count()
        completed_learners = enrollments.filter(status='completed').count()
        
        # Calculate average progress
        total_lessons = Lesson.objects.filter(module__course=c).count()
        total_completed_records = LessonProgress.objects.filter(enrollment__course=c, is_completed=True).count()
        avg_progress = 0
        if total_enrolled > 0 and total_lessons > 0:
            avg_progress = int((total_completed_records / (total_enrolled * total_lessons)) * 100)

        # Quiz metrics
        attempts = QuizAttempt.objects.filter(quiz__course=c)
        quiz_count = attempts.count()
        passed_count = attempts.filter(passed=True).count()
        pass_rate = int((passed_count / quiz_count * 100)) if quiz_count > 0 else 0
        avg_score = attempts.aggregate(Avg('score'))['score__avg']

        courses_analytics.append({
            'course': c,
            'total_enrolled': total_enrolled,
            'active_learners': active_learners,
            'completed_learners': completed_learners,
            'total_lessons': total_lessons,
            'avg_progress': min(100, avg_progress),
            'quiz_attempts_count': quiz_count,
            'pass_rate': pass_rate,
            'avg_score': round(avg_score, 1) if avg_score else 0,
        })

    context = {
        'courses_analytics': courses_analytics,
        'title': 'Course Performance & Completion Analytics',
    }
    return render(request, 'dashboard/admin/course_analytics.html', context)


@admin_required
def admin_lesson_analytics(request, course_id):
    """
    Lesson-level drilldown analytics to identify drop-off points and completion rates.
    """
    course = get_object_or_404(Course, id=course_id)
    modules = course.modules.prefetch_related('lessons').order_by('order')
    total_enrolled = Enrollment.objects.filter(course=course).count()

    modules_data = []
    for mod in modules:
        lessons_data = []
        for l in mod.lessons.all().order_by('order'):
            completed_count = LessonProgress.objects.filter(lesson=l, is_completed=True).count()
            viewed_count = ActivityLog.objects.filter(lesson=l, action_type='lesson_view').values('user').distinct().count()
            
            completion_pct = int((completed_count / total_enrolled * 100)) if total_enrolled > 0 else 0
            
            lessons_data.append({
                'lesson': l,
                'viewed_count': viewed_count,
                'completed_count': completed_count,
                'completion_pct': min(100, completion_pct),
            })

        modules_data.append({
            'module': mod,
            'lessons': lessons_data
        })

    context = {
        'course': course,
        'total_enrolled': total_enrolled,
        'modules_data': modules_data,
        'title': f"Lesson Analytics & Drop-off: {course.title}",
    }
    return render(request, 'dashboard/admin/lesson_analytics.html', context)


@admin_required
def admin_content_courses(request):
    """
    Course content management view: list courses with quick actions to edit, manage modules, lessons, notes, and quizzes.
    """
    courses = Course.objects.all().select_related('category').annotate(
        modules_count=Count('modules', distinct=True),
        enroll_count=Count('enrollments', distinct=True),
        quiz_count=Count('quizzes', distinct=True)
    ).order_by('category__order', '-created_at')

    context = {
        'courses': courses,
        'title': 'Course Content & Syllabus Management',
    }
    return render(request, 'dashboard/admin/content_courses.html', context)


@admin_required
def admin_course_editor(request, course_id=None):
    """
    Create or edit a course metadata, description, prerequisites, and publish state.
    """
    course = get_object_or_404(Course, id=course_id) if course_id else None
    categories = CourseCategory.objects.all().order_by('order', 'name')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        category_id = request.POST.get('category')
        short_description = request.POST.get('short_description', '').strip()
        description = request.POST.get('description', '').strip()
        level = request.POST.get('level', 'beginner')
        duration_hours = Decimal(request.POST.get('duration_hours', '10.0'))
        what_you_will_learn = request.POST.get('what_you_will_learn', '').strip()
        requirements = request.POST.get('requirements', '').strip()
        is_published = request.POST.get('is_published') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'

        category = get_object_or_404(CourseCategory, id=category_id)

        if course:
            course.title = title
            course.category = category
            course.short_description = short_description
            course.description = description
            course.level = level
            course.duration_hours = duration_hours
            course.what_you_will_learn = what_you_will_learn
            course.requirements = requirements
            course.is_published = is_published
            course.is_featured = is_featured
            course.save()
            messages.success(request, f"Course '{course.title}' updated successfully!")
        else:
            course = Course.objects.create(
                title=title,
                category=category,
                instructor=request.user,
                short_description=short_description,
                description=description,
                level=level,
                duration_hours=duration_hours,
                what_you_will_learn=what_you_will_learn,
                requirements=requirements,
                is_published=is_published,
                is_featured=is_featured,
                is_free=True
            )
            messages.success(request, f"Course '{course.title}' created successfully! Now add modules and lessons.")

        return redirect('dashboard:admin_content_courses')

    context = {
        'course': course,
        'categories': categories,
        'title': f"Edit Course: {course.title}" if course else "Create New Course",
    }
    return render(request, 'dashboard/admin/course_editor.html', context)


@admin_required
def admin_lesson_editor(request, course_id, lesson_id=None):
    """
    Rich notes and lesson content editor with live markdown preview support.
    """
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course) if lesson_id else None
    modules = course.modules.all().order_by('order')

    if request.method == 'POST':
        module_id = request.POST.get('module')
        title = request.POST.get('title', '').strip()
        order = int(request.POST.get('order', 1))
        duration_minutes = int(request.POST.get('duration_minutes', 15))
        notes_markdown = request.POST.get('notes_markdown', '').strip()
        key_takeaways = request.POST.get('key_takeaways', '').strip()
        interview_tips = request.POST.get('interview_tips', '').strip()
        practice_exercise = request.POST.get('practice_exercise', '').strip()
        exercise_solution = request.POST.get('exercise_solution', '').strip()
        is_preview = request.POST.get('is_preview') == 'on'

        module = get_object_or_404(Module, id=module_id, course=course)

        if lesson:
            lesson.module = module
            lesson.title = title
            lesson.order = order
            lesson.duration_minutes = duration_minutes
            lesson.notes_markdown = notes_markdown
            lesson.key_takeaways = key_takeaways
            lesson.interview_tips = interview_tips
            lesson.practice_exercise = practice_exercise
            lesson.exercise_solution = exercise_solution
            lesson.is_preview = is_preview
            lesson.save()
            messages.success(request, f"Lesson '{lesson.title}' notes updated successfully!")
        else:
            lesson = Lesson.objects.create(
                module=module,
                title=title,
                order=order,
                lesson_type='article',
                duration_minutes=duration_minutes,
                notes_markdown=notes_markdown,
                key_takeaways=key_takeaways,
                interview_tips=interview_tips,
                practice_exercise=practice_exercise,
                exercise_solution=exercise_solution,
                is_preview=is_preview
            )
            messages.success(request, f"Lesson '{lesson.title}' created successfully!")

        return redirect('dashboard:admin_lesson_analytics', course_id=course.id)

    context = {
        'course': course,
        'lesson': lesson,
        'modules': modules,
        'title': f"Notes Editor: {lesson.title}" if lesson else f"Add New Lesson to {course.title}",
    }
    return render(request, 'dashboard/admin/lesson_editor.html', context)


@admin_required
def admin_export_csv(request, report_type):
    """
    Generates downloadable CSV reports for Users, Course Progress, or Quiz Results.
    Strictly excludes passwords and secrets.
    """
    timestamp = timezone.now().strftime('%Y%m%d_%H%M')
    response = HttpResponse(content_type='text/csv')

    if report_type == 'users':
        response['Content-Disposition'] = f'attachment; filename="techspire_users_{timestamp}.csv"'
        writer = csv.writer(response)
        writer.writerow(['User ID', 'First Name', 'Last Name', 'Email', 'Role', 'Is Active', 'Date Joined', 'Last Login', 'Courses Enrolled', 'Courses Completed'])

        for u in User.objects.all().order_by('-date_joined'):
            enrolled = u.enrollments.count()
            completed = u.enrollments.filter(status='completed').count()
            writer.writerow([
                u.id,
                u.first_name,
                u.last_name,
                u.email,
                u.role,
                u.is_active,
                u.date_joined.strftime('%Y-%m-%d %H:%M') if u.date_joined else '',
                u.last_login.strftime('%Y-%m-%d %H:%M') if u.last_login else 'Never',
                enrolled,
                completed
            ])

    elif report_type == 'progress':
        response['Content-Disposition'] = f'attachment; filename="techspire_course_progress_{timestamp}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Enrollment ID', 'Student Email', 'Student Name', 'Course Title', 'Progress %', 'Completed Lessons', 'Total Lessons', 'Status', 'Enrolled At', 'Completed At'])

        for e in Enrollment.objects.select_related('user', 'course').all().order_by('-enrolled_at'):
            writer.writerow([
                e.id,
                e.user.email,
                e.user.full_name,
                e.course.title,
                f"{e.progress_percentage}%",
                e.completed_lessons_count,
                e.total_lessons,
                e.status.upper(),
                e.enrolled_at.strftime('%Y-%m-%d %H:%M') if e.enrolled_at else '',
                e.completed_at.strftime('%Y-%m-%d %H:%M') if e.completed_at else 'In Progress'
            ])

    elif report_type == 'quizzes':
        response['Content-Disposition'] = f'attachment; filename="techspire_quiz_results_{timestamp}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Attempt ID', 'Student Email', 'Student Name', 'Quiz Title', 'Course Title', 'Score %', 'Points Scored', 'Total Points', 'Passed', 'Date Attempted'])

        for att in QuizAttempt.objects.select_related('user', 'quiz', 'quiz__course').all().order_by('-started_at'):
            writer.writerow([
                att.id,
                att.user.email,
                att.user.full_name,
                att.quiz.title,
                att.quiz.course.title,
                f"{att.score}%",
                att.points_scored,
                att.total_points,
                'PASSED' if att.passed else 'FAILED',
                att.started_at.strftime('%Y-%m-%d %H:%M') if att.started_at else ''
            ])
    else:
        return HttpResponseForbidden("Invalid export report type requested.")

    return response
