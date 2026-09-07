from django.contrib import admin
from .models import CourseCategory, Course, Module, Lesson, CourseProject, InterviewQuestion, CourseAssignment, CourseReview

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'lesson_type', 'duration_minutes', 'video_url', 'downloadable_file', 'resource_title', 'is_preview', 'content', 'notes_markdown', 'practice_exercise', 'exercise_solution', 'interview_tips')

class ModuleInline(admin.StackedInline):
    model = Module
    extra = 1

class CourseProjectInline(admin.StackedInline):
    model = CourseProject
    extra = 0
    fields = ('title', 'order', 'difficulty', 'estimated_hours', 'technologies_used', 'github_starter_url', 'short_description', 'description', 'submission_instructions', 'is_published')

class InterviewQuestionInline(admin.TabularInline):
    model = InterviewQuestion
    extra = 0
    fields = ('order', 'category_tag', 'difficulty', 'question', 'answer')

class CourseAssignmentInline(admin.TabularInline):
    model = CourseAssignment
    extra = 0
    fields = ('order', 'module', 'title', 'max_score', 'instructions')

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
    inlines = [ModuleInline, CourseProjectInline, InterviewQuestionInline, CourseAssignmentInline]

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
    search_fields = ('title', 'content', 'notes_markdown', 'module__title')
    ordering = ('module__course', 'module__order', 'order')

@admin.register(CourseProject)
class CourseProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'difficulty', 'estimated_hours', 'order', 'is_published')
    list_filter = ('difficulty', 'is_published', 'course')
    search_fields = ('title', 'description', 'technologies_used')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'course', 'category_tag', 'difficulty', 'order')
    list_filter = ('difficulty', 'category_tag', 'course')
    search_fields = ('question', 'answer', 'category_tag')

@admin.register(CourseAssignment)
class CourseAssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'module', 'max_score', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'instructions')

@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('course__title', 'user__email', 'comment')
