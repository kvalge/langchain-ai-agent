# LangChain AI Agent (Gemini CLI)

Intelligent meeting notes agent that analyses transcripts, highlights key discussion points, extracts decisions and action items, and produces a summary. After notes are drafted, you can ask follow-up questions in the terminal; the output file is written only when you type `exit`.

## Generated outputs

- [meeting_notes_2026-08-03.txt](output/meeting_notes_2026-08-03.txt)
- [meeting_notes_2026-08-04.txt](output/meeting_notes_2026-08-04.txt)

## Features

- LangChain agent powered by Google Gemini
- Conversational session with short-term memory (one thread per transcript date)
- `@tool`-decorated helpers (`extract_key_points`, `extract_decisions`, `extract_action_items`, `summarize_transcript`) used while drafting notes
- Drop transcripts into `input/transcripts/` — no hardcoded filename in code
- Auto-discovers pending `transcript_YYYY-MM-DD.txt` files and skips already-processed dates
- Follow-up questions in the terminal before saving
- Final notes saved under `output/` as `meeting_notes_YYYY-MM-DD.txt` only after `exit`
- Each new output file is linked in this README under **Generated outputs**
- Model and API key configured via environment variables

## Project structure

```text
.
├── input/
│   └── transcripts/          # Meeting transcript input files
├── output/                   # Generated meeting notes (dated filenames)
├── transcript_io.py          # Transcript discovery / dated outputs / README links
├── tools.py                  # @tool helpers for notes sections (MEETING_TOOLS)
├── main.py                   # Agent + conversational session entry point
├── .env.example
├── requirements.txt
└── README.md
```

| Path | Description |
|------|-------------|
| `input/transcripts/` | Place `transcript_YYYY-MM-DD.txt` files here |
| `output/` | Final `meeting_notes_YYYY-MM-DD.txt` files (written after `exit`) |
| `main.py` | Runs the agent and follow-up session |
| `tools.py` | `@tool` extraction helpers aligned to notes sections |
| `transcript_io.py` | Discovery, file I/O, and README link updates |

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

1. Add a transcript as `input/transcripts/transcript_YYYY-MM-DD.txt`.
2. Run:

```bash
python main.py
```

3. For each **pending** transcript (no matching output yet):
   - The agent prints draft meeting notes
   - A follow-up banner explains how to continue
   - Ask questions at `Follow-up (type 'exit' to save notes):` (session memory keeps the transcript and prior answers)
   - Type `exit` or `quit` to finish that transcript (reminders also appear after each answer)
   - The agent produces the final consolidated notes and saves `output/meeting_notes_YYYY-MM-DD.txt`
   - A markdown link is added under **Generated outputs**
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
