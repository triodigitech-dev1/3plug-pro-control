# Copyright (c) 2026, Triotek and contributors
# For license information, please see license.txt
from __future__ import annotations

import json
from typing import TYPE_CHECKING

import frappe
from frappe.model.document import Document

if TYPE_CHECKING:
	from press.press.doctype.agent_job.agent_job import AgentJob
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
