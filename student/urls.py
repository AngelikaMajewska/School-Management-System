from django.urls import path
from student.views import StudentListView, StudentDetailView


urlpatterns = [
    path("", StudentListView.as_view(), name="students"),
    path("<int:pk>/", StudentDetailView.as_view(), name="student-details"),
]