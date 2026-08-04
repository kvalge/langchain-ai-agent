"""Helper tools the meeting-notes agent can call for structured extraction."""

from langchain.tools import tool


def _filter_lines(text: str, keywords: tuple[str, ...], empty_message: str) -> str:
    """Return numbered transcript lines that match any keyword (case-insensitive)."""
    matches: list[str] = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        if any(keyword in lowered for keyword in keywords):
            matches.append(stripped)

    if not matches:
        return empty_message

    return "\n".join(f"{index}. {line}" for index, line in enumerate(matches, start=1))


@tool
def extract_key_points(text: str) -> str:
    """Extract key discussion points from a meeting transcript.

    Use this when drafting or revising the Key discussion points section.
    Pass the full transcript text. Do not invent points missing from the result.

    Args:
        text: Full meeting transcript text.
    """
    keywords = (
        "discuss",
        "discussed",
        "discussion",
        "update",
        "updated",
        "concern",
        "raised",
        "proposed",
        "noted",
        "review",
        "reviewed",
        "topic",
        "issue",
        "trend",
        "feedback",
    )
    return _filter_lines(text, keywords, "No key points found in transcript.")


@tool
def extract_decisions(text: str) -> str:
    """Extract decisions and agreements from a meeting transcript.

    Use this when drafting or revising the Decisions section.
    Pass the full transcript text. Do not invent decisions missing from the result.

    Args:
        text: Full meeting transcript text.
    """
    keywords = (
        "decision",
        "decided",
        "decide",
        "agreed",
        "agree",
        "agreement",
        "approved",
        "approve",
        "prioritized",
        "priority",
        "will proceed",
        "go ahead",
        "confirmed",
        "resolution",
        "resolved",
    )
    return _filter_lines(text, keywords, "No decisions found in transcript.")


@tool
def extract_action_items(text: str) -> str:
    """Extract action items and ownership cues from a meeting transcript.

    Use this when drafting or revising the Action items section.
    Pass the full transcript text. Prefer lines that name an owner and a next step.

    Args:
        text: Full meeting transcript text.
    """
    keywords = (
        "action",
        "will",
        "needs",
        "should",
        "must",
        "to do",
        "todo",
        "assign",
        "assigned",
        "owner",
        "responsible",
        "by wednesday",
        "by friday",
        "by end",
        "by next",
        "next week",
        "follow up",
        "follow-up",
        "investigate",
        "prepare",
        "draft",
        "grant",
        "coordinate",
        "share",
        "report back",
    )
    return _filter_lines(text, keywords, "No action items found in transcript.")


@tool
def summarize_transcript(text: str) -> str:
    """Build a short factual bullet summary from a meeting transcript.

    Use this when drafting or revising the Summary section.
    Pass the full transcript text. Prefer meeting metadata and high-signal lines.

    Args:
        text: Full meeting transcript text.
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if not lines:
        return "No summary content found in transcript."

    bullets: list[str] = []
    meta_prefixes = ("meeting:", "date:", "attendees:", "next meeting")
    for line in lines:
        lowered = line.lower()
        if any(lowered.startswith(prefix) for prefix in meta_prefixes):
            bullets.append(f"- {line}")

    signal_keywords = (
        "opened",
        "closed",
        "summarizing",
        "top priorities",
        "priority",
        "agreed",
        "decided",
        "will",
    )
    for line in lines:
        lowered = line.lower()
        if any(keyword in lowered for keyword in signal_keywords):
            candidate = f"- {line}"
            if candidate not in bullets:
                bullets.append(candidate)
        if len(bullets) >= 8:
            break

    if not bullets:
        bullets = [f"- {line}" for line in lines[:5]]

    return "Summary candidates:\n" + "\n".join(bullets[:8])


MEETING_TOOLS = [
    extract_key_points,
    extract_decisions,
    extract_action_items,
    summarize_transcript,
]
