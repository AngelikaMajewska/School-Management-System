from django.urls import path, include

from teacher.views import ( ClassroomListView, ClassroomDetailView, GradeCreateView,
                            ScheduleCreateView, MyScheduleListView)

urlpatterns = [
    path("classrooms/", ClassroomListView.as_view(), name="classrooms"),
    path("classrooms/<int:pk>/", ClassroomDetailView.as_view(), name="classroom-details"),
    # path('grade/', GradeCreateView.as_view(), name='grade'),
    path('schedule/', ScheduleCreateView.as_view(), name='schedule'),
    path('my-schedule/<int:teacher_id>/', MyScheduleListView.as_view(), name='my-schedule'),
                 #   muszę utworzyć bazę danych z użytkownikami w Django Admin, żeby mieć user.id
]