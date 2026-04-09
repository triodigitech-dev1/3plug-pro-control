import time

import frappe
from dns.resolver import Resolver
from frappe.utils import cint
from frappe.utils import strip

from press.api.server import plans
from press.runner import Ansible
from press.utils import get_current_team
from press.utils.dns import NAMESERVERS


@frappe.whitelist()
def new(server):
	server_details = frappe._dict(server)

	team = get_current_team(get_doc=True)
	validate_team(team)

	proxy_server = get_proxy_server_for_cluster()

	return create_self_hosted_server(server_details, team, proxy_server)


def create_self_hosted_server(server_details, team, proxy_server):
	try:
		self_hosted_server = frappe.new_doc(
			"Self Hosted Server",
			**{
				"ip": strip(server_details.get("app_public_ip", "")),
				"private_ip": strip(server_details.get("app_private_ip", "")),
				"mariadb_ip": strip(server_details.get("db_public_ip", "")),
				"mariadb_private_ip": strip(server_details.get("db_private_ip", "")),
				"title": server_details.title,
				"proxy_server": proxy_server,
				"proxy_created": True,
				"different_database_server": True,
				"team": team.name,
				"plan": server_details.plan["name"],
				"database_plan": server_details.plan["name"],
				"new_server": True,
			},
		).insert()
	except frappe.DuplicateEntryError as e:
		# Exception return  tupple like ('Self Hosted Server', 'SHS-00018.cloud.pressonprem.com')
		return e.args[1]

	return self_hosted_server.name


def validate_team(team):
	if not team:
		frappe.throw("You must be part of a team to create a new server")

	if not team.enabled:
		frappe.throw("You cannot create a new server because your account is disabled")

	if not team.self_hosted_servers_enabled:
		frappe.throw(
			"You cannot create a new server because Hybrid Cloud is disabled for your account. Please contact support to enable it."
		)


def get_proxy_server_for_cluster(cluster=None):
	cluster = cluster if cluster else get_hybrid_cluster()

	return frappe.get_all("Proxy Server", {"cluster": cluster}, pluck="name")[0]


def get_hybrid_cluster():
	return frappe.db.get_value("Cluster", {"hybrid": 1}, "name")


@frappe.whitelist()
def sshkey():
	return frappe.db.get_value("SSH Key", {"enabled": 1, "default": 1}, "public_key")


@frappe.whitelist()
def verify(server):
	server_doc = frappe.get_doc("Self Hosted Server", server)

	app_server_verified = verify_server("app", server_doc)
	db_server_verified = verify_server("db", server_doc)

	if app_server_verified and db_server_verified:
		server_doc.check_minimum_specs()

		server_doc.status = "Pending"
		server_doc.save()

		server_doc.reload()
		server_doc.create_database_server()

		server_doc.reload()
		server_doc.create_application_server()
		return True

	return False


def verify_server(server_type, server_doc):
	ping = Ansible(
		playbook="ping.yml",
		server=frappe._dict(
			{
				"doctype": "Self Hosted Server",
				"name": server_doc.name,
				"ssh_user": server_doc.ssh_user,
				"ssh_port": server_doc.ssh_port,
				"ip": server_doc.ip if server_type == "app" else server_doc.mariadb_ip,
			}
		),
	)
	result = ping.run()

	if result.status == "Success":
		server_doc.validate_private_ip(result.name, server_type=server_type)

		server_doc.fetch_system_specifications(result.name, server_type=server_type)
		server_doc.reload()

		return True

	return False


@frappe.whitelist()
def setup(server):
	server_doc = frappe.get_doc("Self Hosted Server", server)
	server_doc.start_setup = True
	server_doc.save()
	server_doc.setup_server()
	time.sleep(1)


@frappe.whitelist()
def get_plans():
	return plans("Self Hosted Server")


@frappe.whitelist()
def check_dns(domain, ip):
	try:
		resolver = Resolver(configure=False)
		resolver.nameservers = NAMESERVERS
		domain_ip = resolver.query(domain.strip(), "A")[0].to_text()
		if domain_ip == ip:
			return True
	except Exception:
		return False
	return False


@frappe.whitelist()
def options_for_new():
	return {"plans": get_plans(), "ssh_key": sshkey()}


@frappe.whitelist()
def create_and_verify_selfhosted(server):
	self_hosted_server_name = new(server)

	if verify(self_hosted_server_name):
		setup(self_hosted_server_name)
		return frappe.get_value("Self Hosted Server", self_hosted_server_name, "server")

	frappe.throw("Server verification failed. Please check the server details and try again.")
	return None


def _get_self_hosted_server_for_managed_server(server: str):
	frappe.get_doc("Server", server)
	self_hosted_server_name = frappe.db.get_value("Self Hosted Server", {"server": server}, "name")
	if not self_hosted_server_name:
		frappe.throw("No linked self-hosted server record was found for this managed server")
	return frappe.get_doc("Self Hosted Server", self_hosted_server_name)


def _serialize_self_hosted_bench_state(self_hosted_server):
	play_servers = [value for value in [self_hosted_server.name, self_hosted_server.server] if value]
	recent_plays = frappe.get_all(
		"Ansible Play",
		filters={"server": ("in", play_servers)},
		fields=["name", "play", "status", "creation", "server"],
		order_by="creation desc",
		limit=8,
	)
	return {
		"self_hosted_server": self_hosted_server.name,
		"server": self_hosted_server.server,
		"status": self_hosted_server.status,
		"existing_bench_present": bool(self_hosted_server.existing_bench_present),
		"bench_directory": self_hosted_server.bench_directory,
		"release_group": self_hosted_server.release_group,
		"app_count": len(self_hosted_server.apps or []),
		"site_count": len(self_hosted_server.sites or []),
		"apps": [
			{
				"app_name": row.app_name,
				"branch": row.branch,
				"version": row.version,
			}
			for row in self_hosted_server.apps or []
		],
		"sites": [
			{
				"site_name": row.site_name,
				"apps": row.apps,
				"site": row.site,
			}
			for row in self_hosted_server.sites or []
		],
		"can_discover": bool(
			self_hosted_server.existing_bench_present and self_hosted_server.bench_directory
		),
		"can_create_release_group": bool(
			self_hosted_server.existing_bench_present
			and self_hosted_server.bench_directory
			and self_hosted_server.apps
			and not self_hosted_server.release_group
		),
		"can_create_sites": bool(self_hosted_server.release_group and self_hosted_server.sites),
		"can_restore_files": bool(
			self_hosted_server.release_group
			and self_hosted_server.bench_directory
			and any(row.site for row in self_hosted_server.sites or [])
		),
		"recent_plays": recent_plays,
	}


@frappe.whitelist()
def get_bench_onboarding_state(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	return _serialize_self_hosted_bench_state(self_hosted_server)


@frappe.whitelist()
def update_existing_bench_configuration(
	server: str, existing_bench_present: int | str = 0, bench_directory: str | None = None
):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	self_hosted_server.existing_bench_present = cint(existing_bench_present)
	self_hosted_server.bench_directory = strip(bench_directory or "") or None
	if self_hosted_server.existing_bench_present and not self_hosted_server.bench_directory:
		frappe.throw("Bench directory is required when importing an existing bench")
	self_hosted_server.save()
	return _serialize_self_hosted_bench_state(self_hosted_server)


@frappe.whitelist()
def discover_existing_bench(server: str, bench_directory: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	self_hosted_server.existing_bench_present = 1
	self_hosted_server.bench_directory = strip(bench_directory or "")
	if not self_hosted_server.bench_directory:
		frappe.throw("Bench directory is required to inspect an existing bench")
	self_hosted_server.save()
	self_hosted_server.fetch_apps_and_sites()
	self_hosted_server.reload()
	state = _serialize_self_hosted_bench_state(self_hosted_server)
	state["message"] = "Bench discovery has started. Refresh shortly to inspect discovered apps and sites."
	return state


@frappe.whitelist()
def create_release_group_from_existing_bench(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	if not self_hosted_server.existing_bench_present:
		frappe.throw("Enable existing-bench import before creating a managed bench")
	if not self_hosted_server.bench_directory:
		frappe.throw("Bench directory is required before creating a managed bench")
	if not self_hosted_server.apps:
		frappe.throw("Discover the existing bench apps before creating a managed bench")
	if self_hosted_server.release_group:
		return _serialize_self_hosted_bench_state(self_hosted_server)
	self_hosted_server.create_new_rg()
	self_hosted_server.reload()
	state = _serialize_self_hosted_bench_state(self_hosted_server)
	state["message"] = "Managed bench created from the discovered existing bench"
	return state


@frappe.whitelist()
def create_sites_from_existing_bench(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	if not self_hosted_server.release_group:
		frappe.throw("Create the managed bench before importing sites from it")
	if not self_hosted_server.sites:
		frappe.throw("Discover the existing bench sites before importing them")
	self_hosted_server.create_new_sites()
	self_hosted_server.reload()
	state = _serialize_self_hosted_bench_state(self_hosted_server)
	state["message"] = "Managed site records created from the discovered bench sites"
	return state


@frappe.whitelist()
def restore_site_files_from_existing_bench(server: str):
	self_hosted_server = _get_self_hosted_server_for_managed_server(server)
	if not self_hosted_server.release_group:
		frappe.throw("Create the managed bench before restoring site files")
	if not self_hosted_server.bench_directory:
		frappe.throw("Bench directory is required before restoring site files")
	if not any(row.site for row in self_hosted_server.sites or []):
		frappe.throw("Create the managed site records before restoring site files")
	self_hosted_server.restore_files()
	self_hosted_server.reload()
	state = _serialize_self_hosted_bench_state(self_hosted_server)
	state["message"] = "Site file restoration has started. Track the related plays for progress."
	return state
