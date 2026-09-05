from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_id', 'user', 'course', 'score_percentage', 'issued_at', 'is_revoked')
    list_filter = ('is_revoked', 'issued_at', 'course')
    search_fields = ('certificate_id', 'user__email', 'user__first_name', 'user__last_name', 'course__title')
    readonly_fields = ('certificate_id', 'issued_at')
    list_editable = ('is_revoked',)
