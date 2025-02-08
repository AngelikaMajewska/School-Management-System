from datetime import timedelta

from django import forms

from schooldata.models import Grade, Subject, Student, Schedule

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'grade', 'weight','teacher']

    # def save(self, commit=True):
    #     instance = super().save(commit=False)  # Tworzymy obiekt, ale jeszcze nie zapisujemy
    #     teacher_id = self.cleaned_data['teacher'].id  # Pobieramy ID nauczyciela
    #     instance.teacher_id = teacher_id  # Przypisujemy ID nauczyciela do obiektu
    #     if commit:
    #         instance.save()
    #     return instance

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['subject', 'teacher', 'class_room', 'date','time', 'duration']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'duration': forms.NumberInput(attrs={'type': 'number', 'step': '15', 'min': '15', 'max': '180','value': '15'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        duration = int(self.data.get('duration'))
        if duration > 59:
            hours = duration/60
            minutes = duration%60
            cleaned_data['duration'] = timedelta(hours=hours, minutes=minutes)
        else:
            minutes = duration % 60
            cleaned_data['duration'] = timedelta(minutes=minutes)
        return cleaned_data