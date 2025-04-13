from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_faculty', 'signup_link')

    def signup_link(self, obj):
        url = reverse('faculty_signup')
        return format_html(f'<a class="button" href="{url}">Register New Faculty</a>')

    signup_link.short_description = 'Faculty Signup'
    signup_link.allow_tags = True