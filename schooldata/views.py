from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Schedule, Subject, Teacher

class HomepageView(TemplateView):
    template_name = "schooldata/homepage.html"


class TeacherListView(ListView):
    model = Teacher
    template_name = "schooldata/teacher_list.html"
    context_object_name = "teachers"
    paginate_by = 30

class TeacherDetailView(DetailView):
    model = Teacher
    template_name = "schooldata/teacher_detail.html"
    context_object_name = "teacher"

    def get_queryset(self):
        return Teacher.objects.prefetch_related("subjects_taught")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teacher = self.object
        context['subjects'] = teacher.subjects_taught.all()
        context['schedules'] = (Schedule.objects.filter(teacher=teacher).select_related("class_room", "subject").order_by("date"))
        return context

class SubjectListView(ListView):
    model = Subject
    template_name = "schooldata/subject_list.html"
    context_object_name = "subjects"
    paginate_by = 30

class SubjectDetailView(DetailView):
    model = Subject
    template_name = "schooldata/subject_detail.html"
    context_object_name = "subject"

    def get_queryset(self):
        return Subject.objects.prefetch_related("students", "teachers")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.object

        context['teachers'] = subject.teachers.values("id", "first_name", "last_name")

        context['students'] = subject.students.values("id", "first_name", "last_name")

        context['schedules'] = (
            Schedule.objects.filter(subject=subject)
            .select_related("teacher", "class_room").order_by('date')
        )
        return context


class ScheduleListView(PermissionRequiredMixin,ListView):
    model = Schedule
    template_name = "schooldata/schedule_list.html"
    context_object_name = "schedules"
    paginate_by = 30

    permission_required = 'schooldata.view_schedule'


