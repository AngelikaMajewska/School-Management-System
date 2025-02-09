from django.contrib import admin

# Register your models here.
from .models import ClassRoom, Teacher, Subject, Student, Schedule

# Dodanie wszystkich modeli do panelu admina
admin.site.register(ClassRoom)
admin.site.register(Subject)
admin.site.register(Schedule)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name','date_of_birth','gpa', 'expected_graduation')
    # fields = ('first_name', 'last_name', 'expected_graduation')
    # exclude = ('gpa',)
    readonly_fields = ('gpa', 'date_of_birth')
    fieldsets = (
        ('Personal data', {'fields': ('first_name', 'last_name', 'date_of_birth')}),
        ('Education', {'fields': ('gpa', 'expected_graduation')}),
    )
    list_filter = ('expected_graduation', 'gpa')
    search_fields = ('first_name', 'last_name')
    # list_display = ('first_name', 'last_name', 'gpa', 'expected_graduation')
    # list_editable = ('last_name',)
    ordering = ('last_name', 'first_name')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'hired')
    fieldsets = (
        ('Personal data', {'fields': ('first_name', 'last_name')}),
        ('Qualifications', {'fields': ('hired','qualifications')}),
    )
    readonly_fields = ('hired',)
    ordering = ('last_name', 'first_name')