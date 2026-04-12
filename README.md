# Automatic Code Refactoring Using AI

A Streamlit-based Capstone project that combines AI-powered code analysis with a deterministic refactoring engine and local execution sandbox.

## Overview

`capstone-project` is a hybrid code refactoring tool designed to:

- Analyze user-provided source code in Python, JavaScript, Java, or C++
- Generate refactoring suggestions through an AI code reviewer
- Apply patch updates to source code in a controlled manner
- Execute both original and refactored code locally for output comparison
- Display scoring, metrics, and analysis through an interactive Streamlit UI

## Key Features

- **AI Diagnosis**: Sends code to the OpenAI-compatible API with a structured prompt for analysis.
- **Refactoring Plan**: Parses AI output into a JSON patch plan and applies `replace_block` or `rename` operations.
- **Sandbox Execution**: Runs code in a temporary environment for Python, JavaScript, Java, and C++.
- **Verification**: Compares original and refactored outputs to detect mismatches and preserve logic.
- **Security Best Practice**: Secrets are loaded from `.env` and `.env` is ignored by Git.

## Architecture

- `app.py` - Streamlit UI and main orchestration layer
- `utils.py` - AI client integration and prompt assembly
- `auditor.py` - Code analysis logic and AI prompt design
- `prompts.py` - System and refactoring prompt templates
- `engine.py` - Patch application engine for refactored updates
- `executor.py` - Local execution sandbox for supported languages
- `tester.py` - Helper to run and compare test cases across code versions
- `requirements.txt` - Python dependencies

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root if it does not already exist:

```text
OPENAI_API_KEY=your_api_key_here
```

3. Ensure `.env` is not committed to Git. This repo already excludes `.env` via `.gitignore`.

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open the local Streamlit URL in your browser.

### How it works

- Paste source code into the editor panel.
- Choose the target language and optimization goal.
- Click `Analyze & Refactor Code`.
- Review the AI-generated refactored code and metrics.
- Optionally run appended execution code to compare outputs between original and refactored versions.

## Supported Languages

- Python
- JavaScript
- Java
- C++

## Important Notes

- The OpenAI-compatible API key is loaded from `OPENAI_API_KEY`.
- Do not expose API keys in source files.
- The current app uses `base_url="https://api.groq.com/openai/v1"` for the OpenAI client.

## File Summary

- `app.py` - UI layout and user interaction logic.
- `utils.py` - Environment loading and AI client initialization.
- `auditor.py` - AI prompt creation and analysis orchestration.
- `prompts.py` - Reusable prompt templates for the AI.
- `engine.py` - Applies refactor plan operations to code.
- `executor.py` - Executes code in a temporary sandbox.
- `tester.py` - Runs comparative tests between code versions.
- `.gitignore` - Ensures `.env` is not tracked.
- `.env` - Stores `OPENAI_API_KEY` securely.

## License

This repository is intended for Capstone / Educational use.
