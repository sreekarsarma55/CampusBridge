from django.db import models
from django.conf import settings  # For User model (assumes you are using the default User model)

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="materials")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="materials")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='materials/')
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey('academic_lms.Course', on_delete=models.CASCADE)  # Lazy reference
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS, default='A')
    date = models.DateField()

    class Meta:
        unique_together = ('student', 'course', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.date} - {self.get_status_display()}"
