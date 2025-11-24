import os
import streamlit as st
import asyncio
from pypdf import PdfReader
from agents import Agent, function_tool, Runner
from dotenv import load_dotenv
import tempfile

load_dotenv()

@function_tool
def extract_pdf_text(file_path: str) -> str:
    """
    Extracts text from a PDF file.

    Args:
        file_path: The path to the PDF file.

    Returns:
        The extracted raw plain text from the PDF.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@function_tool
async def generate_quiz(text: str) -> str:
    """
    Generates a multiple-choice or mixed quiz based on the provided text.

    Args:
        text: The text content from which to generate the quiz.

    Returns:
        A string containing the generated quiz.
    """
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    # Create a temporary agent for quiz generation
    quiz_agent = Agent(
        name="QuizGenerator",
        instructions="You are an expert quiz generator. Create a multiple-choice or mixed quiz based on the provided text.",
        model="gemini-2.0-flash",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=gemini_api_key,
        tools=[] # No tools needed for this internal agent
    )

    quiz_prompt = f"Generate a detailed quiz (mix of MCQs and open-ended questions if possible) from the following text:\n\n{text}\n\nEnsure there are at least 5 questions. Provide answers after the questions."

    quiz_result = await Runner.run(quiz_agent, quiz_prompt)
    return quiz_result.final_output

# Agent Setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

study_agent = Agent(
    name="StudyNotesAssistant",
    instructions="You are a Study Notes Assistant. First produce a summary, then generate a quiz.",
    model="gemini-2.0-flash",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=gemini_api_key,
    tools=[extract_pdf_text, generate_quiz]
)

async def main_async():
    st.set_page_config(page_title="Study Notes & Quiz Generator")
    st.title("📚 Study Notes Assistant")

    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        st.success("PDF uploaded successfully! Processing...")

        try:
            extracted_text = extract_pdf_text(tmp_file_path)
            st.session_state['extracted_text'] = extracted_text

            # Agent for summary only initially
            summary_agent_instructions = "You are a Study Notes Assistant. Produce a concise summary of the provided text."
            summary_agent = Agent(
                name="SummaryGenerator",
                instructions=summary_agent_instructions,
                model="gemini-2.0-flash",
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                api_key=gemini_api_key,
                tools=[]
            )

            with st.spinner("Generating summary..."):
                summary_result = await Runner.run(summary_agent, f"Summarize the following document:\n\n{extracted_text}")
                summary = summary_result.final_output
                st.session_state['summary'] = summary
                st.subheader("Summary:")
                st.markdown(summary)

            if st.button("Create Quiz"):
                with st.spinner("Generating quiz..."):
                    quiz = await generate_quiz(st.session_state['extracted_text']) # Call the tool directly
                    st.subheader("Generated Quiz:")
                    st.markdown(quiz)
                    st.session_state['quiz'] = quiz

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            os.remove(tmp_file_path)

if __name__ == "__main__":
    asyncio.run(main_async())
