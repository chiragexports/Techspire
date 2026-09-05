from django.contrib import admin
from .models import CourseCategory, Course, Module, Lesson, CourseReview

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'lesson_type', 'duration_minutes', 'video_url', 'downloadable_file', 'is_preview', 'content')

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_class', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'is_free', 'price', 'is_published', 'is_featured', 'created_at')
    list_filter = ('category', 'level', 'is_free', 'is_published', 'is_featured')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured')
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]
    ordering = ('course', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'duration_minutes', 'is_preview', 'order')
    list_filter = ('lesson_type', 'is_preview', 'module__course')
    search_fields = ('title', 'content', 'module__title')
    ordering = ('module__course', 'module__order', 'order')

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('course__title', 'user__email', 'comment')
