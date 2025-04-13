from django import forms
from .models import Course, Chapter, Material, Assignment,Attendance

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = '__all__'

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['course', 'chapter', 'title', 'description', 'file']


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = '__all__'

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'status', 'date']