from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Avg

class CourseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, default='fas fa-laptop-code', help_text="FontAwesome icon e.g. 'fas fa-code'")
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"{reverse('courses:course_list')}?category={self.slug}"


class Course(models.Model):
    LEVEL_CHOICES = (
        ('all', 'All Levels'),
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='authored_courses')
    instructor_name = models.CharField(max_length=100, default="TECHSPIRE Expert Faculty", help_text="Displayed instructor or lead mentor name")
    short_description = models.CharField(max_length=300, help_text="Catchy 1-2 sentence overview for cards and listings")
    description = models.TextField(help_text="Detailed course syllabus, target audience, and overview")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration_hours = models.DecimalField(max_digits=5, decimal_places=1, default=10.0, help_text="Estimated completion hours")
    thumbnail = models.ImageField(upload_to='courses/thumbnails/', blank=True, null=True)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, help_text="Course fee in INR (0 if Free)")
    what_you_will_learn = models.TextField(help_text="Enter key outcomes separated by newlines", blank=True)
    requirements = models.TextField(help_text="Prerequisites separated by newlines", blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:course_detail', kwargs={'slug': self.slug})

    @property
    def learning_points_list(self):
        if self.what_you_will_learn:
            return [p.strip() for p in self.what_you_will_learn.split('\n') if p.strip()]
        return []

    @property
    def requirements_list(self):
        if self.requirements:
            return [r.strip() for r in self.requirements.split('\n') if r.strip()]
        return []

    @property
    def total_lessons_count(self):
        return Lesson.objects.filter(module__course=self).count()

    @property
    def total_modules_count(self):
        return self.modules.count()

    @property
    def total_duration_minutes(self):
        lessons = Lesson.objects.filter(module__course=self)
        return sum(l.duration_minutes for l in lessons)

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 4.9

    @property
    def total_enrollments(self):
        return self.enrollments.count()


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Course Module"
        verbose_name_plural = "Course Modules"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"


class Lesson(models.Model):
    LESSON_TYPES = (
        ('video', 'Video Lesson'),
        ('article', 'Reading & Code Tutorial'),
        ('quiz', 'Module Quiz / Assessment'),
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='video')
    order = models.PositiveIntegerField(default=1)
    duration_minutes = models.PositiveIntegerField(default=15, help_text="Approximate reading or viewing time")
    video_url = models.CharField(max_length=300, blank=True, help_text="Embeddable video link or YouTube embed URL")
    content = models.TextField(blank=True, help_text="Detailed lesson guide, code snippets, explanations")
    downloadable_file = models.FileField(upload_to='courses/resources/', blank=True, null=True, help_text="Code repository zip, cheat-sheet, or PDF")
    is_preview = models.BooleanField(default=False, help_text="Free sample preview lesson for visitors")

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ['order', 'id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.order}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.module.course.title} -> {self.module.title} -> {self.title}"

    @property
    def course(self):
        return self.module.course


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)], default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course Review"
        verbose_name_plural = "Course Reviews"
        unique_together = ('course', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} on {self.course.title} ({self.rating}★)"
