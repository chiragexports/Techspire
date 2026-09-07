from django.contrib import admin
from django.db.models import Sum, Count
from .models import (
    NotesProduct, NotesBundle, NotesChapter, NotesOrder,
    NotesReadingProgress, NotesBookmark, NotesReview, Coupon
)

class NotesChapterInline(admin.StackedInline):
    model = NotesChapter
    extra = 1
    fields = ('order', 'title', 'is_preview', 'read_time_mins', 'summary', 'content_markdown', 'key_takeaways', 'interview_tips', 'practice_exercise', 'exercise_solution', 'downloadable_asset')

@admin.register(NotesProduct)
class NotesProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'original_price', 'difficulty', 'version', 'is_published', 'is_featured', 'order')
    list_filter = ('category', 'difficulty', 'is_published', 'is_featured')
    search_fields = ('title', 'subtitle', 'short_description', 'full_description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'is_published', 'is_featured', 'order')
    inlines = [NotesChapterInline]

@admin.register(NotesBundle)
class NotesBundleAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'original_price', 'is_published', 'is_featured', 'order')
    list_filter = ('is_published', 'is_featured')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('products',)
    list_editable = ('price', 'is_published', 'order')

@admin.register(NotesChapter)
class NotesChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'order', 'is_preview', 'read_time_mins')
    list_filter = ('product', 'is_preview')
    search_fields = ('title', 'summary', 'content_markdown')
    ordering = ('product', 'order')

@admin.register(NotesOrder)
class NotesOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'get_target_item', 'amount', 'currency', 'status', 'is_verified', 'created_at')
    list_filter = ('status', 'is_verified', 'currency', 'created_at')
    search_fields = ('order_id', 'user__email', 'user__first_name', 'user__last_name', 'gateway_payment_id')
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    actions = ['mark_as_paid', 'mark_as_refunded']

    def get_target_item(self, obj):
        return obj.product.title if obj.product else (obj.bundle.title if obj.bundle else "Item")
    get_target_item.short_description = "Purchased Product / Bundle"

    def mark_as_paid(self, request, queryset):
        queryset.update(status='paid', is_verified=True)
    mark_as_paid.short_description = "Mark selected orders as PAID"

    def mark_as_refunded(self, request, queryset):
        queryset.update(status='refunded')
    mark_as_refunded.short_description = "Mark selected orders as REFUNDED"

@admin.register(NotesReadingProgress)
class NotesReadingProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'progress_percentage', 'last_read_at')
    list_filter = ('product',)
    search_fields = ('user__email', 'product__title')

@admin.register(NotesBookmark)
class NotesBookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'chapter', 'note_text', 'created_at')
    search_fields = ('user__email', 'chapter__title', 'note_text')

@admin.register(NotesReview)
class NotesReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_verified_purchase', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'product')
    search_fields = ('product__title', 'user__email', 'comment')

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'uses_count', 'max_uses', 'is_active', 'valid_to')
    list_filter = ('discount_type', 'is_active')
    search_fields = ('code',)
