import os
import streamlit as st
import tempfile
import asyncio
from pypdf import PdfReader
from dotenv import load_dotenv
from agents import function_tool, Agent, ModelSettings, Runner
from agents import AsyncOpenAI
from agents import set_default_openai_client, set_default_openai_api, set_tracing_disabled

# Load environment variables from .env file
load_dotenv()

# Retrieve Gemini API key from environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Define Gemini Base URL
gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Create a custom AsyncOpenAI client for Gemini
custom_openai_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=gemini_base_url,
)

# Set the custom client as the default for openai-agents
set_default_openai_client(custom_openai_client)

# Set the default OpenAI API to chat_completions
set_default_openai_api("chat_completions")

# Disable tracing to avoid potential errors if an OpenAI API key is not available for tracing
set_tracing_disabled(True)

def _extract_pdf_text_raw(file_path: str) -> str:
    """
    Raw function to extract all text from a PDF file.

    Args:
        file_path: The path to the PDF file.

    Returns:
        The extracted plain raw text from the PDF.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@function_tool
def extract_pdf_text(file_path: str) -> str:
    """
    Extracts all text from a PDF file for the agent.

    Args:
        file_path: The path to the PDF file.

    Returns:
        The extracted plain raw text from the PDF.
    """
    return _extract_pdf_text_raw(file_path)


@function_tool
def generate_quiz(text: str) -> str:
    """
    Generates a quiz (MCQs or mixed format) based on the provided text.

    Args:
        text: The text content to generate the quiz from.

    Returns:
        A string representing the generated quiz.
    """
    # The actual quiz generation will be handled by the agent later.
    return "Quiz generated based on the provided text."


async def run_agent(agent, prompt):
    result = await Runner.run(agent, prompt)
    return result.final_output

def main():
    st.set_page_config(page_title="Study Notes Assistant", layout="wide")
    st.title("📚 Study Notes Assistant")

    # Debugging: Print the API key to ensure it's loaded
    st.write(f"API Key loaded: {'YES' if os.getenv('GEMINI_API_KEY') else 'NO'}")

    # Agent Configuration
    agent = Agent(
        name="Study Notes Assistant",
        instructions="You are a Study Notes Assistant. First summarize the provided PDF content, then generate a quiz based on it.",
        tools=[extract_pdf_text, generate_quiz],
        model="gemini-2.0-flash",
        model_settings=ModelSettings(
            base_url=gemini_base_url,
        ),
    )

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        st.success(f"File uploaded: {uploaded_file.name}")

        # Extract text
        with st.spinner("Extracting text from PDF..."):
            extracted_text = _extract_pdf_text_raw(tmp_file_path)
            st.session_state["extracted_text"] = extracted_text

        st.subheader("Extracted Text (Summary Placeholder)")
        st.text_area("", extracted_text[:1000] + ("..." if len(extracted_text) > 1000 else ""), height=200, disabled=True)

        if st.button("Create Quiz"):
            if "extracted_text" in st.session_state:
                with st.spinner("Generating quiz..."):
                    quiz_prompt = f"Based on the following text, create a quiz (MCQs or mixed format):\n\n{st.session_state['extracted_text']}"
                    
                    # Run the agent asynchronously
                    quiz_result = asyncio.run(run_agent(agent, quiz_prompt))
                    st.subheader("Generated Quiz")
                    st.write(quiz_result)
            else:
                st.warning("Please upload a PDF and extract text first.")


if __name__ == "__main__":
    main()
