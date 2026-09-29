"""Small terminal AI assistant with a simple function-calling loop."""

import json
import logging
import os

from dotenv import load_dotenv
from openai import OpenAI

import config
from tools import TOOLS, discover_tools


def setup_logging() -> None:
    """Keep a record of each tool call and its outcome in logs/assistant.log."""
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=config.LOG_DIR / "assistant.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def execute_tool(name: str, arguments: dict) -> str:
    """Run a registered tool safely, logging both successful and failed calls."""
    tool = TOOLS.get(name)
    if tool is None:
        return f"Error: Unknown tool '{name}'."
    if tool.requires_confirmation:
        print(f"\nThis will: {name}({json.dumps(arguments, ensure_ascii=False)})")
        answer = input("Allow this action? [y/N]: ").strip().lower()
        if answer != "y":
            result = "Cancelled by the user."
            logging.info("tool=%s arguments=%s result=%s", name, arguments, result)
            return result
    try:
        result = str(tool.function(**arguments))
    except Exception as error:  # A tool failure should not crash the chat loop.
        result = f"Error running {name}: {type(error).__name__}: {error}"
    logging.info("tool=%s arguments=%s result=%s", name, arguments, result)
    return result


def run_turn(client: OpenAI, messages: list[dict]) -> str:
    """Ask the model, execute requested tools, and repeat until it answers."""
    tool_definitions = [
        {"type": "function", "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters,
        }}
        for tool in TOOLS.values()
    ]

    for _ in range(config.MAX_TOOL_ROUNDS):
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", config.MODEL),
            messages=messages,
            tools=tool_definitions,
            tool_choice="auto",
        )
        message = response.choices[0].message
        messages.append(message.model_dump(exclude_none=True))
        if not message.tool_calls:
            return message.content or "(The assistant returned an empty answer.)"

        for call in message.tool_calls:
            try:
                arguments = json.loads(call.function.arguments or "{}")
                result = execute_tool(call.function.name, arguments)
            except Exception as error:
                result = f"Error handling tool request: {type(error).__name__}: {error}"
                logging.exception("Could not handle tool request")
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            })
    return "I reached the maximum number of tool steps for this request. Please try a more specific request."


def main() -> None:
    load_dotenv()
    setup_logging()
    discover_tools()
    # LLM_API_KEY works with OpenAI-compatible services such as Gemini.
    # OPENAI_API_KEY remains supported for the original OpenAI setup.
    api_key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("LLM_API_KEY is missing. Copy .env.example to .env and add your key.")

    client_options = {"api_key": api_key}
    base_url = os.getenv("LLM_BASE_URL")
    if base_url:
        client_options["base_url"] = base_url
    client = OpenAI(**client_options)
    messages = [{
        "role": "system",
        "content": "You are a helpful personal computer assistant. Be clear and concise. "
                   "Use available tools when useful. Ask the user for missing details before acting.",
    }]
    print("Personal assistant ready. Type 'quit' to exit.")
    while True:
        try:
            request = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if request.lower() in {"quit", "exit"}:
            print("Goodbye.")
            break
        if not request:
            continue
        messages.append({"role": "user", "content": request})
        try:
            print("\nAssistant:", run_turn(client, messages))
        except Exception as error:
            print(f"\nAssistant error: {type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
