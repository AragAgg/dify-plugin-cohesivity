import json
from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

MCP_URL = "https://cohesivity.ai/mcp"


class GetDocumentationTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        document = tool_parameters.get("document", "")
        if not document:
            yield self.create_text_message("Parameter 'document' is required.")
            return

        arguments: dict[str, Any] = {"document": document}

        offering = tool_parameters.get("offering", "")
        if document == "offering":
            if not offering:
                yield self.create_text_message(
                    "Parameter 'offering' is required when document is 'offering'."
                )
                return
            arguments["offering"] = offering

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "get_cohesivity_documentation",
                "arguments": arguments,
            },
        }

        try:
            resp = requests.post(
                MCP_URL,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "cohesivity-dify-plugin/0.0.1",
                },
                timeout=30,
            )
            resp.raise_for_status()
            result = resp.json()
        except requests.exceptions.RequestException as exc:
            yield self.create_text_message(f"Request failed: {exc}")
            return

        if "error" in result:
            yield self.create_text_message(
                f"Error: {result['error'].get('message', json.dumps(result['error']))}"
            )
            return

        content_items = result.get("result", {}).get("content", [])
        text_parts = [
            item.get("text", "") for item in content_items if item.get("type") == "text"
        ]
        yield self.create_text_message("\n".join(text_parts))
