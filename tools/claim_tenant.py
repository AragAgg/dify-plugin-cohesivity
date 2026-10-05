import json
from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

MCP_URL = "https://cohesivity.ai/mcp"


class ClaimTenantTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        tenant_id = tool_parameters.get("tenant_id", "")
        coh_management_key = tool_parameters.get("coh_management_key", "")
        confirmed = tool_parameters.get("confirmed", False)

        if not tenant_id:
            yield self.create_text_message("Parameter 'tenant_id' is required.")
            return
        if not coh_management_key:
            yield self.create_text_message("Parameter 'coh_management_key' is required.")
            return
        if not confirmed:
            yield self.create_text_message("Claiming requires confirmed=true.")
            return

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "claim_tenant",
                "arguments": {
                    "tenant_id": tenant_id,
                    "coh_management_key": coh_management_key,
                    "confirmed": True,
                },
            },
        }

        try:
            resp = requests.post(
                MCP_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
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
