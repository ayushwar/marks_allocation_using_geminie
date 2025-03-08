from django import forms
from .models import StudentExam

class StudentLoginForm(forms.Form):
    student_name = forms.CharField(label="Student Name", max_length=100)
    roll_no = forms.CharField(label="Roll Number", max_length=20)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = StudentExam
        fields = ['student_answer']
