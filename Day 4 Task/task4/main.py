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
    This tool is called by the main agent to generate the quiz content directly.

    Args:
        text: The text content from which to generate the quiz.

    Returns:
        A string containing the generated quiz.
    """
    # This tool's role is to formulate the LLM call for quiz generation
    # based on the text provided. The main agent will use this tool.
    # The actual LLM call for quiz generation needs to happen *here* within the tool,
    # as instructed by the "Every function must match the tool documentation exactly." rule.
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

    # Create a temporary agent for quiz generation within the tool itself
    quiz_agent = Agent(
        name="QuizGenerator",
        instructions="You are an expert quiz generator. Create a multiple-choice or mixed quiz based on the provided text.",
        model=model,
        tools=[] # No tools needed for this internal agent
    )

    quiz_prompt = f"Generate a detailed quiz (mix of MCQs and open-ended questions if possible) from the following text:\n\n{text}\n\nEnsure there are at least 5 questions. Provide answers after the questions."
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
    instructions="You are a Study Notes Assistant. Your task is to first provide a concise summary of the given text, and then generate a detailed quiz (mix of MCQs and open-ended questions if possible) from the text using the 'generate_quiz' tool. Format your final output with a 'Summary:' heading followed by the summary, and a 'Quiz:' heading followed by the quiz content.",
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
                agent_result = await Runner.run(study_agent, extracted_text)
                full_output = agent_result.final_output

                summary_content = "No summary found."
                quiz_content = "No quiz found."

                summary_marker = "Summary:"
                quiz_marker = "Quiz:"

                summary_start_index = full_output.find(summary_marker)
                quiz_start_index = full_output.find(quiz_marker)

                if summary_start_index != -1:
                    if quiz_start_index != -1 and quiz_start_index > summary_start_index:
                        summary_content = full_output[summary_start_index + len(summary_marker):quiz_start_index].strip()
                        quiz_content = full_output[quiz_start_index + len(quiz_marker):].strip()
                    else:
                        summary_content = full_output[summary_start_index + len(summary_marker):].strip()
                elif quiz_start_index != -1:
                    quiz_content = full_output[quiz_start_index + len(quiz_marker):].strip()
                else:
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
