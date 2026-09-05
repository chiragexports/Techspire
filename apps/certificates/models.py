import uuid
import qrcode
from io import BytesIO
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from django.urls import reverse
from apps.courses.models import Course

def generate_certificate_id():
    unique_suffix = uuid.uuid4().hex[:8].upper()
    return f"TS-2026-{unique_suffix}"

class Certificate(models.Model):
    certificate_id = models.CharField(max_length=50, unique=True, default=generate_certificate_id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    enrollment = models.OneToOneField('enrollments.Enrollment', on_delete=models.CASCADE, related_name='certificate')
    issued_at = models.DateTimeField(default=timezone.now)
    grade = models.CharField(max_length=20, default="Certificate of Excellence")
    score_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100.0)
    qr_code = models.ImageField(upload_to='certificates/qrcodes/', blank=True, null=True)
    pdf_file = models.FileField(upload_to='certificates/pdfs/', blank=True, null=True)
    is_revoked = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
        unique_together = ('user', 'course')
        ordering = ['-issued_at']

    def __str__(self):
        return f"{self.certificate_id} - {self.user.full_name} ({self.course.title})"

    def get_verification_url(self, request=None):
        verify_path = reverse('certificates:verify_public')
        query = f"?cert_id={self.certificate_id}"
        if request:
            return request.build_absolute_uri(verify_path + query)
        return f"/verify-certificate/{query}"

    def generate_qr_code(self, request=None):
        verification_url = self.get_verification_url(request)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=8,
            border=2,
        )
        qr.add_data(verification_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#0F172A", back_color="#FFFFFF")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        filename = f"qr_{self.certificate_id}.png"
        self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=False)

    @classmethod
    def generate_for_enrollment(cls, enrollment):
        existing = cls.objects.filter(user=enrollment.user, course=enrollment.course).first()
        if existing:
            return existing

        # Check user's highest quiz score if applicable
        from apps.quizzes.models import QuizAttempt
        attempts = QuizAttempt.objects.filter(user=enrollment.user, quiz__course=enrollment.course, passed=True).order_by('-score')
        highest_score = 100.0
        if attempts.exists():
            highest_score = float(attempts.first().score)

        cert = cls.objects.create(
            user=enrollment.user,
            course=enrollment.course,
            enrollment=enrollment,
            score_percentage=highest_score,
            issued_at=timezone.now()
        )
        cert.generate_qr_code()
        cert.save()
        return cert
