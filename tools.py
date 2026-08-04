"""Helper tools the meeting-notes agent can call for structured extraction."""


def extract_key_points(text: str) -> str:
    """Extract discussion points, updates, decisions, and concerns from the transcript."""
    keywords = (
        "discuss",
        "discussed",
        "update",
        "decision",
        "decided",
        "agreed",
        "concern",
        "raised",
        "proposed",
        "noted",
    )
    lines = text.split("\n")
    points = [
        line.strip()
        for line in lines
        if any(keyword in line.lower() for keyword in keywords)
    ]
    return "\n".join(points) if points else "No key points found."


def extract_action_items(text: str) -> str:
    """Extract action items and ownership cues (will/needs/should/action/by date)."""
    keywords = (
        "action",
        "will",
        "needs",
        "should",
        "must",
        "by wednesday",
        "by friday",
        "by end",
        "next week",
        "responsible",
    )
    lines = text.split("\n")
    actions = [
        line.strip()
        for line in lines
        if any(keyword in line.lower() for keyword in keywords)
    ]
    return "\n".join(actions) if actions else "No action items found."


def preview_transcript(text: str, max_lines: int = 12) -> str:
    """Return the first lines of the transcript for quick context (not a full summary)."""
    lines = [line for line in text.split("\n") if line.strip()][:max_lines]
    return "Transcript preview:\n" + "\n".join(lines)
