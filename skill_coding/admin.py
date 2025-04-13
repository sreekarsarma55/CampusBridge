from django.contrib import admin
from .models import CodingTrack, CodingProblem, Submission, UserTrackProgress

@admin.register(CodingTrack)
class CodingTrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created_at')
    search_fields = ('title',)
    list_filter = ('difficulty',)

@admin.register(CodingProblem)
class CodingProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'track', 'difficulty', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('difficulty', 'track')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'is_correct', 'score', 'submitted_at')
    list_filter = ('is_correct', 'submitted_at')
    search_fields = ('user__username', 'problem__title')

@admin.register(UserTrackProgress)
class UserTrackProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'track', 'score', 'last_updated')
    search_fields = ('user__username', 'track__title')
