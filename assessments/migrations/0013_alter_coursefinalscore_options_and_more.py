# Generated by Django 5.0.1 on 2024-11-12 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0012_alter_studentassessmentattempt_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursefinalscore',
            options={'verbose_name': 'Course Final Score', 'verbose_name_plural': 'Course Final Scores'},
        ),
        migrations.AlterModelTable(
            name='coursefinalscore',
            table='course_final_score',
        ),
    ]