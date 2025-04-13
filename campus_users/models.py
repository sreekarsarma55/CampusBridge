from django.contrib.auth.models import AbstractUser
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.name
    
        
class Faculty(models.Model):
    email = models.EmailField(unique=True)
    role_choices = [
        ('instructor', 'Instructor'),
        ('coordinator', 'Coordinator'),
    ]
    role = models.CharField(max_length=20, choices=role_choices)
    
    def __str__(self):
        return self.email


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_student(self):
        return self.role == 'student'

    def is_faculty(self):
        return self.role == 'faculty'

    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return f"{self.username} ({self.role})"

class SystemLog(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} at {self.timestamp}"
    
class SiteAnalytics(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user_growth = models.IntegerField()
    engagement = models.IntegerField()

    def __str__(self):
        return f"Analytics - {self.date}"
    
class StudentRecord(models.Model):
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    year = models.IntegerField()
    gpa = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.student_id}"
    

class SystemSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Campus Bridge")
    admin_email = models.EmailField(default="admin@example.com")
    default_language = models.CharField(max_length=20, default="English")

    def __str__(self):
        return "System Settings"
    

class StudentProgress(models.Model):
    student_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attendance = models.FloatField()
    quiz_scores = models.FloatField()
    code_streak = models.IntegerField()

class ScheduledEvent(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20)
    date_time = models.DateTimeField()
    description = models.TextField()

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    material_type = models.CharField(max_length=20)
    file = models.FileField(upload_to='materials/', null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    availability_start = models.DateTimeField()
    availability_end = models.DateTimeField()