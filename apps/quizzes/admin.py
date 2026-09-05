from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, UserAnswer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'pass_percentage', 'time_limit_minutes', 'is_published', 'created_at')
    list_filter = ('is_published', 'course')
    search_fields = ('title', 'description', 'course__title')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('prompt', 'quiz', 'question_type', 'points', 'order')
    list_filter = ('quiz', 'question_type')
    search_fields = ('prompt', 'explanation')
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question', 'is_correct')
    list_filter = ('is_correct', 'question__quiz')
    search_fields = ('choice_text', 'question__prompt')

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'selected_choice', 'is_correct')

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'points_scored', 'total_points', 'passed', 'completed_at')
    list_filter = ('passed', 'quiz', 'completed_at')
    search_fields = ('user__email', 'quiz__title')
    inlines = [UserAnswerInline]
    readonly_fields = ('started_at', 'completed_at')
