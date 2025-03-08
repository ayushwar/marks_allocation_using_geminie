from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import StudentExam
from .serializers import StudentAnswerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough, RunnableSequence
from .forms import StudentLoginForm, AnswerForm
import re
from django.urls import reverse
from .models import StudentExam, EligibleStudent

class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentExam.objects.all()
    serializer_class = StudentAnswerSerializer

# Initialize Google Gemini API
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", api_key="")

evaluation_prompt = PromptTemplate(
    input_variables=["question", "student_answer"],
    template="""
    You are a teacher evaluating a student's answer. Your task is to grade the answer based on its accuracy, completeness, and clarity.

    Question: {question}
    Student's Answer: {student_answer}

    Evaluate the answer and provide a score out of 10. Also, give brief feedback explaining the score.

    Score (out of 10): 
    Feedback:
    """
)

evaluation_chain = RunnableSequence(
    RunnablePassthrough() | evaluation_prompt | llm
)

def evaluate_student_answer(question, student_answer):
    evaluation_result = evaluation_chain.invoke({
        "question": question,
        "student_answer": student_answer
    })
    
    print("Raw Evaluation Response:", evaluation_result)
    
    if isinstance(evaluation_result, dict):
        return evaluation_result.get("text", "No response from AI")
    elif isinstance(evaluation_result, str):
        return evaluation_result
    else:
        return "Error: Unexpected AI response format"
    
    # ✅ Extract numeric score from evaluation text
    marks = extract_marks(evaluation_text)

    return evaluation_text, marks  # Return both feedback and marks

@api_view(['GET'])
def analyze_student_answers(request):
    student_answers = StudentExam.objects.all()
    
    if not student_answers.exists():
        return Response({"error": "No student answers found!"}, status=404)

    results = []
    for answer in student_answers:
        # ✅ Get AI evaluation
        evaluation = evaluate_student_answer(answer.question, answer.student_answer)

        # ✅ Extract marks from AI response
        score = extract_marks(evaluation)

        # ✅ Update the database with AI-generated marks
        answer.marks = score
        answer.save()
        
        results.append({
            "student_name": answer.student_name,
            "question": answer.question,
            "answer": answer.student_answer,
            "evaluation": evaluation
        })

    return Response({"results": results})

def student_login(request):
    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student_name = form.cleaned_data['student_name']
            roll_no = form.cleaned_data['roll_no']

            # Ensure marks has a default value
            student, created = StudentExam.objects.get_or_create(
                roll_no=roll_no,
                defaults={
                    'student_name': student_name,
                    'question': "What is OOP in C++?",
                    'marks': 0  # ✅ Ensure default marks is set
                }
            )

            return redirect('answer_page', roll_no=student.roll_no)
    else:
        form = StudentLoginForm()

    return render(request, 'test_evaluation/login.html', {'form': form})


# from django.shortcuts import render, get_object_or_404, redirect
# import re

def extract_marks(evaluation_text):
    """
    Extracts numeric marks from AI evaluation response.
    """
    match = re.search(r"Score\s*\(out of\s*10\):\s*(\d+)", evaluation_text)
    if match:
        return int(match.group(1))  # Convert to integer
    return 0  # Default to 0 if no score is found

def answer_page(request, roll_no):

    # ✅ Check if student is eligible
    if not EligibleStudent.objects.filter(roll_no=roll_no).exists():
        return render(request, 'test_evaluation/not_eligible.html', {'roll_no': roll_no})
    student = get_object_or_404(StudentExam, roll_no=roll_no)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=student)
        if form.is_valid():
            student = form.save()

            # ✅ Call AI evaluation function and handle return values
            result = evaluate_student_answer(student.question, student.student_answer)

            if isinstance(result, tuple) and len(result) == 2:
                evaluation, marks = result  # Unpack correctly
            else:
                evaluation = result  # If only one value is returned
                marks = extract_marks(evaluation)  # Extract marks separately

            student.evaluation_result = evaluation
            student.marks = marks  # ✅ Store AI marks in the database
            student.save()

            # ✅ Show success message and redirect to results page
            return render(request, 'test_evaluation/test_submitted.html', {
                'student': student,
                'results_url': reverse('results_page')
            })

    else:
        form = AnswerForm(instance=student)

    return render(request, 'test_evaluation/answer.html', {'student': student, 'form': form})



def results_page(request):
    if request.method == "POST":
        roll_no = request.POST.get("roll_no")
        try:
            student = StudentExam.objects.get(roll_no=roll_no)
            return render(request, 'test_evaluation/results.html', {
                'student': student,
                'evaluation_result': student.evaluation_result  # ✅ Pass AI evaluation to the template
            }) 
        except StudentExam.DoesNotExist:
            return render(request, 'test_evaluation/results_login.html', {'error': "Roll number not found!"})

    return render(request, 'test_evaluation/results_login.html')

# def extract_marks(evaluation_text):
#     """
#     Extracts numeric marks from AI evaluation response.
#     Assumes format: "Score (out of 10): X"
#     """
#     match = re.search(r'Score\s*\(out of\s*10\):\s*(\d+)', evaluation_text)
#     if match:
#         return int(match.group(1))  # Convert extracted score to integer
#     return 0  # Return 0 if score is not found


