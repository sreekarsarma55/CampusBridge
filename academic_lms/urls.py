from django.urls import path
from . import views

app_name = 'academic_lms'

urlpatterns = [
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('chapters/add/', views.add_chapter, name='add_chapter'),
    path('material/add/', views.add_material, name='add_material'),
    path('assignments/add/', views.add_assignment, name='add_assignment'),
    path('student/', views.student_lms_home, name='student_lms'),
    path('student/course/<int:course_id>/', views.view_course, name='student_course_detail'),
    path('student/chapter/<int:chapter_id>/', views.view_chapter, name='student_chapter_detail'),
    path('materials/chapter/<int:chapter_id>/', views.view_materials, name='view_materials'),
    path('faculty/attendance/<int:course_id>/', views.faculty_view_attendance, name='faculty_view_attendance'),
    path('student/attendance/<int:course_id>/', views.student_view_attendance, name='view_student_attendance'),
    path('faculty/attendance/add/<int:course_id>/', views.add_attendance, name='add_attendance'),
    path('faculty/attendance/add/<int:course_id>/', views.add_attendance, name='add_attendance'),
    path('student/attendance/', views.student_attendance_summary, name='student_attendance_summary'),
    path('student/attendance-summary/', views.student_attendance_summary, name='student_attendance_summary'),


]
