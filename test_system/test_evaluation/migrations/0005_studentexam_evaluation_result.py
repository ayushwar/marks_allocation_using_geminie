# Generated by Django 5.1.6 on 2025-03-06 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_evaluation', '0004_studentexam_student_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentexam',
            name='evaluation_result',
            field=models.TextField(blank=True, null=True),
        ),
    ]
