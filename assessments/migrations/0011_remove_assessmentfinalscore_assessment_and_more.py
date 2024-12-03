# Generated by Django 5.0.1 on 2024-11-12 03:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0010_alter_studentassessmentattempt_ass_weights_and_more'),
        ('course', '0004_alter_enrollment_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessmentfinalscore',
            name='assessment',
        ),
        migrations.AddField(
            model_name='assessmentfinalscore',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course', verbose_name='Course'),
        ),
    ]