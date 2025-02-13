from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = GoogleGenerativeAI(model="gemini-pro", api_key="YOUR_GEMINI_API_KEY")

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

evaluation_chain = LLMChain(llm=llm, prompt=evaluation_prompt)

def evaluate_student_answer(question, student_answer):
    evaluation_result = evaluation_chain.invoke({
        "question": question,
        "student_answer": student_answer
    })
    return evaluation_result["text"]

if __name__ == "__main__":
    question = "what is Object Oriented Programming in C++?"
    student_answer = input("Enter your answer: ")
    print("\nEvaluating your answer...\n")
    result = evaluate_student_answer(question, student_answer)
    print("Evaluation Result:")
    print(result)
