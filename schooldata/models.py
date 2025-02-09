from distutils.command.check import check

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CheckConstraint, Index, Q, Sum, F
from datetime import datetime, timedelta

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    expected_graduation = models.IntegerField()

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            Index(fields=['id','last_name']),
        ]

    def average_for_subject(self, subject):
        grades = Grade.objects.filter(student=self, subject=subject).aggregate(
            total_weighted=Sum(F('grade') * F('weight')),
            total_weight=Sum('weight')
        )
        if grades['total_weight']:
            weighted_average = round(grades['total_weighted'] / grades['total_weight'], 2)
        else:
            weighted_average = 0.00
        return weighted_average

    def update_gpa(self):
        subjects = Grade.objects.filter(student=self).values_list('subject', flat=True).distinct()
        if not subjects:
            self.gpa = 0.00
        else:
            subject_averages = [self.average_for_subject(subject) for subject in subjects]
            self.gpa = round(sum(subject_averages) / len(subject_averages), 2)
        self.save(update_fields=['gpa'])

    def __str__(self):
        return f"{self.first_name} {self.last_name}, class of: {self.expected_graduation}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=32,null=False, blank=False)
    last_name = models.CharField(max_length=32,null=False, blank=False)
    hired = models.DateField(null=False, blank=False)
    qualifications = models.TextField(null=False, blank=False)
    subjects = models.ManyToManyField("Subject", related_name="teachers_of_subject")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


LEVELS = [
    (0, 'Unknown'),
    (1, 'Introduction'),
    (2, 'Foundation'),
    (3, 'Advanced'),
    (4, 'Extracurricular')
]

class Subject(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    level = models.IntegerField(choices=LEVELS, default=0)
    description = models.TextField(null=False, blank=False)
    students = models.ManyToManyField(Student, related_name="subjects")
    teachers = models.ManyToManyField(Teacher, related_name="subjects_taught")
    regular = models.BooleanField(default=True)

    class Meta:
        unique_together = ('name', 'level')
        ordering = ['name', '-level']

    def __str__(self):
        level_name = dict(LEVELS).get(self.level)
        return f"{self.name}, {level_name}"

LAB = [
    (0, 'Unknown'),
    (1, 'No'),
    (2, 'Biology'),
    (3, 'Chemistry'),
    (4, 'Physics'),
    (5, 'Geography'),
    (5, 'Mathematics'),
    (6, 'Visual arts'),
    (7, 'Music'),
    (8, 'Other'),
]

class ClassRoom(models.Model):
    room_number = models.IntegerField(primary_key=True,null=False, blank=False, unique=True)
    seats = models.IntegerField(null=False, blank=False)
    beamer = models.BooleanField(default=False)
    lab = models.IntegerField(choices=LAB, default=0)

    class Meta:
        ordering = ['room_number']
        constraints = [
            CheckConstraint(check=Q(seats__gt=0), name='seats_gt_zero'),
        ]
        indexes = [
            Index(fields=['room_number']),
        ]

    def __str__(self):
        lab_name = dict(LAB).get(self.lab)
        return f"Classroom {self.room_number}, Lab: {lab_name}"

class Schedule(models.Model):
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    duration = models.DurationField(null=False, blank=False)
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('class_room', 'date','time')
        ordering = ['class_room', '-date', 'time']
        indexes = [
            Index(fields=['class_room', 'date']),
        ]
        constraints = [
            CheckConstraint(
                check=Q(duration__gte=timedelta(minutes=0)) & Q(duration__lte=timedelta(minutes=180)),
                name='duration_within_range'
            )
        ]

    def save(self, *args, **kwargs):
        start_datetime = datetime.combine(self.date, self.time)
        end_datetime = start_datetime + self.duration
        self.end_time = end_datetime.time()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_room.room_number}, {self.date} {self.time}-{self.end_time}, {self.teacher}"

WEIGHTS = [
    (0, 'Unknown'),
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High'),
]

GRADES = [
    (0, 'Unknown'),
    (1, 'D'),
    (2, 'C'),
    (3, 'B'),
    (4, 'A'),
]

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.IntegerField(choices=GRADES, default=0)
    weight = models.IntegerField(choices=WEIGHTS, default=0)
    date_given = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            Index(fields=['subject']),
        ]
        ordering = ['subject', 'teacher','student']
        # permissions = [
        #     ("add_new_grade", "Can add a grade"),
        #     # other permissions
        # ]

    def __str__(self):
        grade_name = dict(GRADES).get(self.grade)
        weight_name = dict(WEIGHTS).get(self.weight)
        return f"{self.subject.name}, {self.student} - grade: {grade_name}, weight: {weight_name}"

class Annotations(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    note = models.TextField(default='')
    date = models.DateField(auto_now_add=True)
    # later to add created_by

    class Meta:
        indexes = [
            Index(fields=['student']),
        ]
        ordering = ['-student']

    def __str__(self):
        return f"Note {self.id} - {self.student}"
