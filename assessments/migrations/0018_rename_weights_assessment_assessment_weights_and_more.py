# Generated by Django 5.0.1 on 2024-11-14 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0017_alter_assessment_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assessment',
            old_name='weights',
            new_name='assessment_weights',
        ),
        migrations.RemoveField(
            model_name='studentassessmentattempt',
            name='ass_weights',
        ),
        migrations.RemoveField(
            model_name='studentassessmentattempt',
            name='quiz_weights',
        ),
        migrations.AddField(
            model_name='assessment',
            name='ass_weights',
            field=models.FloatField(blank=True, default=0.5, null=True),
        ),
        migrations.AddField(
            model_name='assessment',
            name='quiz_weights',
            field=models.FloatField(blank=True, default=0.5, null=True),
        ),
    ]
