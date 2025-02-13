# marks_allocation_using_geminie
# Marks Prediction Project with Gemini API Integration (Python)

## 1. **Project Overview**
This project uses the Gemini API via LangChain to evaluate student answers and assign marks based on similarity and correctness.

---

## 2. **Prerequisites**
- Python 3.x
- IDE (VS Code, PyCharm, Jupyter Notebook)
- Internet connection

---

## 3. **Required Libraries**
Install the following libraries using pip:
```bash
pip install langchain langchain-google-genai google-generativeai
```

---

## 4. **Project Structure**
```
marks_prediction_project/
│
├── main.py               # Main script with evaluation logic
├── requirements.txt      # List of required libraries
└── README.md             # Project documentation
```

---

## 5. **Setup Instructions**
### a. Clone the Repository
```bash
git clone <repository-url>
cd marks_prediction_project
```
### b. Create and Activate Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # On Mac/Linux
venv\Scripts\activate       # On Windows
```
### c. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 6. **Code Implementation**
### main.py
```python
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
```

---

## 7. **Configuration**
- Replace `YOUR_GEMINI_API_KEY` with your Gemini API key.

---

## 8. **Output Example**
```
Question: what is Object Oriented Programming in C++?
Enter your answer: <student answer>

Evaluating your answer...

Evaluation Result:
Score (out of 10): 8
Feedback:
The answer is well-structured and covers key OOP concepts like encapsulation and inheritance, but lacks examples.
```

---

## 9. **Additional Notes**
- Ensure API key is valid.
- Virtual environment activation is recommended.

---

## 10. **Conclusion**
This project integrates Gemini API for accurate and automated student answer evaluations in Python using LangChain.

![image](https://github.com/user-attachments/assets/2be648de-628d-49b7-8e2c-107c87e62add)
