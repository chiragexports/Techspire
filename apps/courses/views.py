from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, CourseCategory, CourseReview, Lesson
from apps.enrollments.models import Enrollment

def course_list_view(request):
    courses = Course.objects.filter(is_published=True).select_related('category', 'instructor')
    categories = CourseCategory.objects.annotate(course_count=Count('courses')).filter(course_count__gt=0)
    
    # Search filter
    q = request.GET.get('q', '').strip()
    if q:
        courses = courses.filter(
            Q(title__icontains=q) |
            Q(short_description__icontains=q) |
            Q(description__icontains=q) |
            Q(category__name__icontains=q)
        )

    # Category filter
    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug:
        selected_category = CourseCategory.objects.filter(slug=category_slug).first()
        if selected_category:
            courses = courses.filter(category=selected_category)

    # Level filter
    level = request.GET.get('level', '').strip()
    if level and level != 'all':
        courses = courses.filter(level=level)

    # Price filter
    price_filter = request.GET.get('price', '').strip()
    if price_filter == 'free':
        courses = courses.filter(is_free=True)
    elif price_filter == 'paid':
        courses = courses.filter(is_free=False)

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'popular':
        courses = courses.annotate(enroll_count=Count('enrollments')).order_by('-enroll_count')
    elif sort_by == 'oldest':
        courses = courses.order_by('created_at')
    else: # newest
        courses = courses.order_by('-created_at')

    context = {
        'courses': courses,
        'categories': categories,
        'selected_category': selected_category,
        'current_q': q,
        'current_level': level,
        'current_price': price_filter,
        'current_sort': sort_by,
        'total_count': courses.count(),
        'title': 'Explore Online Courses - TECHSPIRE Learning',
    }
    return render(request, 'courses/course_list.html', context)


def course_detail_view(request, slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('modules__lessons', 'reviews__user'),
        slug=slug,
        is_published=True
    )
    
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        if enrollment:
            is_enrolled = True

    related_courses = Course.objects.filter(
        category=course.category,
        is_published=True
    ).exclude(id=course.id)[:3]

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
        'related_courses': related_courses,
        'title': f"{course.title} - TECHSPIRE Learning",
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def add_course_review(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    # Verify enrollment
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.error(request, "You must be enrolled in this course to leave a review.")
        return redirect('courses:course_detail', slug=course.slug)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '').strip()
        
        if comment:
            CourseReview.objects.update_or_create(
                course=course,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            messages.success(request, "Thank you for reviewing this course!")
        else:
            messages.error(request, "Please enter your review feedback.")

    return redirect('courses:course_detail', slug=course.slug)
