from typing import Any

from dify_plugin import ToolProvider


class CohesivityProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # No credentials required. Cohesivity uses per-tenant keys
        # returned by create_tenant, not provider-level API keys.
        pass
