import re
from datetime import datetime
from pathlib import Path

INPUT_DIR = Path("input")
TRANSCRIPTS_DIR = INPUT_DIR / "transcripts"
OUTPUT_DIR = Path("output")
README_PATH = Path("README.md")
OUTPUTS_HEADING = "## Generated outputs"


def read_transcript(filename: str) -> str:
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


def save_output(text: str, prefix: str = "meeting_notes") -> Path:
    """Write agent output to output/ with today's date in the filename."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_stamp = datetime.now().strftime("%Y-%m-%d")
    output_path = OUTPUT_DIR / f"{prefix}_{date_stamp}.txt"

    # If a file for today already exists, append a time suffix
    if output_path.exists():
        time_stamp = datetime.now().strftime("%H%M%S")
        output_path = OUTPUT_DIR / f"{prefix}_{date_stamp}_{time_stamp}.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    add_output_link_to_readme(output_path)
    return output_path
