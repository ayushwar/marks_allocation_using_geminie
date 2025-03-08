from django.contrib import admin
from .models import StudentExam
from .models import EligibleStudent

admin.site.register(EligibleStudent)

@admin.register(StudentExam)
class StudentExamAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'roll_no', 'marks')
    search_fields = ('student_name', 'roll_no')
    readonly_fields = ('paper_name', 'paper_code')  # Make them read-only

