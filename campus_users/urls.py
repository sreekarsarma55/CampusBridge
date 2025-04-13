from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('placement/tools', views.placement_tools, name='placement_tools'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/faculty/', views.faculty_signup, name='faculty_signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    #########
    path('dashboard/student/', views.dashboard_student, name='dashboard_student'),
    path('dashboard/student/my-courses/', views.my_courses, name='my_courses'),
    path('dashboard/student/assignments/', views.assignments_attendance, name='assignments_attendance'),
    path('dashboard/student/coding-tracks/', views.coding_tracks, name='coding_tracks'),
    path('dashboard/student/code-editor/', views.code_editor, name='code_editor'),
    path('run-code/', views.run_code, name='run_code'),

    path('dashboard/student/my-progress/', views.my_progress, name='my_progress'),
    path('dashboard/student/ai-assistant/', views.ai_code_assistant, name='ai_code_assistant'),
    path('dashboard/student/live-rooms/', views.live_code_rooms, name='live_code_rooms'),
    path('dashboard/student/job-match/', views.job_match_recommender, name='job_match_recommender'),
    path('dashboard/student/achievements/', views.achievements, name='achievements'),
    path('dashboard/student/settings/', views.settings, name='settings'),

    # Faculty Panel
    path('dashboard/faculty/', views.dashboard_faculty, name='dashboard_faculty'),
    path('dashboard/faculty/upload-content/', views.upload_content, name='upload_content'),
    path('dashboard/faculty/schedule/', views.schedule_lectures_quizzes, name='schedule_lectures_quizzes'),
    path('dashboard/faculty/coding-assignments/', views.create_coding_assignments, name='create_coding_assignments'),
    path('dashboard/faculty/student-progress/', views.monitor_student_progress, name='monitor_student_progress'),
    path('dashboard/faculty/analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('dashboard/faculty/announcements/', views.announcements_faculty, name='announcements_faculty'),

    # Admin Panel
    path('dashboard/admin/', views.admin_dashboard, name='dashboard_admin'),
    path('system-logs/', views.system_logs, name='admin_logs'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('faculty-access/', views.faculty_access, name='faculty_access'),
    path('course-management/', views.course_management, name='course_management'),
    path('site-analytics/', views.admin_site_analytics, name='admin_site_analytics'),
    path('student-records/', views.admin_student_records, name='admin_student_records'),
    path('system-settings/', views.admin_system_settings, name='admin_system_settings'),
    
    
]
