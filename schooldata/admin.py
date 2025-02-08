from django.contrib import admin

# Register your models here.
from .models import ClassRoom, Teacher, Subject, Student, Schedule

# Dodanie wszystkich modeli do panelu admina
admin.site.register(ClassRoom)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Schedule)