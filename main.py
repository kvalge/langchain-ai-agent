# to run: python main.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from encoding import read_transcript, save_output

# New Import for Memory.
from langgraph.checkpoint.memory import InMemorySaver

# Load environment variables from .env file
load_dotenv()

## Step 1: Defining Agent Behaviour
SYSTEM_PROMPT = """
You are an Intelligent Meeting Notes Assistant.

Your responsibilities:
- Identify key discussion points from the meeting transcript
- Extract decisions made during the meeting
- Extract action items along with responsible owners
- Produce a clean, structured summary

Rules:
- Use tools when necessary
- Do NOT add information that is not in the transcript
- Be accurate, factual, and concise
"""

# Transcript file name inside input/transcripts/
TRANSCRIPT_FILE = "transcript_2026-08-03.txt"


# Step 2: Defining Tools that LLM can use
def extract_key_points(text: str):
    """Extract lines containing discussions or updates."""

    lines = text.split("\n")
    points = [line.strip() for line in lines if "discuss" in line.lower() or "update" in line.lower()]
    return "\n".join(points) if points else "No key points found."


def extract_action_items(text: str):
    """Extract lines that mention action items."""
    lines = text.split("\n")
    actions = [line.strip() for line in lines if any(word in line.lower() for word in ["action", "will", "needs", "should"])]
    return "\n".join(actions) if actions else "No action items found."


def summarize_meeting(text: str):
    """Return a simple short summary of the meeting."""
    lines = text.split("\n")[:10]
    return f"Summary:\n" + "\n".join(lines)


## Step 3: Integrating an LLM model to power the Agent
model_name = os.getenv("GEMINI_MODEL")
if not model_name:
    raise ValueError("GEMINI_MODEL is not set in .env")

model = ChatGoogleGenerativeAI(model=model_name)

## Step 4: Use the create_agent Framework

# Create a tool list to let LLM know what tools are at their disposal
tools = [summarize_meeting, extract_action_items, extract_key_points]

# Finally create the agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


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


def main():
    # Read the transcript from input/transcripts/
    transcript = read_transcript(TRANSCRIPT_FILE)

    print("\n--- Agent Output ---\n")

    result = agent.invoke({
        "messages": [HumanMessage(content=transcript)]
    })

    output_text = format_content(result["messages"][-1].content)
    print(output_text)

    # Save output to output/ with today's date in the filename
    output_path = save_output(output_text)
    print(f"\nSaved output to: {output_path}")


if __name__ == "__main__":
    main()
