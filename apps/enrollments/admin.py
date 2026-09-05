from django.contrib import admin
from .models import Enrollment, LessonProgress

class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0
    readonly_fields = ('lesson', 'is_completed', 'completed_at')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'status', 'progress_percentage_display', 'enrolled_at', 'completed_at')
    list_filter = ('status', 'enrolled_at', 'course')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'course__title')
    inlines = [LessonProgressInline]

    def progress_percentage_display(self, obj):
        return f"{obj.progress_percentage}%"
    progress_percentage_display.short_description = "Progress"

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'is_completed', 'completed_at')
    list_filter = ('is_completed', 'enrollment__course')
    search_fields = ('enrollment__user__email', 'lesson__title')
