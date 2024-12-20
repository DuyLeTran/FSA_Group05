# Generated by Django 5.0.1 on 2024-11-21 03:51

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_remove_course_weights'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='discount',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='date_unenrolled',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='coursematerial',
            name='material_type',
            field=models.CharField(choices=[('assignments', 'Assignments'), ('labs', 'Labs'), ('lectures', 'Lectures'), ('references', 'References'), ('assessments', 'Assessments')], max_length=20),
        ),
        migrations.CreateModel(
            name='MaterialViewingDuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('time_spent', models.DurationField(default=datetime.timedelta)),
                ('come_back', models.PositiveIntegerField(default=0)),
                ('material', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='duration', to='course.coursematerial')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='duration', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_successful', models.BooleanField(default=False)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='course.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'course')},
            },
        ),
    ]
