# Generated by Django 5.1.2 on 2025-01-11 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_car_rental_delete_choice_delete_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
