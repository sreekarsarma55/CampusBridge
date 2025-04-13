from django.contrib import admin
from .models import Course, Chapter, Material, Assignment, Attendance

# Register your models for admin panel

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']  # removed 'material_type'
    # list_filter = ['material_type']  # comment or delete this line


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date')
    list_filter = ('course',)


class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'date')
    list_filter = ('course', 'status', 'date')
    search_fields = ('student__username', 'course__title')

admin.site.register(Attendance, AttendanceAdmin)