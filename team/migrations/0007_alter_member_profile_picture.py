# Generated by Django 5.1.1 on 2024-11-02 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0006_alter_member_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default-profile.png', upload_to='profile_pictures/'),
        ),
    ]