from __future__ import annotations

from contextlib import suppress
from typing import Any

import frappe

from press.utils import log_error


def _get_posthog_client_class():
	try:
		from posthog import Posthog

		return Posthog
	except ImportError:
		with suppress(ImportError):
			from posthog import Client

			return Client
	return None


def init_telemetry():
	"""Init posthog for server side telemetry."""
	if hasattr(frappe.local, "posthog"):
		return

	posthog_host = frappe.conf.get("posthog_host")
	posthog_project_id = frappe.conf.get("posthog_project_id")

	if not posthog_host or not posthog_project_id:
		return

	Posthog = _get_posthog_client_class()
	if Posthog is None:
		return

	with suppress(Exception):
		frappe.local.posthog = Posthog(posthog_project_id, host=posthog_host)


def capture(event, app, distinct_id=None):
	init_telemetry()
	ph: Any = getattr(frappe.local, "posthog", None)
	with suppress(Exception):
		properties = {}
		if app == "fc_product_trial":
			properties = {"product_trial": True}
		ph and ph.capture(
			distinct_id=distinct_id or frappe.local.site, event=f"{app}_{event}", properties=properties
		)


def identify(site, **kwargs):
	init_telemetry()
	ph: Any = getattr(frappe.local, "posthog", None)
	with suppress(Exception):
		ph and ph.identify(site, kwargs)


@frappe.whitelist(allow_guest=True)
def capture_read_event(email: str | None = None):
	try:
		capture("read_email", "fc_signup", email)
	except Exception as e:
		log_error("Failed to capture read_email event", e)
	finally:
		frappe.response.update(frappe.utils.get_imaginary_pixel_response())
