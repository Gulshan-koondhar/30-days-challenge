import asyncio
import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from agents import Agent, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
# from openai_agents import OpenAIAgentFactory
# from openai_agents.tools import tool

# Load environment variables
load_dotenv()

# Set up the Gemini API key
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")


def extract_pdf_text_func(file_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_path: The path to the PDF file.

    Returns:
        The extracted text.
    """
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text
extract_pdf_text = function_tool(extract_pdf_text_func)
@function_tool
def generate_quiz(text: str) -> str:
    """
    Generates a quiz from the given text.

    Args:
        text: The text to generate the quiz from.

    Returns:
        The generated quiz.
    """
    return text  # Placeholder for quiz generation


# Configure the agent
external_Client = AsyncOpenAI(
  api_key=os.getenv("GEMINI_API_KEY"),
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client=external_Client
)
agent = Agent(
    name="StudyNotesAgent",
    model=model,
    tools=[extract_pdf_text, generate_quiz],
    instructions="You are a Study Notes Assistant. First summarize the provided PDF content, then generate a quiz based on it.",
)

st.title("PDF Study Notes Assistant")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text from the PDF
    extracted_text = extract_pdf_text_func("temp.pdf")

    # Display the summary
    st.header("Summary")
    summary = asyncio.run(Runner.run(agent,f"Summarize the following text:\n{extracted_text}"))
    st.write(summary.final_output)

    # Create a quiz
    if st.button("Create Quiz"):
        st.header("Quiz")
        quiz = asyncio.run(Runner.run(agent, f"Generate a quiz from the following text:\n{extracted_text}"))
        st.write(quiz.final_output)
