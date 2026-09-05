from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    )
    email = models.EmailField(unique=True, help_text="Required. Used for account login and notifications.")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Contact number for communications.")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name if name else self.username

    @property
    def is_student_role(self):
        return self.role == 'student'

    @property
    def is_instructor_role(self):
        return self.role == 'instructor' or self.is_staff


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    headline = models.CharField(max_length=150, blank=True, help_text="e.g. Aspiring Full Stack Developer")
    bio = models.TextField(blank=True, help_text="Short description about your learning goals and interests.")
    education = models.CharField(max_length=150, blank=True, help_text="e.g. B.Tech Computer Science, BCA")
    city = models.CharField(max_length=100, blank=True, default="Indore")
    state = models.CharField(max_length=100, blank=True, default="Madhya Pradesh")
    country = models.CharField(max_length=100, blank=True, default="India")
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"


@receiver(post_save, sender=User)
def create_or_update_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
