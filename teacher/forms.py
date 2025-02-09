from datetime import timedelta

from django import forms

from schooldata.models import Grade, Subject, Student, Schedule

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'grade', 'weight','teacher']

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'teacher', 'class_room', 'date','time','end_time','recurring','end_date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'recurring': forms.CheckboxInput(attrs={'type': 'checkbox'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if instance.recurring:
            start_date = instance.date
            end_date = instance.end_date  # Zmienna, która powinna zawierać datę zakończenia (możesz dodać do formularza pole końcowej daty)
            if not end_date:
                raise ValueError("Please specify the end date for recurring schedules.")
            current_date = start_date
            while current_date <= end_date:
                new_schedule = Schedule(
                    class_room=instance.class_room,
                    teacher=instance.teacher,
                    subject=instance.subject,
                    date=current_date,
                    time=instance.time,
                    end_time=instance.end_time,
                    recurring=False  # Ustawiamy to jako pojedynczy zapis, nie powtarzający się
                )
                new_schedule.save()
                current_date += timedelta(weeks=1)
            return new_schedule
        else:
            if commit:
                instance.save()
            return instance