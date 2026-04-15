from frappe import _


def get_data():
	return [
		{
			"label": _("Runtime"),
			"items": [
				{"type": "doctype", "name": "Self Hosted Server"},
				{"type": "doctype", "name": "Bench"},
				{"type": "doctype", "name": "Site"},
				{"type": "doctype", "name": "Server"},
			],
		},
		{
			"label": _("Execution And Evidence"),
			"items": [
				{"type": "doctype", "name": "Agent Job"},
				{"type": "doctype", "name": "Forensic Event"},
				{"type": "doctype", "name": "Ansible Play"},
				{"type": "doctype", "name": "Press Job"},
			],
		},
		{
			"label": _("Apps"),
			"items": [
				{"type": "doctype", "name": "App"},
				{"type": "doctype", "name": "App Source"},
				{"type": "doctype", "name": "App Release"},
			],
		},
		{
			"label": _("Administration"),
			"items": [
				{"type": "doctype", "name": "Team"},
				{"type": "doctype", "name": "Press Settings"},
				{"type": "doctype", "name": "Site Plan"},
				{"type": "doctype", "name": "Server Plan"},
			],
		},
	]
