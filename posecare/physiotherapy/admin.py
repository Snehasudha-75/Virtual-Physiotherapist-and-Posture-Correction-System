from django.contrib import admin
from .models import HealthCondition, SessionFeedback, Exercise

@admin.register(HealthCondition)
class HealthConditionAdmin(admin.ModelAdmin):
    list_display = ('user', 'condition', 'pain_level')
    list_filter = ('condition', 'pain_level', 'user')
    search_fields = ('user__username', 'condition')
    ordering = ('user', 'condition')

@admin.register(SessionFeedback)
class SessionFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'condition', 'pain_level', 'posture_score', 'rating', 'date')
    list_filter = ('condition', 'date', 'pain_level', 'user')
    search_fields = ('user__username', 'condition', 'comment')
    readonly_fields = ('date',)
    ordering = ('-date',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'exercise_type', 'pain_level', 'duration_minutes', 'is_active')
    list_filter = ('exercise_type', 'pain_level', 'is_active')
    search_fields = ('name', 'description', 'instructions')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'exercise_type', 'pain_level')
        }),
        ('Details', {
            'fields': ('description', 'instructions', 'duration_minutes')
        }),
        ('Media', {
            'fields': ('video_url', 'gif_file')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
