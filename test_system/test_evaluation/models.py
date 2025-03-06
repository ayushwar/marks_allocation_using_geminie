# from django.db import models

# class StudentExam(models.Model):
#     # Fixed paper details (only one paper)
#     PAPER_NAME = "Computer Science"
#     PAPER_CODE = "CS101"

#     student_name = models.CharField(max_length=100)
#     roll_no = models.CharField(max_length=20, unique=True)
#     paper_name = models.CharField(max_length=100, default=PAPER_NAME, editable=False)
#     paper_code = models.CharField(max_length=20, default=PAPER_CODE, editable=False)
#     question = models.TextField()
#     marks = models.FloatField(default=0.0)  # Initially set to 0
#     feedback = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.student_name} - {self.roll_no}"



from django.db import models

class StudentExam(models.Model):
    # Fixed paper details (only one paper)
    PAPER_NAME = "Computer Science"
    PAPER_CODE = "CS101"

    student_name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, unique=True)
    paper_name = models.CharField(max_length=100, default=PAPER_NAME, editable=False)
    paper_code = models.CharField(max_length=20, default=PAPER_CODE, editable=False)
    question = models.TextField()
    student_answer = models.TextField(blank=True, null=True)  # Student's answer field
    marks = models.FloatField(default=0.0)  # Initially set to 0
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student_name} - {self.roll_no}"

