import os
import streamlit as st
import asyncio
from pypdf import PdfReader
from agents import Agent, function_tool, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import tempfile

load_dotenv()

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

    external_Client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    model = OpenAIChatCompletionsModel(
        model= "gemini-2.0-flash",
        openai_client=external_Client
    )

    # Create a temporary agent for quiz generation
    quiz_agent = Agent(
        name="QuizGenerator",
        instructions="You are an expert quiz generator. Create a multiple-choice or mixed quiz based on the provided text.",
        model=model,
       
        tools=[] # No tools needed for this internal agent
    )

    quiz_prompt = f"Generate a detailed quiz (mix of MCQs and open-ended questions if possible) from the following text:\n\n{text}\n\nEnsure there are at least 5 questions. Provide answers after the questions.\n\nOutput format:\nSummary:\n[Summary Content]\n\nQuiz:\n[Quiz Content]"

    quiz_result = await Runner.run(quiz_agent, quiz_prompt)
    return quiz_result.final_output

# Agent Setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

external_Client = AsyncOpenAI(
  api_key=gemini_api_key,
  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model= "gemini-2.0-flash",
    openai_client=external_Client
)

study_agent = Agent(
    name="StudyNotesAssistant",
    instructions="You are a Study Notes Assistant. First produce a summary, then generate a quiz. Use the generate_quiz tool to create the quiz. Format your output clearly with 'Summary:' and 'Quiz:' sections.",
    model=model,
    tools=[generate_quiz]
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

            with st.spinner("Generating summary and quiz..."):
                combined_prompt = f"Please summarize the following document and then generate a quiz from it:\n\n{extracted_text}"
                
                agent_result = await Runner.run(study_agent, combined_prompt)
                full_output = agent_result.final_output

                # Attempt to parse summary and quiz based on expected agent output format
                summary_start = full_output.find("Summary:")
                quiz_start = full_output.find("Quiz:")

                summary_content = "No summary found."
                quiz_content = "No quiz found."

                if summary_start != -1 and quiz_start != -1 and summary_start < quiz_start:
                    summary_content = full_output[summary_start + len("Summary:"):quiz_start].strip()
                    quiz_content = full_output[quiz_start + len("Quiz:"):].strip()
                elif summary_start != -1 and quiz_start == -1: # Only summary found
                    summary_content = full_output[summary_start + len("Summary:"):].strip()
                elif quiz_start != -1 and summary_start == -1: # Only quiz found
                    quiz_content = full_output[quiz_start + len("Quiz:"):].strip()
                else:
                    # Fallback if parsing fails, display raw output
                    st.subheader("Agent Output (Unable to parse into Summary and Quiz):")
                    st.markdown(full_output)

                if summary_content != "No summary found.":
                    st.subheader("Summary:")
                    st.markdown(summary_content)
                    st.session_state['summary'] = summary_content

                if quiz_content != "No quiz found.":
                    st.subheader("Generated Quiz:")
                    st.markdown(quiz_content)
                    st.session_state['quiz'] = quiz_content

        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            os.remove(tmp_file_path)

if __name__ == "__main__":
    asyncio.run(main_async())