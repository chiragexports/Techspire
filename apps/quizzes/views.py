from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from apps.enrollments.models import Enrollment
from apps.core.models import ActivityLog
from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer

@login_required
def quiz_detail_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Auto-ensure enrollment so student is never blocked from taking assessment
    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user,
        course=quiz.course,
        defaults={'status': 'active'}
    )

    past_attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-started_at')
    has_passed = past_attempts.filter(passed=True).exists()
    attempts_left = max(0, quiz.max_attempts - past_attempts.count())

    context = {
        'quiz': quiz,
        'course': quiz.course,
        'enrollment': enrollment,
        'past_attempts': past_attempts,
        'has_passed': has_passed,
        'attempts_left': attempts_left,
        'title': f"Assessment: {quiz.title}",
    }
    return render(request, 'quizzes/quiz_detail.html', context)


@login_required
def take_quiz_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Auto-ensure active course enrollment
    enrollment, _ = Enrollment.objects.get_or_create(
        user=request.user,
        course=quiz.course,
        defaults={'status': 'active'}
    )

    # Check attempt limit
    attempts_count = QuizAttempt.objects.filter(user=request.user, quiz=quiz).count()
    if attempts_count >= quiz.max_attempts:
        messages.error(request, f"You have reached the maximum allowed attempts ({quiz.max_attempts}) for this assessment.")
        return redirect('quizzes:quiz_detail', quiz_id=quiz.id)

    questions = quiz.questions.prefetch_related('choices').all()

    if request.method == 'GET':
        ActivityLog.log(
            user=request.user,
            action_type='quiz_start',
            course=quiz.course,
            quiz=quiz,
            description=f"Started quiz '{quiz.title}'",
            request=request
        )

    if request.method == 'POST':
        # Evaluate Quiz Submission
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            started_at=timezone.now()
        )

        total_points = 0
        points_scored = 0

        for question in questions:
            total_points += question.points
            selected_choice_id = request.POST.get(f"question_{question.id}")
            
            selected_choice = None
            is_correct = False
            if selected_choice_id:
                selected_choice = Choice.objects.filter(id=selected_choice_id, question=question).first()
                if selected_choice and selected_choice.is_correct:
                    is_correct = True
                    points_scored += question.points

            UserAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_choice=selected_choice,
                is_correct=is_correct
            )

        score_percentage = (points_scored / total_points * 100) if total_points > 0 else 0
        passed = (score_percentage >= quiz.pass_percentage)

        attempt.total_points = total_points
        attempt.points_scored = points_scored
        attempt.score = score_percentage
        attempt.passed = passed
        attempt.completed_at = timezone.now()
        attempt.save()

        ActivityLog.log(
            user=request.user,
            action_type='quiz_submit',
            course=quiz.course,
            quiz=quiz,
            description=f"Submitted quiz '{quiz.title}' - Score {score_percentage:.1f}% ({'PASSED' if passed else 'FAILED'})",
            request=request
        )

        if passed:
            messages.success(request, f"🎉 Congratulations! You scored {score_percentage:.1f}% and passed the assessment!")
            # Trigger course completion and certificate generation
            enrollment.check_and_update_completion()
        else:
            messages.warning(request, f"You scored {score_percentage:.1f}%. Minimum required passing score is {quiz.pass_percentage}%. You can review your answers and retry.")

        return redirect('quizzes:quiz_result', attempt_id=attempt.id)

    context = {
        'quiz': quiz,
        'course': quiz.course,
        'enrollment': enrollment,
        'questions': questions,
        'title': f"Taking Assessment: {quiz.title}",
    }
    return render(request, 'quizzes/quiz_take.html', context)


@login_required
def quiz_result_view(request, attempt_id):
    attempt = QuizAttempt.objects.filter(
        id=attempt_id,
        user=request.user
    ).select_related('quiz__course', 'user').prefetch_related(
        'answers__question__choices', 'answers__selected_choice'
    ).first()

    if not attempt:
        # Fallback to latest attempt for current user
        attempt = QuizAttempt.objects.filter(
            user=request.user
        ).select_related('quiz__course', 'user').prefetch_related(
            'answers__question__choices', 'answers__selected_choice'
        ).order_by('-completed_at', '-id').first()
        
        if not attempt:
            messages.info(request, "No assessment attempts found.")
            return redirect('dashboard:student_dashboard')

    # Check for generated certificate
    from apps.certificates.models import Certificate
    certificate = Certificate.objects.filter(user=request.user, course=attempt.quiz.course).first()

    context = {
        'attempt': attempt,
        'quiz': attempt.quiz,
        'course': attempt.quiz.course,
        'certificate': certificate,
        'title': f"Result: {attempt.quiz.title} - Score {attempt.score}%",
    }
    return render(request, 'quizzes/quiz_result.html', context)
