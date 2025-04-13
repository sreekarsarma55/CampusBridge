from django.urls import path
from . import views

app_name = 'skill_coding'

urlpatterns = [
    path('', views.faculty_dashboard, name='faculty_dashboard'),  # Faculty dashboard
    path('tracks/', views.track_list, name='track_list'),
    path('track/<int:track_id>/', views.track_detail, name='track_detail'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('submit/<int:problem_id>/', views.submit_code, name='submit_code'),
    path('add/track/', views.add_track, name='add_track'),  # Faculty page to add tracks
    path('add/problem/<int:track_id>/', views.add_problem, name='add_problem'),  # Faculty page to add problems
    path('submissions/', views.submission_history, name='submission_history'),
    path('ask-assistant/', views.ask_assistant, name='ask_assistant'),


]
