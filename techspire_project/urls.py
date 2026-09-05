from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from apps.certificates import views as cert_views

def robots_txt(request):
    content = "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /dashboard/\nSitemap: /sitemap.xml\n"
    return HttpResponse(content, content_type="text/plain")

urlpatterns = [
    # Custom Admin & Auth
    path('admin/', admin.site.urls),
    
    # App URLs
    path('', include('apps.core.urls', namespace='core')),
    path('auth/', include('apps.accounts.urls', namespace='accounts')),
    path('courses/', include('apps.courses.urls', namespace='courses')),
    path('learn/', include('apps.enrollments.urls', namespace='enrollments')),
    path('quiz/', include('apps.quizzes.urls', namespace='quizzes')),
    path('certificates/', include('apps.certificates.urls', namespace='certificates')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    
    # Direct short URL for certificate verification
    path('verify-certificate/', cert_views.public_verify_certificate, name='verify_certificate_direct'),

    # SEO & Bot files
    path('robots.txt', robots_txt, name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site branding
admin.site.site_header = "TECHSPIRE Learning Administration"
admin.site.site_title = "TECHSPIRE LMS Portal"
admin.site.index_title = "Academic & Course Management Dashboard"
