from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Grade

@receiver(post_save, sender=Grade)
def update_gpa_after_save(sender, instance, **kwargs):
    student = instance.student
    student.update_gpa()

@receiver(post_delete, sender=Grade)
def update_gpa_after_delete(sender, instance, **kwargs):
    student = instance.student
    student.update_gpa()