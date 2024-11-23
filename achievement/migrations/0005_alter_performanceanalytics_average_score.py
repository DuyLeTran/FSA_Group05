# Generated by Django 5.0.1 on 2024-11-14 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievement', '0004_alter_performanceanalytics_average_score'),
        ('assessments', '0019_coursefinalscore_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performanceanalytics',
            name='average_score',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessments.coursefinalscore'),
        ),
    ]