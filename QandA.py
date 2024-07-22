
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Define prompts
Qn_prompt = ChatPromptTemplate.from_template(
    """you are an AI-based learning assistant called LearnSage. You are designed to help students learn better by providing personalized learning resources.
       Generate questions based on the given text.
       Text: {text}
       Format: {format}"""
)

Ans_prompt = ChatPromptTemplate.from_template(
    """you are an AI-based learning assistant called LearnSage. You are designed to help students learn better by providing personalized learning resources.
       This is a Q&A. Answer the question in this format {format} based on the given context.
       Text: {text}"""
)

# Initialize model
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro" ,temperature=0)

# Define chains
Qn_chain = Qn_prompt | model | StrOutputParser()
Ans_chain = Ans_prompt | model | StrOutputParser()

# Function to generate questions
def generate_questions(text: str, format: str) -> list:
    response = Qn_chain.invoke({"text": text, "format": format})
    return response.split("\n")

# Function to answer questions
def answer_questions(text: str, format: str) -> str:
    response = Ans_chain.invoke({"text": text, "format": format})
    return response

# Function to generate and answer questions
def generate_and_answer(text: str, question_format: str, answer_format: str) -> str:
    # Generate questions based on the given text
    questions = generate_questions(text, question_format)
    
    # Combine the original text with the generated questions
    combined_text = f"{text}\n\n{' '.join(questions)}"
    
    # Call answer_questions with the combined text
    answers = answer_questions(combined_text, answer_format)
    
    return answers
