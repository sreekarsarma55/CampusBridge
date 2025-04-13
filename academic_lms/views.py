import datetime
import json
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Chapter, Material, Assignment, Attendance
from campus_users.models import CustomUser
from django.views.generic import ListView

from .forms import CourseForm, ChapterForm, MaterialForm, AssignmentForm, AttendanceForm

class CourseListView(ListView):
    model = Course
    template_name = 'lms/course_list.html'  # The template to display the course list
    context_object_name = 'courses'

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academic_lms:course_list')
    else:
        form = CourseForm()
    return render(request, 'lms/form_template.html', {'form': form, 'title': 'Add Course'})

def add_chapter(request):
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academic_lms:course_list')
    else:
        form = ChapterForm()
    return render(request, 'lms/form_template.html', {'form': form, 'title': 'Add Chapter'})

def add_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save()
            return redirect('academic_lms:view_materials', chapter_id=material.chapter.id)
    else:
        form = MaterialForm()
    return render(request, 'lms/add_material.html', {'form': form})



def add_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academic_lms:course_list')
    else:
        form = AssignmentForm()
    return render(request, 'lms/form_template.html', {'form': form, 'title': 'Add Assignment'})


def student_lms_home(request):
    courses = Course.objects.all()
    return render(request, 'lms/student_lms.html', {'courses': courses})


def view_course(request, course_id):
    course = Course.objects.get(id=course_id)
    chapters = Chapter.objects.filter(course=course)
    return render(request, 'lms/student_course_detail.html', {
        'course': course,
        'chapters': chapters
    })

def view_chapter(request, chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    materials = chapter.materials.all()  # if you used a ForeignKey from Material to Chapter
    return render(request, 'lms/student_chapter_detail.html', {
        'chapter': chapter,
        'materials': materials
    })

def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapters = Chapter.objects.filter(course=course)
    return render(request, 'lms/student_course_detail.html', {
        'course': course,
        'chapters': chapters
    })

def view_chapter(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    materials = chapter.materials.all()  # assuming a ForeignKey from Material to Chapter
    return render(request, 'lms/student_chapter_detail.html', {
        'chapter': chapter,
        'materials': materials
    })
def view_materials(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    materials = Material.objects.filter(chapter=chapter)
    return render(request, 'lms/view_materials.html', {
        'chapter': chapter,
        'materials': materials
    })


def add_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    students = CustomUser.objects.filter(role='student')

    if request.method == 'POST':
        selected_date = request.POST.get('date')
        attendance_date = datetime.date.today()  # Default
        if selected_date:
            try:
                attendance_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
            except ValueError:
                pass  # fallback to today

        for student in students:
            status = request.POST.get(f'student_{student.id}')
            if status in ['P', 'A']:
                Attendance.objects.create(
                    course=course,
                    student=student,
                    status=status,
                    date=attendance_date
                )
        return redirect('academic_lms:faculty_view_attendance', course_id=course.id)

    return render(request, 'lms/add_attendance.html', {
        'course': course,
        'students': students,
    })




def faculty_view_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    attendances = Attendance.objects.filter(course=course)

    # If you want to display attendance per student:
    student_attendance = {}
    for attendance in attendances:
        if attendance.student not in student_attendance:
            student_attendance[attendance.student] = []
        student_attendance[attendance.student].append(attendance)

    return render(request, 'lms/faculty_view_attendance.html', {
        'course': course,
        'student_attendance': student_attendance,
    })



def student_view_attendance(request, course_id):
    
    user = request.user  # assuming that the user is authenticated and has the Student role
    attendances = Attendance.objects.filter(student=user)

    return render(request, 'lms/student_view_attendance.html', {
        'attendances': attendances,
    })


@login_required
def student_attendance_summary(request):
    student = request.user

    # Fetching attendance data for the student grouped by course
    attendance_data = (
        Attendance.objects.filter(student=student)
        .values('course__title')
        .annotate(
            present=Count('id', filter=Q(status='P')),
            absent=Count('id', filter=Q(status='A')),
            total=Count('id')
        )
    )

    # Extract data to be passed to the template (converting QuerySet to list of dictionaries)
    labels = [item['course__title'] for item in attendance_data]
    present = [item['present'] for item in attendance_data]
    absent = [item['absent'] for item in attendance_data]

    return render(request, 'lms/student_attendance_summary.html', {
        'labels': json.dumps(labels),
        'present': json.dumps(present),
        'absent': json.dumps(absent),
    })