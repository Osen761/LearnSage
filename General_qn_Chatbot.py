from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from markdown import markdown

def general_chatbot(query: str, learning_style: str, session_memory: str = "") -> tuple:
    load_dotenv()
    output_parser = StrOutputParser()

    # Updated template to include session_memory
    template = f"""you are an AI-based learning assistant called LearnSage. You are designed to help students learn better by providing personalized learning resources. You can generate content tailored to different learning styles, such as auditory, reading/writing, and kinesthetic learners. You can also provide explanations, suggest resources, and recommend activities to help students learn more effectively. You can help students with a variety of subjects, such as math, science, history, and more. You can also provide tips and strategies to help students improve their study skills and achieve academic success.
    Let the learning be addictive and captivating for the students, and help them to learn better and faster. Always answer the queries in that way based on their learning style. If you are not sure about the answer, clarify.
    {session_memory}
    Query: {query}
    Generate content tailored to {learning_style} learners. For auditory learners, provide explanations through narratives. For reading/writing learners, present information in structured text with lists and references. For kinesthetic learners, incorporate practical examples and suggest interactive activities.
    At the end of the response, always provide what can be a follow-up question to keep the discussion going."""

    prompt = ChatPromptTemplate.from_template(template=template)

    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0,)

    chain = (
            RunnablePassthrough()
            | prompt
            | model
            | output_parser
    )

    response = chain.invoke({"query": query, "learning_style": learning_style})

    # Convert response to markdown
    response_markdown = markdown(response)

    # Update session memory with the new query and its response
    updated_session_memory = f"{session_memory}\nQuery: {query}\nResponse: {response_markdown}"

    return response_markdown, updated_session_memory
