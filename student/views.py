from datetime import date, timedelta

from django.db.models import Min
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from schooldata.models import Student, Grade, Schedule


# Create your views here.
class StudentListView(ListView):
    model = Student
    template_name = "student/student_list.html"
    context_object_name = "students"
    paginate_by = 30
    for student in Student.objects.all():
        student.update_gpa()

class StudentDetailView(DetailView): # poprawić tabelę z ocenami na podstawie roku
    model = Student
    template_name = "student/student_detail.html"
    context_object_name = "student"

    # def get_queryset(self):
    #     return (
    #         Student.objects.prefetch_related(
    #             "subjects",
    #             "grade_set__subject"
    #         )
    #     )
    def get_context_data(self, **kwargs):
        today = date.today()
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        subjects = student.subjects.all()
        context['subjects'] = subjects
        context['grades'] = Grade.objects.filter(student=student)
        context['schedules'] = (Schedule.objects.filter(subject__students=student).filter(date__lte=today+timedelta(days=7))
                                .select_related('class_room', 'teacher').order_by('date','time'))

        school_start = date(today.year - 1, 9, 1) if today.month <= 7 else date(today.year, 9, 1)

        # Grupowanie ocen według przedmiotów i lat szkolnych
        grades_by_subject = {
            subject: Grade.objects.filter(
                student=student,
                subject=subject,
                date_given__gte=school_start,
                date_given__lte=today
            ).order_by("date_given")
            for subject in subjects
        }
        context['grades_by_subject'] = grades_by_subject
        return context
