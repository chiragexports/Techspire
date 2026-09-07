from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.courses.models import Course, Lesson

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    last_accessed_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='last_accessed_enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        unique_together = ('user', 'course')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.user.email} enrolled in {self.course.title}"

    @property
    def total_lessons(self):
        return Lesson.objects.filter(module__course=self.course).count()

    @property
    def completed_lessons_count(self):
        return self.lesson_progresses.filter(is_completed=True).count()

    @property
    def progress_percentage(self):
        total = self.total_lessons
        if total == 0:
            return 0
        completed = self.completed_lessons_count
        return int((completed / total) * 100)

    @property
    def is_eligible_for_certificate(self):
        total = self.total_lessons
        if total == 0:
            return False
        return self.completed_lessons_count >= total

    def check_and_update_completion(self):
        if self.is_eligible_for_certificate:
            if self.status != 'completed':
                self.status = 'completed'
                self.completed_at = timezone.now()
                self.save(update_fields=['status', 'completed_at'])
            
            # Automatically generate certificate if not existing
            from apps.certificates.models import Certificate
            Certificate.generate_for_enrollment(self)
            return True
        return False

    def get_last_accessed_or_first_lesson(self):
        # Return last accessed lesson if set, otherwise find next incomplete lesson
        all_lessons = Lesson.objects.filter(module__course=self.course).order_by('module__order', 'order')
        completed_ids = set(self.lesson_progresses.filter(is_completed=True).values_list('lesson_id', flat=True))
        
        if self.last_accessed_lesson and self.last_accessed_lesson.id not in completed_ids:
            return self.last_accessed_lesson
            
        for lesson in all_lessons:
            if lesson.id not in completed_ids:
                return lesson
        return all_lessons.first()


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progresses')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Lesson Progress"
        verbose_name_plural = "Lesson Progresses"
        unique_together = ('enrollment', 'lesson')

    def __str__(self):
        status = "Completed" if self.is_completed else "In Progress"
        return f"{self.enrollment.user.email} - {self.lesson.title} ({status})"

    def mark_as_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()
        self.enrollment.check_and_update_completion()
