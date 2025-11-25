1. Project Overview

Your mission is to build an AI Agent capable of:

Extracting text from PDFs (PyPDF)

Generating a clean, meaningful summary

Creating a quiz (MCQs or mixed format)

Frontend: Streamlit (recommended) or HTML/CSS

Backend / Agent: OpenAgents SDK

Model: Gemini (via Gemini CLI)

Tool Provider: Context7 MCP (Docs Reader Tool)

2. Strict Technical Rules

These rules must be followed exactly, with no exceptions.

1. Zero-Bloat Protocol

Write only the required logic.

No additional decorators, helper classes, or UI components.

No extra comments or unnecessary error handling.

2. API Configuration (MANDATORY)

You must use:

OpenAgents SDK

Gemini Base URL:
https://generativelanguage.googleapis.com/v1beta/openai/

Model: gemini-2.0-flash

Environment Variable: GEMINI_API_KEY

3. SDK Syntax Compliance

Do not use the standard openai library.

Use only openai-agents syntax exactly as documented.

All tools must exactly match the SDK tool definition format.

4. Error Recovery Protocol

If you encounter any of the following:

SyntaxError

ImportError

AttributeError

→ Stop immediately
→ Do not guess the solution
→ Run:

@get-library-docs openai-agents

→ Verify correct syntax before continuing.

5. Dependency Rules

Use uv for installing and managing packages.

3. Project File Structure

Your task4/ directory (inside Gemini CLI) must follow this structure:

task4/
├── .gemini/
│ └── settings.json
├── gemini.md
├── main.py
├── pyproject.toml
├── README.md
├── .env
└── uv.lock

⚠️ No additional subfolders are allowed.
All logic must remain inside this root directory.

4. Implementation Flow

Follow the steps below exactly in order.

Step 1 — Documentation Verification

Inside Gemini CLI, run:

@get-library-docs openai-agents

Review:

Tool definition patterns

Agent initialization

Model invocation syntax

Registering tools with the agent

If any step is unclear → repeat the documentation query.

Step 2 — Tool Definitions (Inside main.py)

You must create exactly two tools:

1. extract_pdf_text(file_path)

Use PyPDF to open and read the PDF.

Extract all text.

Return plain raw text.

2. generate_quiz(text)

Accept the original PDF text.

Send it to the agent.

Return a quiz (MCQs or mixed format).

Important:
Tool functions must exactly match the format shown in OpenAgents SDK documentation.

Step 3 — Agent Configuration (main.py)

You must:

Set the Gemini base URL.

Use model: gemini-2.0-flash

Register both tools inside the agent.

Add the system prompt:

"You are a Study Notes Assistant. First summarize the provided PDF content, then generate a quiz based on it."

Step 4 — Streamlit UI

The UI must include:

PDF file uploader.

Text extraction step using PyPDF.

Summary display.

A Create Quiz button.

Display of the generated quiz.

UI may use cards, blocks, containers, or simple text—your choice.

5. Testing Requirements

Verify the following cases:

Uploading a PDF produces a valid summary.

Clicking Create Quiz returns a valid quiz.

Larger PDFs lead to richer summaries and more detailed quizzes.
