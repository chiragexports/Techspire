from django.urls import path
from . import views

app_name = 'certificates'

urlpatterns = [
    path('my-certificates/', views.my_certificates_view, name='my_certificates'),
    path('view/<str:cert_id>/', views.certificate_view, name='view_certificate'),
    path('download/<str:cert_id>/', views.download_certificate_pdf, name='download_pdf'),
    path('verify-certificate/', views.public_verify_certificate, name='verify_public'),
]
