# Generated by Django 4.2.6 on 2023-11-05 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(blank=True, choices=[('A', 'Admin'), ('O', 'Organizer'), ('At', 'Attendee')], default=('At', 'Attendee'), max_length=2, null=True),
        ),
    ]
