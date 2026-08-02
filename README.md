# LangChain AI Agent (Gemini CLI)

A simple command-line app that sends prompts to Google Gemini and prints the response.

## Features

- Interactive CLI prompt loop
- Gemini model configured via environment variables
- Loading animation while generating a response

## Project structure

| File | Description |
|------|-------------|
| `main.py` | CLI entry point |
| `gemini_provider.py` | Gemini API setup and response helper |
| `.env.example` | Template for required environment variables |
| `requirements.txt` | Python dependencies |

## Prerequisites

- Python 3.10+
- A [Google AI Studio](https://aistudio.google.com/apikey) API key

## Setup

1. Clone the repository and go into the project directory.

2. Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create your local env file from the example:

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

5. Edit `.env` and set your values:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=your_model_here
```

Use a model name that is available for your API key. See the [Gemini models list](https://ai.google.dev/gemini-api/docs/models).

## Usage

```bash
python main.py
```

Enter a prompt at the `Prompt:` prompt. Type `exit` or `quit` to leave.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `GEMINI_MODEL` | Yes | Model ID |

Never commit `.env`. Only `.env.example` should be in version control.
