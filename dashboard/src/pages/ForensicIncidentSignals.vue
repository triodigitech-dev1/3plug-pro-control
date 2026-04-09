<template>
	<div class="flex h-full flex-col">
		<Header :sticky="true">
			<Breadcrumbs
				:items="[
					{ label: 'Forensics', route: '/forensics' },
					{ label: 'Incident Signals', route: '/forensics/signals' },
				]"
			/>
		</Header>
		<div class="p-5">
			<div class="mb-5 rounded-lg border bg-white p-5">
				<div class="flex flex-wrap items-start justify-between gap-4">
					<div>
						<p class="text-sm text-gray-500">Forensic Incident Signals</p>
						<h1 class="mt-1 text-2xl font-semibold text-gray-900">
							Repeated failures worth operator attention
						</h1>
						<p class="mt-2 max-w-3xl text-sm text-gray-600">
							This view groups forensic events by target and event type so
							repeated failures show up as one signal instead of a noisy flat log.
						</p>
					</div>
					<div class="grid gap-2 text-sm text-gray-600 sm:text-right">
						<p>
							<span class="font-medium text-gray-900">{{ summary.open }}</span>
							open
						</p>
						<p>
							<span class="font-medium text-gray-900">{{ summary.watch }}</span>
							watch
						</p>
						<p>
							<span class="font-medium text-gray-900">{{ summary.recovered }}</span>
							recovered
						</p>
					</div>
				</div>
			</div>

			<ObjectList :options="listOptions" />
		</div>
	</div>
</template>

<script>
import Header from '../components/Header.vue';
import ObjectList from '../components/ObjectList.vue';
import { Breadcrumbs } from 'frappe-ui';
import { getForensicDocumentRoute } from '../utils/forensics';

function stateTheme(value) {
	return {
		Open: 'red',
		Watch: 'yellow',
		Recovered: 'green',
	}[value] || 'gray';
}

function severityTheme(value) {
	return {
		Info: 'blue',
		Warning: 'yellow',
		Error: 'red',
		Critical: 'red',
	}[value] || 'gray';
}

export default {
	name: 'ForensicIncidentSignals',
	components: {
		Header,
		Breadcrumbs,
		ObjectList,
	},
	data() {
		return {
			filters: {
				hours: '72',
				min_occurrences: '2',
				signal_state: '',
				peak_severity: '',
			},
		};
	},
	resources: {
		signals() {
			return {
				url: 'press.press.doctype.forensic_event.forensic_event.fetch_forensic_incident_signals',
				makeParams: () => this.$resources.signals?.params || this.filters,
				auto: true,
			};
		},
	},
	computed: {
		summary() {
			const rows = this.$resources.signals.data || [];
			return rows.reduce(
				(acc, row) => {
					if (row.signal_state === 'Open') acc.open += 1;
					if (row.signal_state === 'Watch') acc.watch += 1;
					if (row.signal_state === 'Recovered') acc.recovered += 1;
					return acc;
				},
				{ open: 0, watch: 0, recovered: 0 },
			);
		},
		listOptions() {
			return {
				resource: () => this.$resources.signals,
				columns: [
					{
						label: 'Signal',
						fieldname: 'target_label',
						class: 'font-medium',
						width: 1.5,
						link(value, row) {
							return getForensicDocumentRoute(row.document_type, row.document_name);
						},
					},
					{
						label: 'Event',
						fieldname: 'event_type',
						width: 1.1,
					},
					{
						label: 'State',
						fieldname: 'signal_state',
						type: 'Badge',
						width: '120px',
						theme: stateTheme,
					},
					{
						label: 'Peak',
						fieldname: 'peak_severity',
						type: 'Badge',
						width: '120px',
						theme: severityTheme,
					},
					{
						label: 'Hits',
						fieldname: 'count',
						width: '80px',
					},
					{
						label: 'Latest Summary',
						fieldname: 'latest_summary',
						width: 2,
					},
					{
						label: 'Last Seen',
						fieldname: 'last_seen',
						type: 'Timestamp',
						align: 'right',
					},
				],
				filterControls: () => [
					{
						type: 'select',
						label: 'Window',
						fieldname: 'hours',
						options: [
							{ label: '24 hours', value: '24' },
							{ label: '72 hours', value: '72' },
							{ label: '7 days', value: '168' },
						],
						default: '72',
					},
					{
						type: 'select',
						label: 'Min Hits',
						fieldname: 'min_occurrences',
						options: [
							{ label: '2+', value: '2' },
							{ label: '3+', value: '3' },
							{ label: '5+', value: '5' },
						],
						default: '2',
					},
					{
						type: 'select',
						label: 'State',
						fieldname: 'signal_state',
						options: ['', 'Open', 'Watch', 'Recovered'],
					},
					{
						type: 'select',
						label: 'Peak Severity',
						fieldname: 'peak_severity',
						options: ['', 'Warning', 'Error', 'Critical'],
					},
				],
				searchField: null,
				route: (row) => ({
					name: 'Forensic Event Detail',
					params: { name: row.latest_event },
				}),
				moreActions: () => [
					{
						label: 'Open Raw Event Stream',
						icon: 'list',
						onClick: () => this.$router.push('/forensics'),
					},
				],
				emptyStateMessage:
					'No repeated forensic signals in the selected window.',
				banner: () => ({
					title: 'What counts as a signal?',
					text: 'Signals group repeated warning, error, and critical forensic events by target and event type. Critical events appear even on the first hit.',
					theme: 'blue',
				}),
			};
		},
	},
};
</script>
