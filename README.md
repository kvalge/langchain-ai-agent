# LangChain AI Agent (Gemini CLI)

Intelligent meeting notes agent that analyses transcripts, highlights key discussion points, extracts decisions and action items, and produces a summary.

## Generated outputs

- [meeting_notes_2026-08-03.txt](output/meeting_notes_2026-08-03.txt)
- [meeting_notes_2026-08-04.txt](output/meeting_notes_2026-08-04.txt)

## Features

- LangChain agent powered by Google Gemini
- Drop transcripts into `input/transcripts/` — no hardcoded filename in code
- Auto-discovers pending `transcript_YYYY-MM-DD.txt` files and skips already-processed dates
- Agent output saved under `output/` as `meeting_notes_YYYY-MM-DD.txt` (date from the transcript)
- Each new output file is linked in this README under **Generated outputs**
- Model configured via environment variables

## Project structure

```text
.
├── input/
│   └── transcripts/          # Meeting transcript input files
├── output/                   # Generated meeting notes (dated filenames)
├── encoding.py               # Transcript discovery / dated outputs / README links
├── main.py                   # Agent entry point
├── .env.example
├── requirements.txt
└── README.md
```

| Path | Description |
|------|-------------|
| `input/transcripts/` | Place `transcript_YYYY-MM-DD.txt` files here |
| `output/` | Agent writes `meeting_notes_YYYY-MM-DD.txt` here (tracked in git) |
| `main.py` | Runs the meeting-notes agent over pending transcripts |
| `encoding.py` | Discovery, file I/O, and README link updates |

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

Drop-and-run workflow (no filename typing, no code edits):

1. Add a transcript as `input/transcripts/transcript_YYYY-MM-DD.txt` (for example `transcript_2026-08-05.txt`).
2. Run:

```bash
python main.py
```

3. The agent processes every **pending** transcript (no matching output yet):
   - Prints the summary to the console
   - Saves `output/meeting_notes_YYYY-MM-DD.txt` using the date from the transcript filename
   - Adds a markdown link under **Generated outputs** in this README
4. Re-running `python main.py` skips dates that already have an output.

| Role | Pattern | Example |
|------|---------|---------|
| Input | `transcript_YYYY-MM-DD.txt` | `transcript_2026-08-03.txt` |
| Output | `meeting_notes_YYYY-MM-DD.txt` | `meeting_notes_2026-08-03.txt` |

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `GEMINI_MODEL` | Yes | Model ID |

Never commit `.env`. Only `.env.example` should be in version control.
