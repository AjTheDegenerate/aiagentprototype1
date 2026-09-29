"""Tool registry. New files in this folder are discovered automatically."""

from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
import pkgutil
from typing import Any, Callable


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    function: Callable[..., Any]
    requires_confirmation: bool = False


TOOLS: dict[str, Tool] = {}


def register(name: str, description: str, parameters: dict[str, Any], *, confirm: bool = False):
    """Decorator to add a function and its JSON schema to the tool registry."""
    def decorator(function: Callable[..., Any]):
        TOOLS[name] = Tool(name, description, parameters, function, confirm)
        return function
    return decorator


def discover_tools() -> None:
    """Import every tool module so its decorators register the functions."""
    for module in pkgutil.iter_modules(__path__):
        if module.name != "__init__":
            import_module(f"{__name__}.{module.name}")

