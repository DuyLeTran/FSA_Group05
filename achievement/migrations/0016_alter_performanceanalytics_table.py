# Generated by Django 5.0.1 on 2024-11-14 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('achievement', '0015_remove_performanceanalytics_average_score_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='performanceanalytics',
            table='achievement_performance',
        ),
    ]
