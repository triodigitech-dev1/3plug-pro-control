<template>
	<div class="space-y-5">
		<div class="rounded-md border bg-white p-5">
			<div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">
						Bench Onboarding
					</p>
					<h2 class="mt-1 text-xl font-semibold text-gray-900">
						Bring an existing bench under 3plug management
					</h2>
					<p class="mt-2 max-w-3xl text-sm text-gray-600">
						This flow reuses Press's self-hosted import path. We discover the
						bench on this managed server, map its apps, then create the managed
						bench record that the rest of the product can operate on.
					</p>
				</div>
				<div class="space-y-2 text-sm text-gray-600">
					<div>
						Linked record:
						<span class="font-medium text-gray-900">{{
							state.self_hosted_server || 'Loading...'
						}}</span>
					</div>
					<div class="flex items-center gap-2">
						<span>Status</span>
						<Badge :label="state.status || 'Unknown'" />
					</div>
				</div>
			</div>
		</div>

		<div class="grid gap-5 xl:grid-cols-[minmax(0,1.25fr)_22rem]">
			<div class="space-y-5">
				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Existing Bench Source</h3>
					<p class="mt-2 text-sm text-gray-600">
						Use this when the managed server already has a bench you want 3plug
						to adopt instead of creating a fresh empty bench first.
					</p>

					<label class="mt-5 flex items-center gap-3 text-sm text-gray-700">
						<input
							v-model="form.existing_bench_present"
							type="checkbox"
							class="h-4 w-4 rounded border-gray-300 text-gray-900 focus:ring-gray-900"
						/>
						This server already has an existing bench to import
					</label>

					<div class="mt-5">
						<FormControl
							label="Bench Directory"
							type="text"
							v-model="form.bench_directory"
							placeholder="/home/frappe/frappe-bench"
						/>
						<p class="mt-2 text-xs text-gray-500">
							Use the real bench path on the target Linux server.
						</p>
					</div>

					<div class="mt-5 flex flex-wrap gap-3">
						<Button
							variant="outline"
							@click="saveConfiguration"
							:loading="$resources.saveBenchConfiguration.loading"
						>
							Save Bench Settings
						</Button>
						<Button
							variant="solid"
							@click="discoverBench"
							:loading="$resources.discoverExistingBench.loading"
						>
							Discover Existing Bench
						</Button>
						<Button
							v-if="state.release_group"
							variant="ghost"
							:route="{ name: 'Release Group Detail', params: { name: state.release_group } }"
						>
							Open Managed Bench
						</Button>
						<Button
							v-else
							variant="outline"
							@click="createManagedBench"
							:disabled="!state.can_create_release_group"
							:loading="$resources.createManagedBench.loading"
						>
							Create Managed Bench
						</Button>
					</div>

					<div
						v-if="resourceError"
						class="mt-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
					>
						{{ resourceError }}
					</div>
					<div
						v-if="statusMessage"
						class="mt-4 rounded-md border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700"
					>
						{{ statusMessage }}
					</div>
				</section>

				<section class="rounded-md border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Discovered Apps</h3>
							<p class="mt-1 text-sm text-gray-600">
								These app versions are what the existing bench is actually running.
							</p>
						</div>
						<Badge :label="`${state.app_count || 0} apps`" />
					</div>

					<div v-if="state.apps?.length" class="mt-4 space-y-3">
						<div
							v-for="app in state.apps"
							:key="`${app.app_name}-${app.branch}-${app.version}`"
							class="rounded-md border px-4 py-3"
						>
							<div class="flex items-center justify-between gap-3">
								<div class="font-medium text-gray-900">{{ app.app_name }}</div>
								<Badge :label="app.branch || 'unknown branch'" />
							</div>
							<div class="mt-1 text-sm text-gray-600">
								Version {{ app.version || 'unknown' }}
							</div>
						</div>
					</div>
					<p v-else class="mt-4 text-sm text-gray-500">
						No apps discovered yet. Run bench discovery first.
					</p>
				</section>

				<section class="rounded-md border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Discovered Sites</h3>
							<p class="mt-1 text-sm text-gray-600">
								This gives us the first inventory view before we move into site
								import or managed site operations.
							</p>
						</div>
						<Badge :label="`${state.site_count || 0} sites`" />
					</div>

					<div v-if="state.sites?.length" class="mt-4 space-y-3">
						<div
							v-for="site in state.sites"
							:key="site.site_name"
							class="rounded-md border px-4 py-3"
						>
							<div class="font-medium text-gray-900">{{ site.site_name }}</div>
							<div class="mt-1 text-sm text-gray-600">
								{{ site.apps || 'No apps recorded yet' }}
							</div>
							<div v-if="site.site" class="mt-1 text-xs text-gray-500">
								Managed site record: {{ site.site }}
							</div>
						</div>
					</div>
					<p v-else class="mt-4 text-sm text-gray-500">
						No sites discovered yet. Run bench discovery first.
					</p>
				</section>
			</div>

			<div class="space-y-5">
				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">What this unlocks</h3>
					<ul class="mt-4 space-y-3 text-sm text-gray-600">
						<li>Bench inventory becomes visible in the normal server and bench views.</li>
						<li>App versions are captured from the real server state instead of guesses.</li>
						<li>We can move next into managed site operations on top of that bench.</li>
					</ul>
				</section>

				<section class="rounded-md border bg-white p-5">
					<h3 class="text-lg font-semibold text-gray-900">Current State</h3>
					<dl class="mt-4 space-y-3 text-sm">
						<div class="flex items-center justify-between gap-4">
							<dt class="text-gray-500">Existing bench import</dt>
							<dd class="font-medium text-gray-900">
								{{ state.existing_bench_present ? 'Enabled' : 'Disabled' }}
							</dd>
						</div>
						<div class="flex items-center justify-between gap-4">
							<dt class="text-gray-500">Bench path</dt>
							<dd class="font-medium text-gray-900">
								{{ state.bench_directory || 'Not set' }}
							</dd>
						</div>
						<div class="flex items-center justify-between gap-4">
							<dt class="text-gray-500">Managed bench</dt>
							<dd class="font-medium text-gray-900">
								{{ state.release_group || 'Not created yet' }}
							</dd>
						</div>
					</dl>
				</section>
			</div>
		</div>
	</div>
</template>

<script>
import { Badge, Button, FormControl } from 'frappe-ui';

export default {
	name: 'ServerBenchOnboarding',
	components: {
		Badge,
		Button,
		FormControl,
	},
	props: {
		server: {
			type: String,
			required: true,
		},
	},
	data() {
		return {
			form: {
				existing_bench_present: false,
				bench_directory: '',
			},
			state: {},
			statusMessage: '',
		};
	},
	resources: {
		benchOnboardingState() {
			return {
				url: 'press.api.selfhosted.get_bench_onboarding_state',
				auto: true,
				makeParams: () => ({
					server: this.server,
				}),
				onSuccess: (data) => {
					this.applyState(data);
				},
			};
		},
		saveBenchConfiguration() {
			return {
				url: 'press.api.selfhosted.update_existing_bench_configuration',
				makeParams: () => ({
					server: this.server,
					existing_bench_present: this.form.existing_bench_present ? 1 : 0,
					bench_directory: this.form.bench_directory,
				}),
				onSuccess: (data) => {
					this.statusMessage = 'Bench import settings saved';
					this.applyState(data);
				},
			};
		},
		discoverExistingBench() {
			return {
				url: 'press.api.selfhosted.discover_existing_bench',
				makeParams: () => ({
					server: this.server,
					bench_directory: this.form.bench_directory,
				}),
				onSuccess: (data) => {
					this.statusMessage = data.message || 'Bench discovery started';
					this.applyState(data);
				},
			};
		},
		createManagedBench() {
			return {
				url: 'press.api.selfhosted.create_release_group_from_existing_bench',
				makeParams: () => ({
					server: this.server,
				}),
				onSuccess: (data) => {
					this.statusMessage = data.message || 'Managed bench created';
					this.applyState(data);
				},
			};
		},
	},
	computed: {
		resourceError() {
			return (
				this.$resources.benchOnboardingState.error ||
				this.$resources.saveBenchConfiguration.error ||
				this.$resources.discoverExistingBench.error ||
				this.$resources.createManagedBench.error
			);
		},
	},
	methods: {
		applyState(data) {
			this.state = data || {};
			this.form.existing_bench_present = Boolean(data?.existing_bench_present);
			this.form.bench_directory = data?.bench_directory || '';
		},
		saveConfiguration() {
			this.statusMessage = '';
			this.$resources.saveBenchConfiguration.submit();
		},
		discoverBench() {
			this.statusMessage = '';
			this.$resources.discoverExistingBench.submit();
		},
		createManagedBench() {
			this.statusMessage = '';
			this.$resources.createManagedBench.submit();
		},
	},
};
</script>
