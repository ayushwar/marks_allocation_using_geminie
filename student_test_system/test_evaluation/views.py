from rest_framework import viewsets
from .models import StudentAnswer
from .serializers import StudentAnswerSerializer
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Initialize Gemini API
llm = GoogleGenerativeAI(model="gemini-pro", api_key="YOUR_API_KEY")

# Define evaluation prompt
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

# Create an evaluation chain
evaluation_chain = LLMChain(llm=llm, prompt=evaluation_prompt)

# Define API view for StudentAnswer
class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer

# API to evaluate student's answer
@api_view(['POST'])
def evaluate_answer(request, roll_no):
    student_answer = get_object_or_404(StudentAnswer, roll_no=roll_no)
    evaluation_result = evaluation_chain.invoke({
        "question": student_answer.question,
        "student_answer": student_answer.answer
    })
    
    # Extract marks and feedback
    student_answer.marks = int(evaluation_result.get("text", "5").split("\n")[0])
    student_answer.feedback = evaluation_result.get("text", "Needs improvement.")
    student_answer.save()
    
    return Response({"marks": student_answer.marks, "feedback": student_answer.feedback})

# ✅ Add the missing function `student_results`
@api_view(['GET'])
def student_results(request, roll_no):
    """
    This API retrieves the marks and feedback for a student based on roll number.
    """
    student_answer = get_object_or_404(StudentAnswer, roll_no=roll_no)
    return Response({
        "roll_no": student_answer.roll_no,
        "question": student_answer.question,
        "answer": student_answer.answer,
        "marks": student_answer.marks,
        "feedback": student_answer.feedback
    })
