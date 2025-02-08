from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView

from schooldata.models import Grade, ClassRoom, Schedule
from .forms import GradeForm, ScheduleForm



# Create your views here.

class ClassroomListView(PermissionRequiredMixin,ListView):
    model = ClassRoom
    template_name = "teacher/classroom_list.html"
    context_object_name = "classrooms"
    paginate_by = 30

    permission_required = "schooldata.view_classroom"  # Poprawna nazwa uprawnienia

    # Automatyczne przekierowanie na login, jeśli użytkownik nie ma dostępu
    login_url = "/login/"
    redirect_field_name = "next"

class ClassroomDetailView(DetailView):
    model = ClassRoom
    template_name = "teacher/classroom_detail.html"
    context_object_name = "classroom"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom = self.get_object()
        context['schedules'] = Schedule.objects.filter(class_room=classroom).select_related('teacher')
        return context


class GradeCreateView(PermissionRequiredMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = "teacher/forms/grade_form.html"

    permission_required = 'schooldata.add_grade'

    def form_valid(self, form):
        form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("student-detail", kwargs={"pk": self.object.student.pk})

class ScheduleCreateView(PermissionRequiredMixin, CreateView):
    model = Schedule
    form_class = ScheduleForm
    template_name = "teacher/forms/schedule_form.html"

    permission_required = 'schooldata.add_schedule'


    def get_success_url(self):
        return reverse_lazy("classrooms")

class MyScheduleListView(PermissionRequiredMixin, ListView):
    # user.id w Django Admin - nie mam użytkowników i ich ID w DA
    model = Schedule
    template_name = "teacher/schedule_list.html"
    context_object_name = "schedules"
    paginate_by = 30
    permission_required = 'schooldata.view_schedule'

    def get_queryset(self):
        teacher_id = self.request.GET.get("teacher_id")  # Pobranie z parametru w URL
        if not teacher_id:
            return Schedule.objects.none()  # Jeśli brak teacher_id, zwracamy pusty queryset

        return Schedule.objects.filter(teacher_id=teacher_id).select_related('class_room', 'subject')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_id'] = self.request.GET.get("teacher_id")
        return context
