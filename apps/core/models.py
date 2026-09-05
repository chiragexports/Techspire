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
