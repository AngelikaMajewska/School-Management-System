# Generated by Django 5.1.5 on 2025-02-08 18:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schooldata", "0012_alter_teacher_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="student",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
