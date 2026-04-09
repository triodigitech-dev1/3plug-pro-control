# Copyright (c) 2026, Triotek and contributors
# For license information, please see license.txt
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import frappe
from frappe.model.document import Document

if TYPE_CHECKING:
	from press.press.doctype.agent_job.agent_job import AgentJob
	from press.press.doctype.press_job.press_job import PressJob
	from press.press.doctype.press_job_step.press_job_step import PressJobStep
	from press.press.doctype.security_update_check.security_update_check import SecurityUpdateCheck
	from press.press.doctype.server_activity.server_activity import ServerActivity
	from press.press.doctype.site_activity.site_activity import SiteActivity


class ForensicEvent(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	if TYPE_CHECKING:
		from frappe.types import DF

		actor: DF.Link | None
		bench: DF.Link | None
		document_name: DF.DynamicLink
		document_type: DF.Link
		event_type: DF.Data
		job: DF.Link | None
		payload: DF.Code | None
		server: DF.Data | None
		server_type: DF.Data | None
		severity: DF.Literal["Info", "Warning", "Error", "Critical"]
		site: DF.Link | None
		source_doctype: DF.Link | None
		source_name: DF.DynamicLink | None
		status: DF.Data | None
		summary: DF.SmallText
		team: DF.Link | None
	# end: auto-generated types

	dashboard_fields = (
		"event_type",
		"severity",
		"status",
		"team",
		"document_type",
		"document_name",
		"source_doctype",
		"source_name",
		"site",
		"bench",
		"job",
		"server_type",
		"server",
		"actor",
		"summary",
	)


def create_forensic_event(**kwargs):
	payload = kwargs.pop("payload", None)
	if payload is not None:
		kwargs["payload"] = json.dumps(payload, sort_keys=True, default=str, indent=2)

	return frappe.get_doc({"doctype": "Forensic Event", **kwargs}).insert(ignore_permissions=True)


@frappe.whitelist()
def fetch_forensic_events_for_export(filters=None):
	filters = frappe.parse_json(filters) or {}
	fields = [
		"name",
		"creation",
		"severity",
		"event_type",
		"status",
		"document_type",
		"document_name",
		"team",
		"actor",
		"site",
		"bench",
		"server_type",
		"server",
		"job",
		"summary",
		"payload",
	]
	return frappe.get_all(
		"Forensic Event",
		filters=filters,
		fields=fields,
		order_by="creation desc",
		limit_page_length=5000,
	)


@frappe.whitelist()
def fetch_forensic_incident_signals(
	hours=72, min_occurrences=2, signal_state=None, peak_severity=None, team=None
):
	hours = max(int(hours or 72), 1)
	min_occurrences = max(int(min_occurrences or 2), 1)
	from_time = frappe.utils.add_to_date(frappe.utils.now_datetime(), hours=-hours, as_datetime=True)
	fields = [
		"name",
		"creation",
		"severity",
		"event_type",
		"status",
		"document_type",
		"document_name",
		"source_doctype",
		"source_name",
		"team",
		"actor",
		"site",
		"bench",
		"server_type",
		"server",
		"job",
		"summary",
	]
	filters = {"creation": (">=", from_time)}
	if team:
		filters["team"] = team

	events = frappe.get_all(
		"Forensic Event",
		filters=filters,
		fields=fields,
		order_by="creation desc",
		limit_page_length=5000,
	)

	signals = {}
	for event in events:
		target_type = event.get("document_type") or event.get("source_doctype") or "Forensic Event"
		target_name = event.get("document_name") or event.get("source_name") or event.get("name")
		event_type = event.get("event_type") or "Unknown Event"
		key = f"{target_type}::{target_name}::{event_type}"
		signal = signals.setdefault(
			key,
			{
				"name": key,
				"signal_key": key,
				"target_label": f"{target_type} {target_name}".strip(),
				"document_type": target_type,
				"document_name": target_name,
				"event_type": event_type,
				"team": event.get("team"),
				"site": event.get("site"),
				"bench": event.get("bench"),
				"server_type": event.get("server_type"),
				"server": event.get("server"),
				"job": event.get("job"),
				"count": 0,
				"first_seen": event.get("creation"),
				"last_seen": event.get("creation"),
				"peak_severity": event.get("severity") or "Info",
				"latest_severity": event.get("severity") or "Info",
				"latest_status": event.get("status"),
				"latest_summary": event.get("summary"),
				"latest_event": event.get("name"),
				"latest_actor": event.get("actor"),
				"signal_state": "Watch",
			},
		)

		signal["first_seen"] = min(signal["first_seen"], event.get("creation"))
		signal["last_seen"] = max(signal["last_seen"], event.get("creation"))
		if _severity_rank(event.get("severity")) > _severity_rank(signal["peak_severity"]):
			signal["peak_severity"] = event.get("severity") or "Info"

		if event.get("creation") >= signal["last_seen"]:
			signal["latest_severity"] = event.get("severity") or "Info"
			signal["latest_status"] = event.get("status")
			signal["latest_summary"] = event.get("summary")
			signal["latest_event"] = event.get("name")
			signal["latest_actor"] = event.get("actor")
			signal["team"] = signal["team"] or event.get("team")
			signal["site"] = signal["site"] or event.get("site")
			signal["bench"] = signal["bench"] or event.get("bench")
			signal["server_type"] = signal["server_type"] or event.get("server_type")
			signal["server"] = signal["server"] or event.get("server")
			signal["job"] = signal["job"] or event.get("job")

		if _is_signal_severity(event.get("severity")):
			signal["count"] += 1

	results = []
	for signal in signals.values():
		if signal["count"] < min_occurrences and signal["peak_severity"] != "Critical":
			continue

		signal["signal_state"] = _signal_state_for(signal["latest_severity"])
		if signal_state and signal["signal_state"] != signal_state:
			continue
		if peak_severity and signal["peak_severity"] != peak_severity:
			continue
		results.append(signal)

	results.sort(
		key=lambda signal: (
			_severity_rank(signal["peak_severity"]),
			signal["count"],
			signal["last_seen"],
		),
		reverse=True,
	)
	return results


def capture_agent_job_insert(doc: "AgentJob", _method=None):
	create_forensic_event(
		event_type="Agent Job Created",
		severity=_severity_for_job_status(doc.status),
		status=doc.status,
		team=_resolve_team(doc),
		document_type=_resolve_primary_document_type(doc),
		document_name=_resolve_primary_document_name(doc),
		source_doctype=doc.doctype,
		source_name=doc.name,
		site=doc.site,
		bench=doc.bench,
		job=doc.name,
		server_type=doc.server_type,
		server=doc.server,
		actor=doc.owner,
		summary=f"{doc.job_type} queued for { _describe_primary_target(doc) }".strip(),
		payload={
			"job_type": doc.job_type,
			"status": doc.status,
			"request_method": doc.request_method,
			"request_path": doc.request_path,
			"reference_doctype": doc.reference_doctype,
			"reference_name": doc.reference_name,
		},
	)


def capture_agent_job_update(doc: "AgentJob", _method=None):
	previous = doc.get_doc_before_save()
	if not previous:
		return

	changed_fields = {}
	for fieldname in ("status", "start", "end", "duration", "job_id"):
		before = previous.get(fieldname)
		after = doc.get(fieldname)
		if before != after:
			changed_fields[fieldname] = {"before": before, "after": after}

	if not changed_fields:
		return

	old_status = previous.get("status")
	new_status = doc.get("status")
	summary = f"{doc.job_type} updated"
	if old_status != new_status:
		summary = f"{doc.job_type}: {old_status or 'Unknown'} -> {new_status or 'Unknown'}"

	create_forensic_event(
		event_type="Agent Job Updated",
		severity=_severity_for_job_status(new_status),
		status=new_status,
		team=_resolve_team(doc),
		document_type=_resolve_primary_document_type(doc),
		document_name=_resolve_primary_document_name(doc),
		source_doctype=doc.doctype,
		source_name=doc.name,
		site=doc.site,
		bench=doc.bench,
		job=doc.name,
		server_type=doc.server_type,
		server=doc.server,
		actor=doc.modified_by,
		summary=summary,
		payload={"changes": changed_fields},
	)


def capture_site_activity_insert(doc: "SiteActivity", _method=None):
	create_forensic_event(
		event_type="Site Activity",
		severity=_severity_for_site_action(doc.action),
		status=doc.action,
		team=doc.team or frappe.db.get_value("Site", doc.site, "team"),
		document_type="Site",
		document_name=doc.site,
		source_doctype=doc.doctype,
		source_name=doc.name,
		site=doc.site,
		job=doc.job,
		actor=doc.owner,
		summary=f"{doc.action} on site {doc.site}",
		payload={"reason": doc.reason, "job": doc.job},
	)


def capture_server_activity_insert(doc: "ServerActivity", _method=None):
	create_forensic_event(
		event_type="Server Activity",
		severity=_severity_for_server_action(doc.action),
		status=doc.action,
		team=doc.team,
		document_type=doc.document_type,
		document_name=doc.document_name,
		source_doctype=doc.doctype,
		source_name=doc.name,
		server_type=doc.document_type,
		server=doc.document_name,
		actor=doc.owner,
		summary=f"{doc.action} on {doc.document_type} {doc.document_name}",
		payload={"reason": doc.reason},
	)


def capture_press_job_insert(doc: "PressJob", _method=None):
	create_forensic_event(
		event_type="Press Job Created",
		severity=_severity_for_press_job_status(doc.status),
		status=doc.status,
		team=_resolve_team(doc),
		document_type=_resolve_primary_document_type(doc),
		document_name=_resolve_primary_document_name(doc),
		source_doctype=doc.doctype,
		source_name=doc.name,
		server_type=doc.server_type,
		server=doc.server,
		actor=doc.owner,
		summary=f"{doc.job_type} press job queued for { _describe_primary_target(doc) }".strip(),
		payload={
			"job_type": doc.job_type,
			"status": doc.status,
			"virtual_machine": doc.virtual_machine,
			"callback_executed": doc.callback_executed,
		},
	)


def capture_press_job_update(doc: "PressJob", _method=None):
	previous = doc.get_doc_before_save()
	if not previous:
		return

	changed_fields = {}
	for fieldname in (
		"status",
		"start",
		"end",
		"duration",
		"callback_executed",
		"callback_failed",
		"callback_retry_limit_reached",
	):
		before = previous.get(fieldname)
		after = doc.get(fieldname)
		if before != after:
			changed_fields[fieldname] = {"before": before, "after": after}

	if not changed_fields:
		return

	old_status = previous.get("status")
	new_status = doc.get("status")
	summary = f"{doc.job_type} press job updated"
	if old_status != new_status:
		summary = f"{doc.job_type}: {old_status or 'Unknown'} -> {new_status or 'Unknown'}"

	create_forensic_event(
		event_type="Press Job Updated",
		severity=_severity_for_press_job_status(new_status),
		status=new_status,
		team=_resolve_team(doc),
		document_type=_resolve_primary_document_type(doc),
		document_name=_resolve_primary_document_name(doc),
		source_doctype=doc.doctype,
		source_name=doc.name,
		server_type=doc.server_type,
		server=doc.server,
		actor=doc.modified_by,
		summary=summary,
		payload={"changes": changed_fields},
	)


def capture_press_job_step_update(doc: "PressJobStep", _method=None):
	previous = doc.get_doc_before_save()
	if not previous or previous.get("status") == doc.status:
		return

	job = frappe.get_cached_doc("Press Job", doc.job)
	create_forensic_event(
		event_type="Press Job Step Updated",
		severity=_severity_for_press_job_step_status(doc.status),
		status=doc.status,
		team=_resolve_team(job),
		document_type="Press Job",
		document_name=doc.job,
		source_doctype=doc.doctype,
		source_name=doc.name,
		server_type=job.server_type,
		server=job.server,
		actor=doc.modified_by,
		summary=f"{doc.step_name}: {previous.get('status') or 'Unknown'} -> {doc.status or 'Unknown'}",
		payload={
			"step_name": doc.step_name,
			"job_type": doc.job_type,
			"attempts": doc.attempts,
			"result": doc.result,
			"traceback": doc.traceback,
		},
	)


def capture_security_update_check_update(doc: "SecurityUpdateCheck", _method=None):
	previous = doc.get_doc_before_save()
	if not previous or previous.get("status") == doc.status:
		return

	create_forensic_event(
		event_type="Security Update Check Updated",
		severity=_severity_for_security_update_check_status(doc.status),
		status=doc.status,
		team=frappe.db.get_value(doc.server_type, doc.server, "team") if doc.server_type and doc.server else None,
		document_type=doc.server_type or doc.doctype,
		document_name=doc.server or doc.name,
		source_doctype=doc.doctype,
		source_name=doc.name,
		server_type=doc.server_type,
		server=doc.server,
		actor=doc.modified_by,
		summary=f"Security update check on {doc.server}: {previous.get('status') or 'Unknown'} -> {doc.status or 'Unknown'}",
		payload={"play": doc.play},
	)


def _resolve_team(doc) -> str | None:
	if getattr(doc, "site", None):
		return frappe.db.get_value("Site", doc.site, "team")
	if getattr(doc, "bench", None):
		return frappe.db.get_value("Bench", doc.bench, "team")
	if getattr(doc, "server", None) and getattr(doc, "server_type", None):
		return frappe.db.get_value(doc.server_type, doc.server, "team")
	if getattr(doc, "reference_doctype", None) and getattr(doc, "reference_name", None):
		if frappe.get_meta(doc.reference_doctype).has_field("team"):
			return frappe.db.get_value(doc.reference_doctype, doc.reference_name, "team")
	return None


def _resolve_primary_document_type(doc) -> str:
	if getattr(doc, "reference_doctype", None):
		return doc.reference_doctype
	if getattr(doc, "site", None):
		return "Site"
	if getattr(doc, "bench", None):
		return "Bench"
	if getattr(doc, "server_type", None):
		return doc.server_type
	return doc.doctype


def _resolve_primary_document_name(doc) -> str:
	if getattr(doc, "reference_name", None):
		return doc.reference_name
	if getattr(doc, "site", None):
		return doc.site
	if getattr(doc, "bench", None):
		return doc.bench
	if getattr(doc, "server", None):
		return doc.server
	return doc.name


def _describe_primary_target(doc) -> str:
	document_type = _resolve_primary_document_type(doc)
	document_name = _resolve_primary_document_name(doc)
	return f"{document_type} {document_name}".strip()


def _severity_for_job_status(status: str | None) -> str:
	return {
		"Failure": "Error",
		"Delivery Failure": "Error",
		"Undelivered": "Warning",
		"Running": "Info",
		"Pending": "Info",
		"Success": "Info",
	}.get(status or "", "Info")


def _severity_for_site_action(action: str | None) -> str:
	if action in {"Suspend Site", "Archive", "Deactivate Site", "Disable Monitoring And Alerts"}:
		return "Warning"
	if action in {"Login as Administrator"}:
		return "Critical"
	return "Info"


def _severity_for_server_action(action: str | None) -> str:
	if action in {"Terminated", "Incident"}:
		return "Warning"
	return "Info"


def _severity_for_press_job_status(status: str | None) -> str:
	return {
		"Failure": "Error",
		"Skipped": "Warning",
		"Running": "Info",
		"Pending": "Info",
		"Success": "Info",
	}.get(status or "", "Info")


def _severity_for_press_job_step_status(status: str | None) -> str:
	return {
		"Failure": "Error",
		"Skipped": "Warning",
		"Running": "Info",
		"Pending": "Info",
		"Success": "Info",
	}.get(status or "", "Info")


def _severity_for_security_update_check_status(status: str | None) -> str:
	return {
		"Failure": "Critical",
		"Running": "Info",
		"Pending": "Info",
		"Success": "Info",
	}.get(status or "", "Info")


def _severity_rank(severity: str | None) -> int:
	return {
		"Info": 0,
		"Warning": 1,
		"Error": 2,
		"Critical": 3,
	}.get(severity or "Info", 0)


def _is_signal_severity(severity: str | None) -> bool:
	return _severity_rank(severity) >= _severity_rank("Warning")


def _signal_state_for(severity: str | None) -> str:
	if severity == "Critical":
		return "Open"
	if severity == "Error":
		return "Open"
	if severity == "Warning":
		return "Watch"
	return "Recovered"
