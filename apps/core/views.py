from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.db.models import Count
from apps.courses.models import Course, CourseCategory
from apps.accounts.models import User
from .models import FAQ, Testimonial, ContactInquiry, SiteSetting
from .forms import ContactInquiryForm, NewsletterForm

def home_view(request):
    try:
        featured_courses = Course.objects.filter(is_published=True).select_related('category', 'instructor')[:6]
        categories = CourseCategory.objects.annotate(courses_count=Count('courses')).order_by('order', 'name')
        testimonials = Testimonial.objects.filter(is_featured=True)[:6]
        faqs = FAQ.objects.filter(is_active=True)[:6]
        total_students = User.objects.filter(role='student').count() + 1250
        total_courses = Course.objects.filter(is_published=True).count()
    except Exception:
        featured_courses = []
        categories = []
        testimonials = []
        faqs = []
        total_students = 1250
        total_courses = 0
    
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'testimonials': testimonials,
        'faqs': faqs,
        'total_students': total_students,
        'total_courses': total_courses,
        'title': 'TECHSPIRE Learning - Master Tech Skills Online',
    }
    return render(request, 'core/home.html', context)



def about_view(request):
    testimonials = Testimonial.objects.filter(is_featured=True)[:4]
    context = {
        'testimonials': testimonials,
        'title': 'About Us - TECHSPIRE Learning',
    }
    return render(request, 'core/about.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for reaching out! Our academic counseling team in Indore will get in touch with you shortly.")
            return redirect('core:contact')
        else:
            messages.error(request, "Please ensure all required fields are correctly filled in.")
    else:
        form = ContactInquiryForm()

    context = {
        'form': form,
        'title': 'Contact Us & Academic Support - TECHSPIRE Learning',
    }
    return render(request, 'core/contact.html', context)


def faq_view(request):
    faqs = FAQ.objects.filter(is_active=True)
    categories = FAQ.CATEGORY_CHOICES
    context = {
        'faqs': faqs,
        'categories': categories,
        'title': 'Frequently Asked Questions - TECHSPIRE Learning',
    }
    return render(request, 'core/faq.html', context)


def privacy_view(request):
    return render(request, 'core/privacy.html', {'title': 'Privacy Policy - TECHSPIRE Learning'})


def terms_view(request):
    return render(request, 'core/terms.html', {'title': 'Terms & Conditions - TECHSPIRE Learning'})


def refund_policy_view(request):
    return render(request, 'core/refund_policy.html', {'title': 'Refund and Cancellation Policy - TECHSPIRE Learning'})



def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully subscribed to TECHSPIRE Learning tech insights & free resources!")
        else:
            messages.info(request, "You are already subscribed or entered an invalid email.")
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))
