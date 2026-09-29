"""Tools for launching desktop applications."""

import os

from tools import register


@register(
    "open_app",
    "Open a desktop application by its installed app name or executable path.",
    {"type": "object", "properties": {"name": {"type": "string", "description": "Application name, for example notepad"}}, "required": ["name"], "additionalProperties": False},
    confirm=True,
)
def open_app(name: str) -> str:
    """Ask Windows to open an application using its normal file association."""
    if os.name != "nt":
        return "open_app is currently implemented for Windows only."
    os.startfile(name)  # Uses Windows' normal app/file launching behavior.
    return f"Asked Windows to open: {name}"

