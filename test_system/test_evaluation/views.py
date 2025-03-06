from django.shortcuts import render
from rest_framework import viewsets
from .models import StudentExam
from .serializers import StudentAnswerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.runnable import RunnableSequence
from .models import StudentExam

from django.urls import get_resolver
from django.http import JsonResponse


class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentExam.objects.all()
    serializer_class = StudentAnswerSerializer


# Initialize Google Gemini API
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", api_key="")

# Define a prompt template for evaluating the answer
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

# ✅ Use RunnableSequence Instead of LLMChain
evaluation_chain = (
    RunnablePassthrough()
    | evaluation_prompt
    | llm
)


# Define the evaluation chain
evaluation_chain = RunnablePassthrough() | evaluation_prompt | llm

# Function to evaluate student answers using Gemini AI
def evaluate_student_answer(question, student_answer):
    evaluation_result = evaluation_chain.invoke({
        "question": question,
        "student_answer": student_answer
    })

    # Print raw response for debugging
    print("Raw Evaluation Response:", evaluation_result)

    # Handle different response formats
    if isinstance(evaluation_result, dict):
        return evaluation_result.get("text", "No text response from Gemini AI")
    elif isinstance(evaluation_result, str):
        return evaluation_result  # Return as is if response is a string
    else:
        return "Error: Unexpected response format from Gemini AI"

@api_view(['GET'])
def analyze_student_answers(request):
    """
    Fetches student answers, evaluates them using Gemini AI, and returns marks & feedback.
    """
    student_answers = StudentExam.objects.all()  # Fetch all answers

    if not student_answers.exists():
        return Response({"error": "No student answers found!"}, status=404)

    results = []

    for answer in student_answers:
        # Ensure correct field name is used
        evaluation = evaluate_student_answer(answer.question, answer.student_answer)  
        
        results.append({
            "student_name": answer.student_name,
            "question": answer.question,
            "answer": answer.student_answer,
            "evaluation": evaluation  # AI-generated score & feedback
        })

    return Response({"results": results})



# from google.generativeai import configure, list_models

# configure(api_key="AIzaSyDS99c8Ycr8razMXQJv4aOK_a_U6jIU3Ks")

# models = list_models()
# for model in models:
#     print(model.name, "supports:", model.supported_generation_methods)
