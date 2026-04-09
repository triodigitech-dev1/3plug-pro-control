<template>
	<div class="space-y-6">
		<div class="rounded-xl border bg-white p-6">
			<div class="flex flex-wrap items-start justify-between gap-4">
				<div>
					<p class="text-sm uppercase tracking-wide text-gray-500">
						3plug Control Center
					</p>
					<h2 class="mt-1 text-2xl font-semibold text-gray-900">
						Single-server operations at a glance
					</h2>
					<p class="mt-2 max-w-3xl text-sm text-gray-600">
						This is the core operator surface for the managed server, its benches,
						sites, jobs, and forensic signals.
					</p>
				</div>
				<div class="flex flex-wrap gap-2">
					<Button variant="solid" :route="{ name: 'Register Managed Server' }">
						Register server
					</Button>
					<Button :route="{ name: 'New Site' }">Create site</Button>
					<Button :route="'/forensics/signals'">Review signals</Button>
				</div>
			</div>
		</div>

		<div class="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
			<div
				v-for="card in summaryCards"
				:key="card.label"
				class="rounded-xl border bg-white p-5"
			>
				<p class="text-sm text-gray-500">{{ card.label }}</p>
				<p class="mt-3 text-3xl font-semibold text-gray-900">
					{{ card.value }}
				</p>
				<p class="mt-2 text-sm text-gray-600">{{ card.helper }}</p>
			</div>
		</div>

		<div class="grid gap-6 xl:grid-cols-[1.3fr_minmax(0,1fr)]">
			<div class="space-y-6">
				<section class="rounded-xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Managed Server</h3>
							<p class="mt-1 text-sm text-gray-600">
								The server side of the product should stay visible and simple.
							</p>
						</div>
						<Button variant="ghost" :route="{ name: 'Server List' }">
							View servers
						</Button>
					</div>
					<div v-if="servers.length" class="mt-4 space-y-3">
						<router-link
							v-for="server in servers"
							:key="server.name"
							:to="{ name: 'Server Detail Overview', params: { name: server.name } }"
							class="flex items-center justify-between rounded-lg border px-4 py-3 transition hover:bg-gray-50"
						>
							<div>
								<p class="font-medium text-gray-900">
									{{ server.title || server.name }}
								</p>
								<p class="mt-1 text-sm text-gray-600">
									{{ server.name }}
									<span v-if="server.cluster">in {{ server.cluster }}</span>
								</p>
							</div>
							<Badge :label="server.status" />
						</router-link>
					</div>
					<p v-else class="mt-4 text-sm text-gray-600">
						No managed server is visible yet.
					</p>
				</section>

				<section class="rounded-xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Benches</h3>
							<p class="mt-1 text-sm text-gray-600">
								Bench inventory is the real runtime backbone behind site operations.
							</p>
						</div>
						<Button variant="ghost" :route="{ name: 'Bench List' }">
							View benches
						</Button>
					</div>
					<div v-if="benches.length" class="mt-4 space-y-3">
						<router-link
							v-for="bench in benches"
							:key="bench.name"
							:to="{ name: 'Bench Detail Overview', params: { name: bench.name } }"
							class="flex items-center justify-between rounded-lg border px-4 py-3 transition hover:bg-gray-50"
						>
							<div>
								<p class="font-medium text-gray-900">{{ bench.name }}</p>
								<p class="mt-1 text-sm text-gray-600">
									{{ bench.server }}
									<span v-if="bench.group">under {{ bench.group }}</span>
								</p>
							</div>
							<Badge :label="bench.status" />
						</router-link>
					</div>
					<p v-else class="mt-4 text-sm text-gray-600">
						No benches are available yet.
					</p>
				</section>

				<section class="rounded-xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Sites</h3>
							<p class="mt-1 text-sm text-gray-600">
								These are the current managed sites across the available benches.
							</p>
						</div>
						<Button variant="ghost" :route="{ name: 'Site List' }">
							View sites
						</Button>
					</div>
					<div v-if="sites.length" class="mt-4 space-y-3">
						<router-link
							v-for="site in sites"
							:key="site.name"
							:to="{ name: 'Site Detail Overview', params: { name: site.name } }"
							class="flex items-center justify-between rounded-lg border px-4 py-3 transition hover:bg-gray-50"
						>
							<div>
								<p class="font-medium text-gray-900">
									{{ site.host_name || site.name }}
								</p>
								<p class="mt-1 text-sm text-gray-600">
									{{ site.name }}
									<span v-if="site.bench">on {{ site.bench }}</span>
								</p>
							</div>
							<Badge :label="site.status" />
						</router-link>
					</div>
					<p v-else class="mt-4 text-sm text-gray-600">
						No sites are registered yet.
					</p>
				</section>
			</div>

			<div class="space-y-6">
				<section class="rounded-xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">Active Jobs</h3>
							<p class="mt-1 text-sm text-gray-600">
								Operator actions should always be visible as tracked jobs.
							</p>
						</div>
					</div>
					<div v-if="recentJobs.length" class="mt-4 space-y-3">
						<component
							v-for="job in recentJobs"
							:key="job.name"
							:is="jobRoute(job) ? 'router-link' : 'div'"
							:to="jobRoute(job)"
							class="block rounded-lg border px-4 py-3 transition hover:bg-gray-50"
						>
							<div class="flex items-center justify-between gap-4">
								<div>
									<p class="font-medium text-gray-900">{{ job.job_type }}</p>
									<p class="mt-1 text-sm text-gray-600">
										{{ job.site || job.bench || job.server || 'No target recorded' }}
									</p>
								</div>
								<Badge :label="job.status" />
							</div>
							<p class="mt-2 text-xs text-gray-500">
								{{ formatTimestamp(job.creation) }}
							</p>
						</component>
					</div>
					<p v-else class="mt-4 text-sm text-gray-600">
						No recent jobs yet.
					</p>
				</section>

				<section class="rounded-xl border bg-white p-5">
					<div class="flex items-center justify-between gap-4">
						<div>
							<h3 class="text-lg font-semibold text-gray-900">
								Forensic Signals
							</h3>
							<p class="mt-1 text-sm text-gray-600">
								Repeated failures are grouped here so the operator can focus.
							</p>
						</div>
						<Button variant="ghost" :route="'/forensics/signals'">
							View all
						</Button>
					</div>
					<div v-if="recentSignals.length" class="mt-4 space-y-3">
						<router-link
							v-for="signal in recentSignals"
							:key="signal.signal_key"
							:to="{ name: 'Forensic Event Detail', params: { name: signal.latest_event } }"
							class="block rounded-lg border px-4 py-3 transition hover:bg-gray-50"
						>
							<div class="flex items-center justify-between gap-4">
								<div>
									<p class="font-medium text-gray-900">
										{{ signal.target_label }}
									</p>
									<p class="mt-1 text-sm text-gray-600">
										{{ signal.event_type }}
									</p>
								</div>
								<div class="text-right">
									<Badge :label="signal.signal_state" />
									<p class="mt-1 text-xs text-gray-500">
										{{ signal.count }} hits
									</p>
								</div>
							</div>
						</router-link>
					</div>
					<p v-else class="mt-4 text-sm text-gray-600">
						No repeated forensic signals in the current review window.
					</p>
				</section>
			</div>
		</div>
	</div>
</template>

<script>
import { Badge } from 'frappe-ui';
import { getForensicJobRoute } from '../utils/forensics';

export default {
	name: 'HomeSummary',
	components: {
		Badge,
	},
	resources: {
		home() {
			if (!this.$team.doc?.name) return;
			return {
				url: 'press.api.client.run_doc_method',
				cache: ['home_data', this.$team.doc.name],
				makeParams() {
					return {
						dt: 'Team',
						dn: this.$team.doc.name,
						method: 'get_home_data',
					};
				},
				auto: true,
			};
		},
	},
	computed: {
		data() {
			return this.$resources.home.data?.message || {};
		},
		summary() {
			return this.data.summary || {};
		},
		servers() {
			return this.data.servers || [];
		},
		benches() {
			return this.data.benches || [];
		},
		sites() {
			return this.data.sites || [];
		},
		recentJobs() {
			return this.data.recent_jobs || [];
		},
		recentSignals() {
			return this.data.recent_signals || [];
		},
		summaryCards() {
			return [
				{
					label: 'Managed Servers',
					value: this.summary.server_count || 0,
					helper: `${this.summary.active_server_count || 0} active`,
				},
				{
					label: 'Benches',
					value: this.summary.bench_count || 0,
					helper: `${this.summary.active_bench_count || 0} active, ${this.summary.broken_bench_count || 0} broken`,
				},
				{
					label: 'Sites',
					value: this.summary.site_count || 0,
					helper: `${this.summary.active_site_count || 0} active, ${this.summary.broken_site_count || 0} broken`,
				},
				{
					label: 'Active Jobs',
					value: this.summary.active_job_count || 0,
					helper: 'Tracked execution for current operations',
				},
				{
					label: 'Open Signals',
					value: this.summary.open_signal_count || 0,
					helper: 'Repeated failures needing operator review',
				},
			];
		},
	},
	methods: {
		jobRoute(job) {
			return getForensicJobRoute(job);
		},
		formatTimestamp(value) {
			if (!value) return 'Not recorded';
			return this.$format.date(value, 'lll');
		},
	},
};
</script>
