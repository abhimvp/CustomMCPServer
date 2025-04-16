# Project: AI Sticky Notes
import os
from mcp.server.fastmcp import FastMCP


# create an mcp server
mcp = FastMCP("AI Sticky Notes")

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")


def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")  # create an empty file


#  create an mcp tool using python decorator
# do not forget to add docstring
@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note to the sticky note file.

    Args:
        message (str): The note message to be added.

    Returns:
        str: Confirmation message indicating the note has been added/was saved.
    """
    # above now we have documented the tool , the AI knows when to use it.
    ensure_file()
    with open(NOTES_FILE, "a") as f:  # a is append mode
        f.write(message + "\n")
    return "Note added."


@mcp.tool()
def read_notes() -> str:
    """
    Read all the notes from the sticky note file.

    Returns:
        str: All the notes in the file, each note on a new line.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        notes = f.read().strip()
    return notes or "No notes found."


@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the latest note from the sticky note file.

    Returns:
        str: The latest note in the file.
    """
    ensure_file()
    with open(NOTES_FILE, "r") as f:
        notes = f.readlines()
    return notes[-1] if notes else "No notes found."


@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Summarize the latest note in the sticky note file.

    Returns:
        str: The summary of the latest note.
    """
    ensure_file()
    latest_note = get_latest_note()
    if latest_note == "No notes found.":
        return "No notes found."
    return f"Summarize the following note: {latest_note}"
