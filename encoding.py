import re
from datetime import datetime
from pathlib import Path

INPUT_DIR = Path("input")
TRANSCRIPTS_DIR = INPUT_DIR / "transcripts"
OUTPUT_DIR = Path("output")
README_PATH = Path("README.md")
OUTPUTS_HEADING = "## Generated outputs"

DATE_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})")


def extract_date(path: Path | str) -> str:
    """Parse YYYY-MM-DD from a transcript or output filename."""
    name = Path(path).name
    match = DATE_PATTERN.search(name)
    if not match:
        raise ValueError(f"No YYYY-MM-DD date found in filename: {name}")
    return match.group(1)


def list_transcripts() -> list[Path]:
    """Return sorted transcript_*.txt files from input/transcripts/."""
    if not TRANSCRIPTS_DIR.exists():
        return []
    return sorted(TRANSCRIPTS_DIR.glob("transcript_*.txt"))


def is_processed(transcript_path: Path) -> bool:
    """True if output/ already has meeting_notes_<same-date>.txt (or time-suffixed)."""
    date_stamp = extract_date(transcript_path)
    exact = OUTPUT_DIR / f"meeting_notes_{date_stamp}.txt"
    if exact.exists():
        return True
    return any(OUTPUT_DIR.glob(f"meeting_notes_{date_stamp}_*.txt"))


def list_pending_transcripts() -> list[Path]:
    """Transcripts that do not yet have a matching dated output."""
    return [path for path in list_transcripts() if not is_processed(path)]


def read_transcript(filename: str | Path) -> str:
    """Read a transcript from input/transcripts, trying common encodings."""
    path = Path(filename)
    if not path.is_absolute() and path.parent == Path("."):
        path = TRANSCRIPTS_DIR / path.name

    encodings = ["utf-8-sig", "utf-8", "latin-1", "cp1252"]

    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            print(f"Tried {encoding}... failed")
            continue

    raise ValueError(f"Could not decode {path} with any common encoding")


def add_output_link_to_readme(output_path: Path) -> None:
    """Insert a markdown link to the new output after the README intro text."""
    if not README_PATH.exists():
        return

    relative = output_path.as_posix()
    link_line = f"- [{output_path.name}]({relative})"
    text = README_PATH.read_text(encoding="utf-8")

    if relative in text:
        return

    if OUTPUTS_HEADING in text:
        text = re.sub(
            rf"({re.escape(OUTPUTS_HEADING)}\n\n)",
            rf"\1{link_line}\n",
            text,
            count=1,
        )
    else:
        text = re.sub(
            r"(# LangChain AI Agent \(Gemini CLI\)\n\n.+?\n\n)",
            rf"\1{OUTPUTS_HEADING}\n\n{link_line}\n\n",
            text,
            count=1,
            flags=re.DOTALL,
        )

    README_PATH.write_text(text, encoding="utf-8")


def save_output(
    text: str,
    transcript_date: str | None = None,
    prefix: str = "meeting_notes",
) -> Path:
    """Write agent output to output/ using the transcript date in the filename."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_stamp = transcript_date or datetime.now().strftime("%Y-%m-%d")
    output_path = OUTPUT_DIR / f"{prefix}_{date_stamp}.txt"

    # If a file for this date already exists, append a time suffix
    if output_path.exists():
        time_stamp = datetime.now().strftime("%H%M%S")
        output_path = OUTPUT_DIR / f"{prefix}_{date_stamp}_{time_stamp}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    add_output_link_to_readme(output_path)
    return output_path
