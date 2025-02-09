from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Grade, Student, Teacher

@receiver(post_save, sender=Grade)
def update_gpa_after_save(sender, instance, **kwargs):
    student = instance.student
    student.update_gpa()

@receiver(post_delete, sender=Grade)
def update_gpa_after_delete(sender, instance, **kwargs):
    student = instance.student
    student.update_gpa()

@receiver(post_save, sender=Teacher)
def add_teacher_profile(sender, instance, created, **kwargs):
    if created:  # Wykonujemy kod tylko, jeśli obiekt Teacher został stworzony, a nie za każdym razem, gdy jest edytowany
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')  # Tworzy grupę, jeśli nie istnieje

        # Sprawdzenie, czy użytkownik już istnieje
        if not instance.user:  # Zakładam, że Teacher ma pole user = OneToOneField(User)
            username = f"{instance.first_name.lower()}_{instance.last_name.lower()}"
            if User.objects.filter(username=username).exists():
                username = f"{username}_{instance.id}"  # Zapobiega konfliktowi nazw

            user = User.objects.create(
                username=username,
                first_name=instance.first_name,
                last_name=instance.last_name
            )
            user.set_password("coderslab")  # Ustawienie domyślnego hasła
            user.groups.add(teacher_group)
            user.save()

            # Przypisanie użytkownika do nauczyciela
            instance.user = user
            instance.save()

@receiver(post_save, sender=Student)
def add_student_profile(sender, instance, created, **kwargs):
    # print(f"SIGNAL TRIGGERED: created={created}, instance={instance}")
    if created:
        student_group, _ = Group.objects.get_or_create(name='Student')

        if not instance.user:
            username = f"{instance.first_name.lower()}_{instance.last_name.lower()}"
            if User.objects.filter(username=username).exists():
                username = f"{username}_{instance.id}"

            user = User.objects.create(
                username=username,
                first_name=instance.first_name,
                last_name=instance.last_name
            )
            user.set_password("coderslab")
            user.groups.add(student_group)
            user.save()
            instance.user = user
            instance.save()