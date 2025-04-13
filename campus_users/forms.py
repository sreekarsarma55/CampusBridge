from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import CustomUser, Course, Faculty

from django.contrib.auth import get_user_model

User = get_user_model()

class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_student = True
        if commit:
            user.save()
        return user

class FacultySignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_faculty = True
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name',  'description']

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['email', 'role']

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'is_active']