from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from apps.courses.models import Course, Module, Lesson
from apps.quizzes.models import Quiz
from apps.core.models import ActivityLog
from .models import Enrollment, LessonProgress

@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'status': 'active'}
    )

    if created:
        ActivityLog.log(
            user=request.user,
            action_type='course_enroll',
            course=course,
            description=f"Enrolled in course '{course.title}'",
            request=request
        )
        messages.success(request, f"🎉 You have successfully enrolled in '{course.title}'! Happy learning!")
    else:
        messages.info(request, f"Welcome back! Resuming your learning in '{course.title}'.")

    # Determine first lesson to start with
    target_lesson = enrollment.get_last_accessed_or_first_lesson()
    if target_lesson:
        return redirect('enrollments:lesson_view', course_slug=course.slug, lesson_id=target_lesson.id)
    return redirect('enrollments:classroom', course_slug=course.slug)


@login_required
def classroom_view(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'status': 'active'}
    )
    
    first_lesson = enrollment.get_last_accessed_or_first_lesson()
    if first_lesson:
        return redirect('enrollments:lesson_view', course_slug=course.slug, lesson_id=first_lesson.id)
    
    context = {
        'course': course,
        'enrollment': enrollment,
        'title': f"Classroom - {course.title}",
    }
    return render(request, 'enrollments/classroom.html', context)


@login_required
def lesson_view(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'status': 'active'}
    )
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    # Track last accessed lesson
    if enrollment.last_accessed_lesson != lesson:
        enrollment.last_accessed_lesson = lesson
        enrollment.save(update_fields=['last_accessed_lesson', 'updated_at'])

    # Get or create progress for this lesson
    progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )

    # Log lesson view
    ActivityLog.log(
        user=request.user,
        action_type='lesson_view',
        course=course,
        lesson=lesson,
        description=f"Opened lesson '{lesson.title}'",
        request=request
    )

    # Get all modules and lessons for sidebar hierarchy
    modules = course.modules.prefetch_related('lessons').all()
    all_lessons = list(Lesson.objects.filter(module__course=course).order_by('module__order', 'order'))
    
    # Calculate completed lesson ids
    completed_lesson_ids = set(
        enrollment.lesson_progresses.filter(is_completed=True).values_list('lesson_id', flat=True)
    )

    # Find prev and next lesson
    current_index = -1
    for idx, l in enumerate(all_lessons):
        if l.id == lesson.id:
            current_index = idx
            break

    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index >= 0 and current_index < len(all_lessons) - 1 else None

    # Associated assessment quiz
    associated_quiz = Quiz.objects.filter(course=course, is_published=True).first()

    context = {
        'course': course,
        'enrollment': enrollment,
        'lesson': lesson,
        'progress': progress,
        'modules': modules,
        'all_lessons': all_lessons,
        'completed_lesson_ids': completed_lesson_ids,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'associated_quiz': associated_quiz,
        'title': f"{lesson.title} - {course.title}",
    }
    return render(request, 'enrollments/lesson_view.html', context)


@login_required
def mark_lesson_complete(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    progress, _ = LessonProgress.objects.get_or_create(
        enrollment=enrollment,
        lesson=lesson
    )
    if not progress.is_completed:
        progress.mark_as_completed()
        ActivityLog.log(
            user=request.user,
            action_type='lesson_complete',
            course=course,
            lesson=lesson,
            description=f"Completed lesson '{lesson.title}'",
            request=request
        )

    # Find next lesson
    all_lessons = list(Lesson.objects.filter(module__course=course).order_by('module__order', 'order'))
    current_index = -1
    for idx, l in enumerate(all_lessons):
        if l.id == lesson.id:
            current_index = idx
            break

    next_lesson = all_lessons[current_index + 1] if current_index >= 0 and current_index < len(all_lessons) - 1 else None

    # Check if this completed the entire course
    if enrollment.progress_percentage >= 100:
        ActivityLog.log(
            user=request.user,
            action_type='course_complete',
            course=course,
            description=f"Completed 100% of lessons in '{course.title}'",
            request=request
        )

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'progress_percentage': enrollment.progress_percentage,
            'completed_count': enrollment.completed_lessons_count,
            'total_count': enrollment.total_lessons,
            'next_lesson_id': next_lesson.id if next_lesson else None,
        })

    if next_lesson:
        messages.success(request, f"✓ Lesson completed! Next: {next_lesson.title}")
        return redirect('enrollments:lesson_view', course_slug=course.slug, lesson_id=next_lesson.id)
    else:
        # Check if completed all lessons
        if enrollment.progress_percentage >= 100:
            messages.success(request, "🎉 Outstanding! You have completed all lessons for this course!")
            quiz = Quiz.objects.filter(course=course, is_published=True).first()
            if quiz:
                messages.info(request, "Now take the final assessment quiz to test your knowledge and earn your certificate!")
                return redirect('quizzes:quiz_detail', quiz_id=quiz.id)
            return redirect('certificates:my_certificates')
        
        return redirect('enrollments:lesson_view', course_slug=course.slug, lesson_id=lesson.id)

