# Generated by Django 5.0.1 on 2024-11-14 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievement', '0009_alter_performanceanalytics_completion_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='performanceanalytics',
            old_name='score',
            new_name='average_score',
        ),
    ]