# Generated by Django 5.1.6 on 2025-03-05 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('test_evaluation', '0002_delete_studentanswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100)),
                ('roll_no', models.CharField(max_length=20, unique=True)),
                ('paper_name', models.CharField(default='Computer Science', editable=False, max_length=100)),
                ('paper_code', models.CharField(default='CS101', editable=False, max_length=20)),
                ('question', models.TextField()),
                ('marks', models.FloatField(default=0.0)),
                ('feedback', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
