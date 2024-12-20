# Generated by Django 5.0.1 on 2024-11-12 01:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessments', '0008_assessment_weights_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentFinalScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('final_score_ass', models.FloatField(default=0)),
                ('final_score_quiz', models.FloatField(default=0)),
                ('final_score', models.FloatField(default=0)),
                ('average_score', models.FloatField(default=0, verbose_name='Average Score')),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessments.assessment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student Assessment Score',
                'verbose_name_plural': 'Student Assessment Score',
                'db_table': 'student_assessment_score',
            },
        ),
    ]
