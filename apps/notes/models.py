import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Avg
from apps.courses.models import CourseCategory, Course

def generate_order_id():
    unique_suffix = uuid.uuid4().hex[:8].upper()
    return f"TS-ORD-2026-{unique_suffix}"

class NotesProduct(models.Model):
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    )
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    subtitle = models.CharField(max_length=250, blank=True, help_text="e.g. Complete Comprehensive Guide & Interview Kit")
    short_description = models.CharField(max_length=350, help_text="Catchy 1-2 sentence overview for cards")
    full_description = models.TextField(help_text="Detailed overview, table of contents summary, audience, and key highlights")
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='notes_products')
    related_course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='notes_products')
    cover_image = models.ImageField(upload_to='notes/covers/', blank=True, null=True)
    author_name = models.CharField(max_length=120, default="TECHSPIRE Expert Academic Council")
    version = models.CharField(max_length=30, default="v2.0 (2026 Edition)")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    estimated_reading_hours = models.DecimalField(max_digits=5, decimal_places=1, default=12.0)
    page_count_est = models.PositiveIntegerField(default=150, help_text="Estimated textbook page count")
    exercise_count = models.PositiveIntegerField(default=25)
    project_count = models.PositiveIntegerField(default=5)
    interview_q_count = models.PositiveIntegerField(default=40)
    is_free = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=299.00, help_text="Selling price in INR")
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=599.00, help_text="Original printed edition / MRP in INR")
    currency = models.CharField(max_length=10, default="INR")
    pdf_file = models.FileField(upload_to='notes/pdfs/', blank=True, null=True, help_text="Uploaded pre-compiled PDF or generated asset")
    what_you_will_learn = models.TextField(help_text="Key takeaways separated by newlines", blank=True)
    prerequisites = models.TextField(help_text="Prerequisites separated by newlines", blank=True)
    target_audience = models.TextField(help_text="Target audience separated by newlines", blank=True)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notes Product"
        verbose_name_plural = "Notes Products"
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (₹{self.price})"

    def get_absolute_url(self):
        return reverse('notes:product_detail', kwargs={'slug': self.slug})

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            diff = self.original_price - self.price
            return int((diff / self.original_price) * 100)
        return 0

    @property
    def savings_amount(self):
        if self.original_price and self.original_price > self.price:
            return int(self.original_price - self.price)
        return 0

    @property
    def total_chapters_count(self):
        return self.chapters.count()

    @property
    def preview_chapters_count(self):
        return self.chapters.filter(is_preview=True).count()

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 4.9

    @property
    def total_sales_count(self):
        return self.orders.filter(status='paid').count() + 184

    @property
    def learning_points_list(self):
        if self.what_you_will_learn:
            return [p.strip() for p in self.what_you_will_learn.split('\n') if p.strip()]
        return []

    @property
    def prerequisites_list(self):
        if self.prerequisites:
            return [r.strip() for r in self.prerequisites.split('\n') if r.strip()]
        return []

    @property
    def target_audience_list(self):
        if self.target_audience:
            return [a.strip() for a in self.target_audience.split('\n') if a.strip()]
        return []

    def user_has_purchased(self, user):
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        # Direct product purchase
        if NotesOrder.objects.filter(user=user, product=self, status='paid').exists():
            return True
        # Purchase via bundle
        if NotesOrder.objects.filter(user=user, bundle__products=self, status='paid').exists():
            return True
        return False


class NotesBundle(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='notes/bundles/', blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=799.00)
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=1499.00)
    products = models.ManyToManyField(NotesProduct, related_name='bundles')
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notes Bundle"
        verbose_name_plural = "Notes Bundles"
        ordering = ['order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bundle: {self.title} (₹{self.price})"

    def get_absolute_url(self):
        return reverse('notes:bundle_detail', kwargs={'slug': self.slug})

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            diff = self.original_price - self.price
            return int((diff / self.original_price) * 100)
        return 0

    @property
    def savings_amount(self):
        if self.original_price and self.original_price > self.price:
            return int(self.original_price - self.price)
        return 0

    def user_has_purchased(self, user):
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return NotesOrder.objects.filter(user=user, bundle=self, status='paid').exists()


class NotesChapter(models.Model):
    product = models.ForeignKey(NotesProduct, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, blank=True)
    order = models.PositiveIntegerField(default=1)
    summary = models.CharField(max_length=350, blank=True)
    is_preview = models.BooleanField(default=False, help_text="Allow free sample preview to non-buyers")
    read_time_mins = models.PositiveIntegerField(default=20)
    content_markdown = models.TextField(help_text="Comprehensive structured study notes in Markdown/HTML")
    key_takeaways = models.TextField(blank=True, help_text="Key takeaways separated by newlines")
    interview_tips = models.TextField(blank=True, help_text="Interview tips and expected technical questions")
    practice_exercise = models.TextField(blank=True, help_text="Hands-on practice challenge")
    exercise_solution = models.TextField(blank=True, help_text="Solution and explanation")
    downloadable_asset = models.FileField(upload_to='notes/resources/', blank=True, null=True)

    class Meta:
        verbose_name = "Notes Chapter"
        verbose_name_plural = "Notes Chapters"
        ordering = ['order', 'id']
        unique_together = ('product', 'order')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"ch-{self.order}-{self.title[:50]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} - Ch {self.order}: {self.title}"

    @property
    def takeaways_list(self):
        if self.key_takeaways:
            return [t.strip() for t in self.key_takeaways.split('\n') if t.strip()]
        return []


class NotesOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('paid', 'Paid & Active'),
        ('failed', 'Payment Failed'),
        ('refunded', 'Refunded'),
        ('cancelled', 'Cancelled'),
    )
    order_id = models.CharField(max_length=60, unique=True, default=generate_order_id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes_orders')
    product = models.ForeignKey(NotesProduct, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    bundle = models.ForeignKey(NotesBundle, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway_payment_id = models.CharField(max_length=120, blank=True, null=True)
    gateway_order_id = models.CharField(max_length=120, blank=True, null=True)
    payment_method = models.CharField(max_length=50, default="UPI / Card / NetBanking")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Notes Order"
        verbose_name_plural = "Notes Orders"
        ordering = ['-created_at']

    def __str__(self):
        target = self.product.title if self.product else (self.bundle.title if self.bundle else "Item")
        return f"{self.order_id} - {self.user.email} - {target} ({self.status.upper()})"

    def mark_as_paid(self, payment_id=None):
        self.status = 'paid'
        self.is_verified = True
        if payment_id:
            self.gateway_payment_id = payment_id
        self.save()


class NotesReadingProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes_progress')
    product = models.ForeignKey(NotesProduct, on_delete=models.CASCADE, related_name='reading_records')
    current_chapter = models.ForeignKey(NotesChapter, on_delete=models.SET_NULL, null=True, blank=True)
    completed_chapters = models.ManyToManyField(NotesChapter, blank=True, related_name='completed_by_users')
    progress_percentage = models.PositiveIntegerField(default=0)
    last_read_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reading Progress"
        verbose_name_plural = "Reading Progress Records"
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.email} - {self.product.title} ({self.progress_percentage}%)"

    def recalculate_progress(self):
        total = self.product.chapters.count()
        if total == 0:
            self.progress_percentage = 0
        else:
            completed = self.completed_chapters.count()
            self.progress_percentage = min(100, int((completed / total) * 100))
        self.save()


class NotesBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes_bookmarks')
    chapter = models.ForeignKey(NotesChapter, on_delete=models.CASCADE, related_name='bookmarks')
    note_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notes Bookmark"
        verbose_name_plural = "Notes Bookmarks"
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f"{self.user.email} - Bookmark on {self.chapter.title}"


class NotesReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes_reviews')
    product = models.ForeignKey(NotesProduct, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)], default=5)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notes Review"
        verbose_name_plural = "Notes Reviews"
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} on {self.product.title} ({self.rating}★)"


class Coupon(models.Model):
    TYPE_CHOICES = (
        ('percentage', 'Percentage Discount (%)'),
        ('fixed', 'Fixed Discount (₹)'),
    )
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='percentage')
    discount_value = models.DecimalField(max_digits=6, decimal_places=2, help_text="e.g. 20 for 20% or 100 for ₹100")
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    max_uses = models.PositiveIntegerField(default=1000)
    uses_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    applicable_products = models.ManyToManyField(NotesProduct, blank=True, related_name='coupons')

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"

    def __str__(self):
        val = f"{self.discount_value}%" if self.discount_type == 'percentage' else f"₹{self.discount_value}"
        return f"{self.code} ({val} OFF)"

    def calculate_discount(self, original_price):
        if not original_price:
            return Decimal('0.00')
        price = Decimal(str(original_price))
        if self.discount_type == 'percentage':
            disc = (Decimal(str(self.discount_value)) / Decimal('100.0')) * price
            return round(disc, 2)
        return min(Decimal(str(self.discount_value)), price)
