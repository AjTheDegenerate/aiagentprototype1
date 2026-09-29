# Personal AI Assistant

A small Windows-first terminal assistant built with Python 3.11+, the OpenAI Python SDK, and simple function tools. It currently includes `open_app`, `web_search`, and `get_system_info`.

## Setup

1. Install Python 3.11 or newer and make sure the `python` command works in a new terminal.
2. In this project folder, create a virtual environment and install requirements:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and put your API key after `LLM_API_KEY=`. The example is configured for Gemini's OpenAI-compatible endpoint; `LLM_MODEL` selects the model. Never commit `.env` or share the key. For OpenAI, set `LLM_API_KEY` to your OpenAI key, remove `LLM_BASE_URL`, and set the model you want.
4. Run `python agent.py`.

The assistant keeps conversation history in memory for the current run. `open_app` asks you to confirm before it launches anything. Tool calls and results are recorded in `logs/assistant.log`. Web search needs an internet connection.

## Workspace setting

`config.py` contains `WORKSPACE_DIR`, initially set to an `assistant_workspace` folder next to this code. Future file tools should resolve paths against that directory and reject paths that escape it.

## Add a tool

Create one `.py` file inside `tools/`, import `register` from `tools`, and decorate a function with its name, description, and JSON schema. For example:

```python
from tools import register

@register("hello", "Say hello", {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"],
    "additionalProperties": False,
})
def hello(name: str) -> str:
    return f"Hello, {name}!"
```

Tool modules are discovered when the assistant starts. Set `confirm=True` in the decorator for actions that change something or send information. Keep each tool small and return readable error details by raising normal Python exceptions (the agent catches and logs them).

## Add voice later

Keep `run_turn(client, messages)` as the shared conversation core. A future speech-to-text input layer can turn audio into a string and pass it to the same function. A text-to-speech layer can speak the returned answer. The terminal input and output are currently the only interface; no audio packages are installed.
