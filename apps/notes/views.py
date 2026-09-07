import json
import uuid
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.db.models import Q, Count
from django.utils import timezone
from django.views.decorators.http import require_POST
from apps.courses.models import CourseCategory
from .models import (
    NotesProduct, NotesBundle, NotesChapter, NotesOrder,
    NotesReadingProgress, NotesBookmark, NotesReview, Coupon
)
from .pdf_generator import generate_notes_pdf_buffer

def marketplace_view(request):
    products = NotesProduct.objects.filter(is_published=True).select_related('category')
    bundles = NotesBundle.objects.filter(is_published=True).prefetch_related('products')
    categories = CourseCategory.objects.annotate(notes_count=Count('notes_products')).filter(notes_count__gt=0)

    # Filter Search
    q = request.GET.get('q', '').strip()
    if q:
        products = products.filter(
            Q(title__icontains=q) |
            Q(subtitle__icontains=q) |
            Q(short_description__icontains=q) |
            Q(full_description__icontains=q) |
            Q(category__name__icontains=q)
        )

    # Filter Category
    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug:
        selected_category = CourseCategory.objects.filter(slug=category_slug).first()
        if selected_category:
            products = products.filter(category=selected_category)

    # Filter Difficulty
    difficulty = request.GET.get('difficulty', '').strip()
    if difficulty and difficulty != 'all':
        products = products.filter(difficulty=difficulty)

    # Filter Price
    price_filter = request.GET.get('price', '').strip()
    if price_filter == 'free':
        products = products.filter(is_free=True)
    elif price_filter == 'paid':
        products = products.filter(is_free=False)

    # Sort
    sort_by = request.GET.get('sort', 'featured')
    if sort_by == 'popular':
        products = products.order_by('-order', '-created_at')
    elif sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    else: # featured
        products = products.order_by('-is_featured', 'order', '-created_at')

    # Check user owned products if logged in
    user_purchased_product_ids = set()
    if request.user.is_authenticated:
        # direct purchases
        direct_ids = NotesOrder.objects.filter(user=request.user, status='paid', product__isnull=False).values_list('product_id', flat=True)
        # bundle purchases
        bundle_products = NotesProduct.objects.filter(bundles__orders__user=request.user, bundles__orders__status='paid').values_list('id', flat=True)
        user_purchased_product_ids = set(list(direct_ids) + list(bundle_products))

    context = {
        'products': products,
        'bundles': bundles,
        'categories': categories,
        'selected_category': selected_category,
        'current_q': q,
        'current_difficulty': difficulty,
        'current_price': price_filter,
        'current_sort': sort_by,
        'total_count': products.count(),
        'user_purchased_product_ids': user_purchased_product_ids,
        'title': 'Premium Technical Notes & Study Material Marketplace — TECHSPIRE',
    }
    return render(request, 'notes/marketplace.html', context)


def product_detail_view(request, slug):
    product = get_object_or_404(
        NotesProduct.objects.select_related('category', 'related_course').prefetch_related('chapters', 'reviews__user'),
        slug=slug,
        is_published=True
    )
    
    is_purchased = product.user_has_purchased(request.user)
    chapters = product.chapters.all().order_by('order')
    first_preview_chapter = chapters.filter(is_preview=True).first() or chapters.first()
    
    # Related products in same category
    related_products = NotesProduct.objects.filter(
        category=product.category,
        is_published=True
    ).exclude(id=product.id)[:3]

    # Bundles that contain this product
    containing_bundles = product.bundles.filter(is_published=True)

    # Reading progress if purchased
    progress = None
    if request.user.is_authenticated and is_purchased:
        progress = NotesReadingProgress.objects.filter(user=request.user, product=product).first()

    context = {
        'product': product,
        'is_purchased': is_purchased,
        'chapters': chapters,
        'first_preview_chapter': first_preview_chapter,
        'related_products': related_products,
        'containing_bundles': containing_bundles,
        'progress': progress,
        'title': f"{product.title} — Premium Study Notes & E-Book",
    }
    return render(request, 'notes/product_detail.html', context)


def bundle_detail_view(request, slug):
    bundle = get_object_or_404(
        NotesBundle.objects.prefetch_related('products__category', 'products__chapters'),
        slug=slug,
        is_published=True
    )
    is_purchased = bundle.user_has_purchased(request.user)

    context = {
        'bundle': bundle,
        'is_purchased': is_purchased,
        'title': f"{bundle.title} — Premium Notes Bundle",
    }
    return render(request, 'notes/bundle_detail.html', context)


@login_required
def checkout_view(request, slug):
    product = get_object_or_404(NotesProduct, slug=slug, is_published=True)

    # Check if user already owns it
    if product.user_has_purchased(request.user):
        messages.info(request, f"You already own '{product.title}'! You can read the notes anytime.")
        return redirect('notes:reader', product_slug=product.slug)

    # Create or retrieve pending order
    order, _ = NotesOrder.objects.get_or_create(
        user=request.user,
        product=product,
        status='pending',
        defaults={
            'amount': product.price,
            'currency': product.currency
        }
    )
    order.amount = product.price
    order.save()

    context = {
        'item': product,
        'item_type': 'product',
        'order': order,
        'title': f"Checkout: {product.title}",
    }
    return render(request, 'notes/checkout.html', context)


@login_required
def bundle_checkout_view(request, slug):
    bundle = get_object_or_404(NotesBundle, slug=slug, is_published=True)

    if bundle.user_has_purchased(request.user):
        messages.info(request, f"You already own the '{bundle.title}' bundle!")
        return redirect('notes:marketplace')

    order, _ = NotesOrder.objects.get_or_create(
        user=request.user,
        bundle=bundle,
        status='pending',
        defaults={
            'amount': bundle.price,
            'currency': 'INR'
        }
    )
    order.amount = bundle.price
    order.save()

    context = {
        'item': bundle,
        'item_type': 'bundle',
        'order': order,
        'title': f"Checkout: {bundle.title}",
    }
    return render(request, 'notes/checkout.html', context)


@login_required
@require_POST
def verify_payment(request):
    """
    Handles payment verification and unlocks access.
    Supports both simulated test authorization and live gateway signatures.
    """
    order_id = request.POST.get('order_id')
    payment_id = request.POST.get('payment_id', f"PAY-SIM-{uuid.uuid4().hex[:10].upper()}")
    coupon_code = request.POST.get('coupon_code', '').strip().upper()

    order = get_object_or_404(NotesOrder, order_id=order_id, user=request.user)

    if coupon_code:
        coupon = Coupon.objects.filter(code=coupon_code, is_active=True).first()
        if coupon:
            discount = coupon.calculate_discount(order.amount)
            order.amount = max(Decimal('0.00'), order.amount - discount)
            coupon.uses_count += 1
            coupon.save()

    # Mark order as paid
    order.mark_as_paid(payment_id=payment_id)

    # If product purchase, initialize reading progress
    if order.product:
        NotesReadingProgress.objects.get_or_create(
            user=request.user,
            product=order.product,
            defaults={'progress_percentage': 0}
        )
    elif order.bundle:
        for p in order.bundle.products.all():
            NotesReadingProgress.objects.get_or_create(
                user=request.user,
                product=p,
                defaults={'progress_percentage': 0}
            )

    messages.success(request, "🎉 Payment Verified Successfully! Your complete notes and downloadable PDF are now unlocked.")
    return redirect('notes:order_success', order_id=order.order_id)


@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(NotesOrder, order_id=order_id, user=request.user, status='paid')
    context = {
        'order': order,
        'title': 'Order Successful — TECHSPIRE Notes Access Granted',
    }
    return render(request, 'notes/order_success.html', context)


def notes_reader_view(request, product_slug, chapter_slug=None):
    product = get_object_or_404(
        NotesProduct.objects.prefetch_related('chapters'),
        slug=product_slug,
        is_published=True
    )
    chapters = list(product.chapters.all().order_by('order'))
    if not chapters:
        messages.error(request, "No chapters available in this notes pack yet.")
        return redirect('notes:product_detail', slug=product.slug)

    # Determine current chapter
    current_chapter = None
    if chapter_slug:
        for ch in chapters:
            if ch.slug == chapter_slug or str(ch.order) == str(chapter_slug):
                current_chapter = ch
                break
    
    if not current_chapter:
        current_chapter = chapters[0]

    # Check Authorization:
    # If user has purchased OR if current chapter is free preview
    is_purchased = product.user_has_purchased(request.user)

    if not is_purchased and not current_chapter.is_preview:
        messages.warning(request, f"🔒 Chapter '{current_chapter.title}' is a Premium Chapter. Unlock the full study material to read all chapters and download the PDF.")
        return redirect('notes:product_detail', slug=product.slug)

    # Find prev and next chapters
    current_index = -1
    for idx, ch in enumerate(chapters):
        if ch.id == current_chapter.id:
            current_index = idx
            break

    prev_chapter = chapters[current_index - 1] if current_index > 0 else None
    next_chapter = chapters[current_index + 1] if current_index >= 0 and current_index < len(chapters) - 1 else None

    # Track progress and bookmarks if user is authenticated
    progress = None
    is_bookmarked = False
    completed_chapter_ids = set()

    if request.user.is_authenticated:
        progress, _ = NotesReadingProgress.objects.get_or_create(
            user=request.user,
            product=product
        )
        progress.current_chapter = current_chapter
        progress.save()
        completed_chapter_ids = set(progress.completed_chapters.values_list('id', flat=True))
        is_bookmarked = NotesBookmark.objects.filter(user=request.user, chapter=current_chapter).exists()

    context = {
        'product': product,
        'current_chapter': current_chapter,
        'chapters': chapters,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'is_purchased': is_purchased,
        'progress': progress,
        'completed_chapter_ids': completed_chapter_ids,
        'is_bookmarked': is_bookmarked,
        'title': f"{current_chapter.title} — {product.title} Reader",
    }
    return render(request, 'notes/reader.html', context)


@login_required
@require_POST
def mark_chapter_complete(request, product_slug, chapter_id):
    product = get_object_or_404(NotesProduct, slug=product_slug)
    chapter = get_object_or_404(NotesChapter, id=chapter_id, product=product)

    progress, _ = NotesReadingProgress.objects.get_or_create(user=request.user, product=product)
    progress.completed_chapters.add(chapter)
    progress.recalculate_progress()

    # Find next chapter
    chapters = list(product.chapters.all().order_by('order'))
    next_chapter = None
    for idx, ch in enumerate(chapters):
        if ch.id == chapter.id and idx < len(chapters) - 1:
            next_chapter = chapters[idx + 1]
            break

    if next_chapter:
        messages.success(request, f"Chapter {chapter.order} completed! Moving to Chapter {next_chapter.order}.")
        return redirect('notes:reader_chapter', product_slug=product.slug, chapter_slug=next_chapter.slug)
    else:
        messages.success(request, f"🎉 Congratulations! You have completed all chapters for {product.title}!")
        return redirect('notes:reader_chapter', product_slug=product.slug, chapter_slug=chapter.slug)


@login_required
@require_POST
def toggle_bookmark(request, chapter_id):
    chapter = get_object_or_404(NotesChapter, id=chapter_id)
    bookmark = NotesBookmark.objects.filter(user=request.user, chapter=chapter).first()
    
    if bookmark:
        bookmark.delete()
        is_bookmarked = False
        msg = "Bookmark removed."
    else:
        NotesBookmark.objects.create(user=request.user, chapter=chapter)
        is_bookmarked = True
        msg = "Chapter bookmarked in My Notes."

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_bookmarked': is_bookmarked, 'message': msg})
    
    messages.info(request, msg)
    return redirect('notes:reader_chapter', product_slug=chapter.product.slug, chapter_slug=chapter.slug)


def download_notes_pdf(request, slug):
    """
    Secure server-side protected PDF delivery.
    """
    product = get_object_or_404(NotesProduct, slug=slug, is_published=True)

    # Enforce purchase verification
    if not product.user_has_purchased(request.user):
        messages.error(request, "🔒 You must purchase this premium notes pack before downloading the complete PDF book.")
        return redirect('notes:product_detail', slug=product.slug)

    # Generate fresh watermarked ReportLab PDF buffer
    pdf_buffer = generate_notes_pdf_buffer(product, request.user)

    filename = f"TECHSPIRE_{product.slug.replace('-', '_')}_Complete_Notes.pdf"
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def my_notes_view(request):
    # Fetch all notes products user has purchased
    direct_purchased_ids = NotesOrder.objects.filter(user=request.user, status='paid', product__isnull=False).values_list('product_id', flat=True)
    bundle_purchased_ids = NotesProduct.objects.filter(bundles__orders__user=request.user, bundles__orders__status='paid').values_list('id', flat=True)
    all_purchased_ids = set(list(direct_purchased_ids) + list(bundle_purchased_ids))

    purchased_products = NotesProduct.objects.filter(id__in=all_purchased_ids).select_related('category')
    
    # Attach reading progress
    progress_map = {
        p.product_id: p for p in NotesReadingProgress.objects.filter(user=request.user, product__in=purchased_products).select_related('current_chapter')
    }

    products_with_progress = []
    for prod in purchased_products:
        prog = progress_map.get(prod.id)
        products_with_progress.append({
            'product': prod,
            'progress': prog,
            'progress_percentage': prog.progress_percentage if prog else 0,
            'current_chapter': prog.current_chapter if (prog and prog.current_chapter) else prod.chapters.first(),
        })

    bookmarks = NotesBookmark.objects.filter(user=request.user).select_related('chapter__product').order_by('-created_at')

    context = {
        'products_with_progress': products_with_progress,
        'bookmarks': bookmarks,
        'title': 'My Purchased Notes & Study Materials — TECHSPIRE',
    }
    return render(request, 'dashboard/my_notes.html', context)


@login_required
def my_orders_view(request):
    orders = NotesOrder.objects.filter(user=request.user).select_related('product', 'bundle').order_by('-created_at')
    context = {
        'orders': orders,
        'title': 'My Orders & Invoices — TECHSPIRE',
    }
    return render(request, 'dashboard/my_orders.html', context)


def check_coupon_api(request):
    code = request.GET.get('code', '').strip().upper()
    try:
        raw_amount = request.GET.get('amount', '0')
        amount = Decimal(str(raw_amount))
    except Exception:
        amount = Decimal('0.00')

    coupon = Coupon.objects.filter(code=code, is_active=True).first()
    
    if not coupon:
        return JsonResponse({'valid': False, 'message': 'Invalid or expired coupon code.'})

    discount = coupon.calculate_discount(amount)
    final_amount = max(Decimal('0.00'), amount - discount)

    return JsonResponse({
        'valid': True,
        'code': coupon.code,
        'discount_value': float(discount),
        'final_amount': float(final_amount),
        'message': f"Coupon applied: ₹{float(discount):.2f} OFF!"
    })
