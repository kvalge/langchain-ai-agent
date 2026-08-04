# to run: python main.py

import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

from tools import extract_action_items, extract_key_points, preview_transcript
from transcript_io import (
    extract_date,
    list_pending_transcripts,
    read_transcript,
    save_output,
)

load_dotenv()

SYSTEM_PROMPT = """
You are an Intelligent Meeting Notes Assistant in a conversational session.

You must remember across messages in the same session:
- The meeting transcript already provided
- Prior answers and any corrections the user made
- The latest version of the structured meeting notes

When the user first sends a transcript, produce clean structured meeting notes with:
- Key discussion points
- Decisions made
- Action items with responsible owners (when stated)
- A short summary

When the user asks follow-up questions, answer from session memory.
If they ask you to revise the notes, update the structured notes accordingly.

When asked for the final meeting notes document, return only the complete,
up-to-date structured notes (ready to save to a file), with no extra chat framing.

Rules:
- Use tools when they help extract candidate lines from the transcript
- Do NOT add information that is not in the transcript or confirmed by the user
- Be accurate, factual, and concise
"""

INITIAL_NOTES_INSTRUCTION = """
Analyze the following meeting transcript and produce structured meeting notes.

Include these sections:
1. Summary
2. Key discussion points
3. Decisions
4. Action items (with owners when available)

Transcript:
"""

FINAL_NOTES_INSTRUCTION = (
    "Produce the final consolidated meeting notes document now, incorporating "
    "the original transcript analysis and any corrections or clarifications from "
    "this conversation. Return only the complete notes, ready to save to a file."
)


def require_env() -> tuple[str, str]:
    """Validate required environment variables and return (model, api_key)."""
    model_name = os.getenv("GEMINI_MODEL")
    api_key = os.getenv("GEMINI_API_KEY")
    missing = [
        name
        for name, value in (("GEMINI_MODEL", model_name), ("GEMINI_API_KEY", api_key))
        if not value
    ]
    if missing:
        raise ValueError(
            "Missing required environment variable(s) in .env: " + ", ".join(missing)
        )
    return model_name, api_key


def build_agent(model_name: str, api_key: str):
    """Create the Gemini-backed agent with short-term memory."""
    model = ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
    memory = InMemorySaver()
    tools = [extract_key_points, extract_action_items, preview_transcript]
    return create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )


def thread_config(transcript_date: str) -> dict:
    """One memory thread per transcript date so meetings do not mix."""
    return {"configurable": {"thread_id": f"meeting-{transcript_date}"}}


def format_content(content) -> str:
    """Normalize agent message content into a plain text string."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        seen = set()
        parts = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                text = block["text"].strip()
                if text and text not in seen:
                    seen.add(text)
                    parts.append(text)
        return "\n".join(parts)

    return str(content)


def invoke_agent(agent, message: str, transcript_date: str) -> str:
    """Invoke the agent with thread memory and return plain-text content."""
    result = agent.invoke(
        {"messages": [HumanMessage(content=message)]},
        config=thread_config(transcript_date),
    )
    return format_content(result["messages"][-1].content)


def follow_up_session(agent, transcript_date: str, latest_notes: str) -> str:
    """
    Interactive follow-ups for one transcript.
    Saves nothing here; returns the latest notes text to persist after exit.
    """
    print(
        "\n"
        "============================================================\n"
        "Follow-up mode\n"
        "------------------------------------------------------------\n"
        "Ask questions or request changes to these meeting notes.\n"
        "When you are done, type: exit\n"
        "(also accepted: quit)\n"
        "That saves the final notes file and continues to the next transcript.\n"
        "============================================================\n"
    )

    prompt = "Follow-up (type 'exit' to save notes): "

    while True:
        try:
            question = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEnding follow-up session (same as typing 'exit').")
            break

        if not question:
            print("(Ask a question, or type 'exit' to save the final notes.)")
            continue

        if question.lower() in {"exit", "exit()", "quit"}:
            break

        try:
            answer = invoke_agent(agent, question, transcript_date)
        except Exception as exc:
            print(f"\nError answering follow-up: {exc}\n")
            continue

        print(f"\n{answer}\n")
        print("(Type another follow-up, or 'exit' to save the final notes.)\n")

        # If the user asked to revise notes, keep the latest assistant text as a candidate.
        revision_cues = ("update the notes", "revise", "corrected notes", "final notes")
        if any(cue in question.lower() for cue in revision_cues):
            latest_notes = answer

    print("\nGenerating final meeting notes for save...\n")
    try:
        final_notes = invoke_agent(agent, FINAL_NOTES_INSTRUCTION, transcript_date)
        if final_notes.strip():
            return final_notes
    except Exception as exc:
        print(f"Could not refresh final notes from the agent ({exc}).")
        print("Saving the latest notes from this session instead.\n")

    return latest_notes


def process_transcript(agent, transcript_path) -> None:
    """Analyze one transcript, run follow-ups, then save notes on exit."""
    transcript_date = extract_date(transcript_path)
    print(f"--- Processing {transcript_path.name} ---\n")

    transcript = read_transcript(transcript_path)
    notes = invoke_agent(
        agent,
        INITIAL_NOTES_INSTRUCTION + transcript,
        transcript_date,
    )
    print(notes)

    final_notes = follow_up_session(agent, transcript_date, notes)
    output_path = save_output(final_notes, transcript_date=transcript_date)
    print(f"\nSaved final meeting notes to: {output_path}\n")


def main():
    model_name, api_key = require_env()
    agent = build_agent(model_name, api_key)

    pending = list_pending_transcripts()
    if not pending:
        print("All transcripts are already processed. Nothing to do.")
        return

    print(f"Found {len(pending)} pending transcript(s).\n")

    failures: list[str] = []
    for transcript_path in pending:
        try:
            process_transcript(agent, transcript_path)
        except Exception as exc:
            failures.append(transcript_path.name)
            print(f"\nFailed to process {transcript_path.name}: {exc}\n")
            continue

    if failures:
        print("Finished with failures:")
        for name in failures:
            print(f"  - {name}")
    else:
        print("All pending transcripts processed successfully.")


if __name__ == "__main__":
    main()
