from __future__ import annotations

try:
	from frappe.frappeclient import FrappeClient, FrappeException
except ImportError:  # pragma: no cover - framework layout fallback
	from frappe.integrations.frappe_providers.frappeclient import FrappeClient, FrappeException  # type: ignore

__all__ = ["FrappeClient", "FrappeException"]
