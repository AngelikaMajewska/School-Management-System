# Generated by Django 5.1.5 on 2025-02-03 14:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("schooldata", "0002_remove_student_expected_graduation_not_in_past"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="student",
            name="dob_in_past",
        ),
    ]
