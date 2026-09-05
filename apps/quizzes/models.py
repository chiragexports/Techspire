from django.db import models
from django.conf import settings
from apps.courses.models import Course, Module

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes')
    module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, help_text="Instructions, topics covered, and exam criteria")
    pass_percentage = models.PositiveIntegerField(default=70, help_text="Minimum score percentage required to pass")
    time_limit_minutes = models.PositiveIntegerField(default=15, help_text="Time limit in minutes (0 for untimed)")
    max_attempts = models.PositiveIntegerField(default=5, help_text="Maximum retry attempts allowed")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ['course', 'id']

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    @property
    def total_questions_count(self):
        return self.questions.count()

    @property
    def total_points(self):
        return sum(q.points for q in self.questions.all())

    def user_highest_attempt(self, user):
        return self.attempts.filter(user=user).order_by('-score').first()

    def user_attempts_count(self, user):
        return self.attempts.filter(user=user).count()

    def has_user_passed(self, user):
        return self.attempts.filter(user=user, passed=True).exists()


class Question(models.Model):
    QUESTION_TYPES = (
        ('single', 'Single Choice (Radio)'),
        ('multiple', 'Multiple Choice (Checkbox)'),
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    prompt = models.TextField(help_text="The question text or problem statement")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='single')
    points = models.PositiveIntegerField(default=1)
    explanation = models.TextField(blank=True, help_text="Explanation shown after evaluation")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['order', 'id']

    def __str__(self):
        return f"Q{self.order}: {self.prompt[:60]}..."


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"

    def __str__(self):
        return f"{self.choice_text} ({'Correct' if self.is_correct else 'Incorrect'})"


class QuizAttempt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Percentage score")
    points_scored = models.PositiveIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Quiz Attempt"
        verbose_name_plural = "Quiz Attempts"
        ordering = ['-started_at']

    def __str__(self):
        status = "PASSED" if self.passed else "FAILED"
        return f"{self.user.email} - {self.quiz.title} ({self.score}% - {status})"


class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User Answer"
        verbose_name_plural = "User Answers"

    def __str__(self):
        return f"Answer for Q{self.question.id} in Attempt #{self.attempt.id}"
