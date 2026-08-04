# LangChain AI Agent (Gemini CLI)

Intelligent meeting notes agent that analyses transcripts, highlights key discussion points, extracts decisions and action items, and produces a summary.

## Generated outputs

- [meeting_notes_2026-08-04.txt](output/meeting_notes_2026-08-04.txt)

## Features

- LangChain agent powered by Google Gemini
- Transcripts stored under `input/transcripts/`
- Agent output saved under `output/` with the run date in the filename
- Each new output file is linked in this README under **Generated outputs**
- Model configured via environment variables

## Project structure

```text
.
├── input/
│   └── transcripts/          # Meeting transcript input files
├── output/                   # Generated meeting notes (dated filenames)
├── encoding.py               # Read transcripts / write dated outputs / update README links
├── main.py                   # Agent entry point
├── .env.example
├── requirements.txt
└── README.md
```

| Path | Description |
|------|-------------|
| `input/transcripts/` | Place transcript `.txt` files here |
| `output/` | Agent writes dated result files here (tracked in git) |
| `main.py` | Runs the meeting-notes agent |
| `encoding.py` | File I/O helpers and README link updates |

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

1. Put a transcript file in `input/transcripts/` (for example `transcript_2026-08-03.txt`).
2. Set `TRANSCRIPT_FILE` in `main.py` to that filename if needed.
3. Run:

```bash
python main.py
```

The agent:

1. Prints the summary to the console
2. Saves it under `output/` as `meeting_notes_YYYY-MM-DD.txt` (adds a time suffix if that file already exists)
3. Adds a markdown link to the new file under **Generated outputs** in this README

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `GEMINI_MODEL` | Yes | Model ID |

Never commit `.env`. Only `.env.example` should be in version control.
