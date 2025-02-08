from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

from .views import (TeacherListView, TeacherDetailView, SubjectListView, SubjectDetailView)

urlpatterns = [
    path("teachers/", TeacherListView.as_view(), name="teachers"),
    path("teachers/<int:pk>/", TeacherDetailView.as_view(), name="teacher-details"),
    path("subjects/", SubjectListView.as_view(), name="subjects"),
    path("subjects/<int:pk>/", SubjectDetailView.as_view(), name="subjects-details"),
]
