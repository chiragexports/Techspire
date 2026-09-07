from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from apps.accounts.models import User
from apps.courses.models import Course, CourseCategory, Lesson
from apps.core.models import FAQ, Testimonial, ContactInquiry, SiteSetting
from apps.core.forms import ContactInquiryForm, NewsletterForm
from apps.enrollments.models import Enrollment, LessonProgress


def home_view(request):
    try:
        featured_courses = Course.objects.filter(is_published=True).select_related('category', 'instructor').order_by('-is_featured', 'category__order', '-created_at')[:6]
        categories = CourseCategory.objects.annotate(courses_count=Count('courses', filter=Q(courses__is_published=True))).order_by('order', 'name')
        faqs = FAQ.objects.filter(is_active=True)[:6]
        total_students = User.objects.filter(role='student').count()
        total_courses = Course.objects.filter(is_published=True).count()
        total_lessons = Lesson.objects.count()

        # Map user's active enrollments for logged-in users
        user_enrollments_map = {}
        if request.user.is_authenticated:
            for e in Enrollment.objects.filter(user=request.user):
                user_enrollments_map[e.course_id] = {
                    'progress': e.progress_percentage,
                    'status': e.status,
                    'completed_lessons': e.completed_lessons_count,
                    'total_lessons': e.total_lessons,
                }
    except Exception:
        featured_courses = []
        categories = []
        faqs = []
        total_students = 0
        total_courses = 0
        total_lessons = 0
        user_enrollments_map = {}
    
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'faqs': faqs,
        'total_students': total_students,
        'total_courses': total_courses,
        'total_lessons': total_lessons,
        'user_enrollments_map': user_enrollments_map,
        'title': 'Techspire - Professional Self-Paced Learning Academy',
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
