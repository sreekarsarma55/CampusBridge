import datetime
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
import requests
from .models import Course, Faculty, SystemLog, CustomUser, SiteAnalytics, StudentRecord, SystemSettings, StudentProgress, ScheduledEvent,CourseMaterial
from .forms import CourseForm, FacultyForm, UserForm

from .forms import LoginForm, StudentSignupForm, FacultySignupForm

User = get_user_model()

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .models import Assignment, Course, JobMatch, Progress

@login_required
def home_view(request):
    return render(request, 'home.html')

def placement_tools(request):
    return render(request, 'placement_tools.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_faculty():
                return redirect('home')
            elif user.is_student():
                return redirect('home')
            else:
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})




# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Student Signup
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = StudentSignupForm()
    return render(request, 'users/signup_student.html', {'form': form})

# Faculty Signup (restricted to admin)
@user_passes_test(lambda u: u.is_superuser)
def faculty_signup(request):
    if request.method == 'POST':
        form = FacultySignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'faculty'
            user.save()
            return redirect('login')
    else:
        form = FacultySignupForm()
    return render(request, 'users/signup_faculty.html', {'form': form})

# Home View


# Dashboard View (differentiated by role)
@login_required
def dashboard_view(request):
    if request.user.is_superuser:
        return redirect('/admin/')  # or a custom admin dashboard if you create one

    elif hasattr(request.user, 'is_faculty') and request.user.is_faculty:
        return redirect('faculty_dashboard')

    elif hasattr(request.user, 'is_student') and request.user.is_student:
        return redirect('student_dashboard')

@login_required
def dashboard_student(request):
    return render(request, 'users/dashboard_student.html')

@login_required
def my_courses(request):
    return render(request, 'student/my_courses.html')

@login_required
def assignments_attendance(request):
    return render(request, 'student/assignments_attendance.html')

@login_required
def coding_tracks(request):
    return render(request, 'student/coding_tracks.html')

@login_required
def code_editor(request):
    return render(request, 'student/code_editor.html')

@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        language = request.POST.get('language')
        user_input = request.POST.get('input', '')

        lang_map = {
            'C': 'c',
            'C++': 'cpp',
            'Java': 'java',
            'Python': 'python3'
        }

        payload = {
            "clientId": settings.JDOODLE_CLIENT_ID,
            "clientSecret": settings.JDOODLE_CLIENT_SECRET,
            "script": code,
            "stdin": user_input,
            "language": lang_map.get(language, 'python3'),
            "versionIndex": "0"
        }

        response = requests.post("https://api.jdoodle.com/v1/execute", json=payload)
        result = response.json()
        return JsonResponse(result)

@login_required
def my_progress(request):
    return render(request, 'student/my_progress.html')

@login_required
def ai_code_assistant(request):
    return render(request, 'student/ai_code_assistant.html')

@login_required
def live_code_rooms(request):
    return render(request, 'student/live_code_rooms.html')

@login_required
def job_match_recommender(request):
    return render(request, 'student/job_match_recommender.html')

@login_required
def achievements(request):
    return render(request, 'student/achievements.html')
@login_required
def settings(request):
    return render(request, 'student/settings.html')
    

# Faculty Panel Views
@login_required
def dashboard_faculty(request):
    return render(request, 'users/dashboard_faculty.html')

def upload_content(request):
    courses = Course.objects.all()  # Get all courses for the dropdown
    if request.method == 'POST':
        course = request.POST['course']
        material_type = request.POST['material_type']
        file = request.FILES.get('file')  # Get uploaded file
        link = request.POST['link']  # Or a link to external material
        availability_start = request.POST['availability_start']
        availability_end = request.POST['availability_end']

        # Save the uploaded content
        material = CourseMaterial(course=course, material_type=material_type, file=file, link=link, availability_start=availability_start, availability_end=availability_end)
        material.save()
    return render(request, 'faculty/upload_content.html', {'courses': courses})

def schedule_lectures_quizzes(request):
    courses = Course.objects.all()  # Get all courses for selection
    if request.method == "POST":
        # Handle the form submission
        course = request.POST['course']
        event_type = request.POST['event_type']
        date_time = request.POST['date_time']
        description = request.POST['description']
        event = ScheduledEvent(course=course, event_type=event_type, date_time=date_time, description=description)
        event.save()
    return render(request, 'faculty/schedule_lectures_quizzes.html', {'courses': courses})

@login_required
def create_coding_assignments(request):
    return render(request, 'faculty/create_coding_assignments.html')

def monitor_student_progress(request):
    course_filter = request.GET.get('course', None)  # Get course filter if any
    if course_filter:
        students = StudentProgress.objects.filter(course=course_filter)
    else:
        students = StudentProgress.objects.all()

    return render(request, 'faculty/moniter_student_progress.html', {'students': students})

@login_required
def analytics_dashboard(request):
    # Assuming you want some statistics about student performance in each course
    courses = Course.objects.all()  # Get all courses
    student_stats = {}

    for course in courses:
        students = StudentProgress.objects.filter(course=course)
        total_students = students.count()
        total_attendance = sum([student.attendance for student in students]) / total_students if total_students else 0
        total_quiz_scores = sum([student.quiz_scores for student in students]) / total_students if total_students else 0

        student_stats[course.name] = {
            'total_students': total_students,
            'average_attendance': total_attendance,
            'average_quiz_scores': total_quiz_scores,
        }

    return render(request, 'faculty/analytics_dashboard.html', {'student_stats': student_stats})

@login_required
def announcements_faculty(request):
    return render(request, 'faculty/announcements_faculty.html')


# Admin Panel Views
def admin_dashboard(request):
    total_users = User.objects.count()
    total_faculty = User.objects.filter(role ="faculty").count()
    system_notices = [
        "Backup completed at 3:30 AM",
        "New faculty request pending approval",
    ]

    context = {
        'total_users': total_users,
        'total_faculty': total_faculty,
        'system_notices': system_notices,
        'user': request.user,
    }

    return render(request, 'users/dashboard_admin.html', context)

from django.shortcuts import render

def course_management(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            log = SystemLog(action=f"Course added - {form.cleaned_data['name']}")
            log.save()
            return redirect('admin_course_management')
    else:
        form = CourseForm()

    return render(request, 'admin/admin_course_management.html', {'form': form})

# View for Faculty Access
def faculty_access(request):
    if request.method == "POST":
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            log = SystemLog(action=f"Faculty access granted - {form.cleaned_data['email']}")
            log.save()
            return redirect('admin_faculty_access')
    else:
        form = FacultyForm()

    return render(request, 'admin/admin_faculty_access.html', {'form': form})

# View for System Logs
def system_logs(request):
    logs = SystemLog.objects.all()
    return render(request, 'admin/admin_logs.html', {'logs': logs})

# View for Manage Users
def manage_users(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/admin_manage_users.html', {'users': users})

def admin_site_analytics(request):
    queryset = SiteAnalytics.objects.all().order_by('-date')[:5][::-1]  # Oldest to latest
    labels = [entry.date.strftime('%b %d') for entry in queryset]
    growth_values = [entry.user_growth for entry in queryset]
    engagement_values = [entry.engagement_score for entry in queryset]

    analytics_data = {
        "growth": {
            "labels": labels,
            "values": growth_values
        },
        "engagement": {
            "labels": labels,
            "values": engagement_values
        }
    }

    return render(request, 'admin/admin_site_analytics.html', {
        'analytics': analytics_data
    })

def admin_student_records(request):
    students = StudentRecord.objects.all()
    return render(request, 'admin/admin_student_records.html', {'students': students})

def admin_system_settings(request):
    settings = SystemSettings.objects.first()  # Assuming only one record
    return render(request, 'admin/admin_system_settings.html', {'settings': settings})
