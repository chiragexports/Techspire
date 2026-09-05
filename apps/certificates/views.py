from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib import messages
from .models import Certificate
from .pdf_generator import generate_certificate_pdf_buffer

@login_required
def my_certificates_view(request):
    certificates = Certificate.objects.filter(user=request.user).select_related('course')
    context = {
        'certificates': certificates,
        'title': 'My Earned Certificates - TECHSPIRE Learning',
    }
    return render(request, 'certificates/certificate_list.html', context)


@login_required
def certificate_view(request, cert_id):
    certificate = get_object_or_404(
        Certificate.objects.select_related('course', 'user'),
        certificate_id=cert_id,
        user=request.user
    )
    if not certificate.qr_code:
        certificate.generate_qr_code(request)
        certificate.save()

    context = {
        'certificate': certificate,
        'title': f"Certificate: {certificate.course.title}",
    }
    return render(request, 'certificates/certificate_view.html', context)


def download_certificate_pdf(request, cert_id):
    certificate = get_object_or_404(Certificate, certificate_id=cert_id)
    
    # Generate fresh PDF buffer
    pdf_buffer = generate_certificate_pdf_buffer(certificate, request)
    
    filename = f"TECHSPIRE_Certificate_{certificate.certificate_id}.pdf"
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def public_verify_certificate(request):
    cert_id = request.GET.get('cert_id', '').strip().upper()
    certificate = None
    has_searched = False
    is_valid = False

    if cert_id:
        has_searched = True
        certificate = Certificate.objects.filter(certificate_id__iexact=cert_id).select_related('course', 'user').first()
        if certificate and not certificate.is_revoked:
            is_valid = True

    context = {
        'cert_id': cert_id,
        'has_searched': has_searched,
        'certificate': certificate,
        'is_valid': is_valid,
        'title': 'Online Certificate Verification - TECHSPIRE Learning',
    }
    return render(request, 'certificates/verify_certificate.html', context)
