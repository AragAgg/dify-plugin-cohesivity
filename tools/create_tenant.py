import json
from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

MCP_URL = "https://cohesivity.ai/mcp"


class CreateTenantTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        confirmed = tool_parameters.get("confirmed", False)
        if not confirmed:
            yield self.create_text_message(
                "Tenant creation requires confirmed=true. "
                "Please confirm the user wants to create a new Cohesivity tenant."
            )
            return

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "create_tenant",
                "arguments": {"confirmed": True},
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
        output = "\n".join(text_parts)

        yield self.create_text_message(output)
