from django.db import models

class SiteSetting(models.Model):
    brand_name = models.CharField(max_length=100, default="TECHSPIRE Learning")
    tagline = models.CharField(max_length=200, default="Learn Today, Lead Tomorrow.")
    business_name = models.CharField(max_length=100, default="TECHSPIRE")
    proprietor_name = models.CharField(max_length=100, default="Vivek Jat")
    business_type = models.CharField(max_length=100, default="Proprietorship / Micro Enterprise")
    location = models.CharField(max_length=100, default="Indore, Madhya Pradesh, India")
    address = models.TextField(default="53/43 Radhaswami Nagar, Nowlakha, Indore, Madhya Pradesh 452001")
    email = models.EmailField(default="vivekjat301@gmail.com")
    phone = models.CharField(max_length=20, default="+91 9713931301")
    udyam_registration = models.CharField(max_length=50, default="UDYAM-MP-23-0283495")
    gstin = models.CharField(max_length=50, default="23BEZPJ5728J1ZW")
    hero_title = models.CharField(max_length=200, default="Master In-Demand Tech Skills & Build Your Future")
    hero_subtitle = models.TextField(default="Industry-aligned hands-on courses in Web Development, Python, AI Tools, and Data Analytics. Earn verified certificates recognized by top employers.")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return f"{self.brand_name} Settings"

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class FAQ(models.Model):
    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('courses', 'Courses & Learning'),
        ('certificates', 'Certificates & Verification'),
        ('enrollment', 'Enrollment & Access'),
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='general')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', 'id']

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g. Python Developer at Tech Corp")
    course_taken = models.CharField(max_length=150, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"


class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry from {self.name} - {self.subject}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('signup', 'Account Created'),
        ('course_enroll', 'Course Enrolled'),
        ('lesson_view', 'Lesson Opened'),
        ('lesson_complete', 'Lesson Completed'),
        ('quiz_start', 'Quiz Started'),
        ('quiz_submit', 'Quiz Submitted'),
        ('course_complete', 'Course Completed'),
        ('certificate_issued', 'Certificate Generated'),
    )

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='activity_logs'
    )
    action_type = models.CharField(max_length=30, choices=ACTION_CHOICES, db_index=True)
    course = models.ForeignKey('courses.Course', on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    quiz = models.ForeignKey('quizzes.Quiz', on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    description = models.CharField(max_length=300)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-created_at']

    def __str__(self):
        user_display = self.user.email if self.user else "Anonymous"
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M')}] {user_display} - {self.get_action_type_display()}: {self.description}"

    @classmethod
    def log(cls, user=None, action_type='login', description='', course=None, lesson=None, quiz=None, request=None):
        ip = None
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
            if not user and request.user.is_authenticated:
                user = request.user
        try:
            return cls.objects.create(
                user=user if (user and user.is_authenticated) else None,
                action_type=action_type,
                course=course,
                lesson=lesson,
                quiz=quiz,
                description=description,
                ip_address=ip
            )
        except Exception:
            return None

