<template>
	<div class="sticky top-0 z-10 shrink-0">
		<Header>
			<Breadcrumbs
				:items="[
					{ label: 'Servers', route: '/servers' },
					{ label: 'Register Managed Server', route: '/servers/register-managed' },
				]"
			/>
		</Header>
	</div>

	<div
		v-if="!$team.doc?.is_desk_user && !$session.hasServerCreationAccess"
		class="mx-auto mt-60 w-fit rounded-md border border-dashed px-12 py-8 text-center text-gray-600"
	>
		<lucide-alert-triangle class="mx-auto mb-4 h-6 w-6 text-red-600" />
		<ErrorMessage message="You aren't permitted to register managed servers" />
	</div>

	<div
		v-else-if="!$team.doc?.self_hosted_servers_enabled"
		class="mx-auto mt-24 max-w-3xl rounded-xl border bg-white p-8 text-gray-700"
	>
		<h2 class="text-xl font-semibold text-gray-900">
			Self-hosted server registration is not enabled
		</h2>
		<p class="mt-3 text-sm">
			This 3plug flow is meant for the single managed-server model. Enable
			self-hosted server access for this team before registering the target
			server.
		</p>
	</div>

	<div v-else class="mx-auto max-w-6xl px-5 py-8">
		<div class="grid gap-6 xl:grid-cols-[minmax(0,1.35fr)_24rem]">
			<div class="space-y-6">
				<section class="rounded-xl border bg-white p-6">
					<p class="text-sm uppercase tracking-wide text-gray-500">
						Managed Server Registration
					</p>
					<h1 class="mt-1 text-2xl font-semibold text-gray-900">
						Register the Linux server 3plug will manage
					</h1>
					<p class="mt-3 max-w-3xl text-sm text-gray-600">
						This is the one-server path for 3plug. We verify the app and
						database hosts, create the Press records, and hand the operator into
						the server job flow.
					</p>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Server Details</h2>
					<div class="mt-5 grid gap-5 md:grid-cols-2">
						<FormControl
							label="Server Title"
							type="text"
							v-model="form.title"
							placeholder="Triotek Production Server"
						/>
						<div>
							<p class="text-sm font-medium text-gray-900">Default Plan</p>
							<div class="mt-2 rounded-lg border bg-gray-50 px-4 py-3 text-sm text-gray-700">
								{{ planLabel }}
							</div>
						</div>
						<FormControl
							label="Application Public IP"
							type="text"
							v-model="form.app_public_ip"
							placeholder="203.0.113.10"
						/>
						<FormControl
							label="Application Private IP"
							type="text"
							v-model="form.app_private_ip"
							placeholder="10.0.0.10"
						/>
						<FormControl
							label="Database Public IP"
							type="text"
							v-model="form.db_public_ip"
							placeholder="203.0.113.11"
						/>
						<FormControl
							label="Database Private IP"
							type="text"
							v-model="form.db_private_ip"
							placeholder="10.0.0.11"
						/>
					</div>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<div class="flex items-start justify-between gap-4">
						<div>
							<h2 class="text-lg font-semibold text-gray-900">
								Verification Access
							</h2>
							<p class="mt-2 text-sm text-gray-600">
								The target hosts must allow the default SSH key so 3plug can
								verify connectivity and minimum specs.
							</p>
						</div>
						<Button
							v-if="sshKey"
							variant="ghost"
							@click="copySshKey"
						>
							Copy SSH Key
						</Button>
					</div>
					<pre
						class="mt-4 overflow-auto rounded-lg bg-gray-950 p-4 text-xs leading-6 text-gray-100"
					>{{ sshKey || 'Loading SSH key...' }}</pre>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<div class="flex items-start justify-between gap-4">
						<div>
							<h2 class="text-lg font-semibold text-gray-900">Create Record</h2>
							<p class="mt-2 text-sm text-gray-600">
								This verifies both hosts, creates the self-hosted server record,
								and starts setup against the managed server model.
							</p>
						</div>
						<Button
							variant="solid"
							@click="registerServer"
							:loading="$resources.registerManagedServer.loading"
						>
							Register Managed Server
						</Button>
					</div>
					<div
						v-if="$resources.registerManagedServer.error"
						class="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
					>
						{{ $resources.registerManagedServer.error }}
					</div>
				</section>
			</div>

			<div class="space-y-6">
				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">Readiness Checks</h2>
					<ul class="mt-4 space-y-3 text-sm text-gray-600">
						<li>SSH access must work from 3plug to both application and database hosts.</li>
						<li>Private IPs must actually belong to the target machines.</li>
						<li>Minimum baseline remains 4 GB RAM, 2 vCPU, and 40+ GB storage.</li>
						<li>Docker is assumed available and not currently a special blocker.</li>
					</ul>
				</section>

				<section class="rounded-xl border bg-white p-6">
					<h2 class="text-lg font-semibold text-gray-900">What happens next</h2>
					<ul class="mt-4 space-y-3 text-sm text-gray-600">
						<li>3plug creates the managed server records.</li>
						<li>The platform verifies host reachability and core specs.</li>
						<li>Setup jobs become visible on the server detail page.</li>
						<li>After that, we move into bench and site operations.</li>
					</ul>
				</section>
			</div>
		</div>
	</div>
</template>

<script>
import { FormControl, Breadcrumbs, Button, ErrorMessage } from 'frappe-ui';
import Header from '../components/Header.vue';

export default {
	name: 'RegisterManagedServer',
	components: {
		Breadcrumbs,
		Button,
		ErrorMessage,
		FormControl,
		Header,
	},
	data() {
		return {
			form: {
				title: '',
				app_public_ip: '',
				app_private_ip: '',
				db_public_ip: '',
				db_private_ip: '',
			},
		};
	},
	resources: {
		managedServerOptions() {
			return {
				url: 'press.api.selfhosted.options_for_new',
				auto: true,
			};
		},
		registerManagedServer() {
			return {
				url: 'press.api.selfhosted.create_and_verify_selfhosted',
				makeParams: () => ({
					server: {
						...this.form,
						plan: this.defaultPlan,
					},
				}),
				validate: () => {
					for (const [key, value] of Object.entries(this.form)) {
						if (!value) {
							throw new Error(`${this.prettyLabel(key)} is required`);
						}
					}
					if (!this.defaultPlan) {
						throw new Error('No self-hosted server plan is available');
					}
				},
				onSuccess: (server) => {
					this.$router.push({
						name: 'Server Detail Plays',
						params: { name: server },
					});
				},
			};
		},
	},
	computed: {
		sshKey() {
			return this.$resources.managedServerOptions.data?.ssh_key || '';
		},
		defaultPlan() {
			return this.$resources.managedServerOptions.data?.plans?.[0] || null;
		},
		planLabel() {
			if (!this.defaultPlan) return 'No self-hosted plan found';
			return this.$format.planTitle(this.defaultPlan);
		},
	},
	methods: {
		prettyLabel(key) {
			return key.replaceAll('_', ' ').replace(/\b\w/g, (char) => char.toUpperCase());
		},
		async copySshKey() {
			if (!this.sshKey) return;
			await navigator.clipboard.writeText(this.sshKey);
		},
		registerServer() {
			this.$resources.registerManagedServer.submit();
		},
	},
};
</script>
