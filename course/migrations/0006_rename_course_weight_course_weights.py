# Generated by Django 5.0.1 on 2024-11-12 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_course_course_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course_weight',
            new_name='weights',
        ),
    ]
