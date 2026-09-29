"""Search the web using the lightweight DuckDuckGo Search package."""

from ddgs import DDGS

from tools import register


@register(
    "web_search",
    "Search the web and return a few relevant results with a short summary of their snippets.",
    {"type": "object", "properties": {"query": {"type": "string", "description": "What to search for"}}, "required": ["query"], "additionalProperties": False},
)
def web_search(query: str) -> str:
    results = list(DDGS().text(query, max_results=5))
    if not results:
        return "No search results were returned."

    lines = [f"Search results for: {query}"]
    snippets = []
    for number, result in enumerate(results, start=1):
        title = result.get("title", "Untitled")
        url = result.get("href", "")
        snippet = result.get("body", "")
        lines.append(f"{number}. {title}\n   {url}\n   {snippet}")
        if snippet:
            snippets.append(snippet)
    lines.append("\nSnippet summary: " + (" ".join(snippets[:3])[:900] or "No snippets available."))
    return "\n".join(lines)

