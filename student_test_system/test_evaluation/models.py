from django.db import models

class StudentAnswer(models.Model):
    roll_no = models.CharField(max_length=10, unique=True)
    question = models.TextField()
    answer = models.TextField()
    marks = models.IntegerField(default=0)
    feedback = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.roll_no} - {self.question[:30]}"