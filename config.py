"""Settings for the personal assistant. Edit WORKSPACE_DIR to your chosen folder."""

from pathlib import Path

# By default, file tools are limited to an assistant_workspace folder here.
# Change this to another folder you own if you prefer.
WORKSPACE_DIR = Path(__file__).parent / "assistant_workspace"

MODEL = "gpt-4o-mini"
MAX_TOOL_ROUNDS = 8
LOG_DIR = Path(__file__).parent / "logs"

