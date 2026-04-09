import { createResource } from 'frappe-ui';
import { unparse } from 'papaparse';
import { icon } from '../../utils/components';

function getSeverityTheme(value) {
	return {
		Info: 'blue',
		Warning: 'yellow',
		Error: 'red',
		Critical: 'red',
	}[value] || 'gray';
}

export function getForensicColumns() {
	return [
		{
			label: 'Summary',
			fieldname: 'summary',
			class: 'font-medium',
			width: 2,
		},
		{
			label: 'Severity',
			fieldname: 'severity',
			type: 'Badge',
			width: '120px',
			theme: getSeverityTheme,
		},
		{
			label: 'Event',
			fieldname: 'event_type',
			width: 1.2,
		},
		{
			label: 'Target',
			fieldname: 'document_name',
			width: 1.2,
			format(value, row) {
				if (!value) {
					return row.document_type || '';
				}
				return row.document_type ? `${row.document_type} ${value}` : value;
			},
		},
		{
			label: 'Actor',
			fieldname: 'actor',
			width: 0.8,
		},
		{
			label: 'Status',
			fieldname: 'status',
			width: 0.8,
			format(value) {
				return value || '';
			},
		},
		{
			label: '',
			fieldname: 'creation',
			type: 'Timestamp',
			align: 'right',
		},
	];
}

export function getForensicFilterControls() {
	return [
		{
			type: 'select',
			label: 'Severity',
			fieldname: 'severity',
			options: ['', 'Info', 'Warning', 'Error', 'Critical'],
		},
		{
			type: 'select',
			label: 'Event',
			fieldname: 'event_type',
			options: [
				'',
				'Agent Job Created',
				'Agent Job Updated',
				'Site Activity',
				'Server Activity',
			],
		},
		{
			type: 'select',
			label: 'Target',
			fieldname: 'document_type',
			options: ['', 'Site', 'Bench', 'Server', 'Database Server', 'Agent Job'],
		},
	];
}

export function exportForensicEvents(listResource) {
	const exportResource = createResource({
		url: 'press.press.doctype.forensic_event.forensic_event.fetch_forensic_events_for_export',
		makeParams() {
			return {
				filters: listResource?.filters || {},
			};
		},
	});

	return exportResource.submit().then((rows) => {
		const fields = [
			'creation',
			'severity',
			'event_type',
			'status',
			'document_type',
			'document_name',
			'team',
			'actor',
			'site',
			'bench',
			'server_type',
			'server',
			'job',
			'summary',
			'payload',
		];
		let csv = unparse({
			fields,
			data: rows || [],
		});
		csv = '\uFEFF' + csv;

		const blob = new Blob([csv], {
			type: 'text/csv;charset=utf-8',
		});
		const today = new Date().toISOString().split('T')[0];
		const link = document.createElement('a');
		link.href = URL.createObjectURL(blob);
		link.download = `forensic-events-${today}.csv`;
		link.click();
		URL.revokeObjectURL(link.href);
	});
}

export function getForensicTab(filters) {
	return {
		label: 'Forensics',
		icon: icon('file-search'),
		route: 'forensics',
		type: 'list',
		list: {
			doctype: 'Forensic Event',
			filters,
			orderBy: 'creation desc',
			fields: [
				'creation',
				'severity',
				'event_type',
				'status',
				'document_type',
				'document_name',
				'actor',
				'team',
				'site',
				'bench',
				'server_type',
				'server',
				'job',
				'summary',
			],
			columns: getForensicColumns(),
			filterControls: getForensicFilterControls,
			route(row) {
				return {
					name: 'Forensic Event Detail',
					params: { name: row.name },
				};
			},
			moreActions({ listResource }) {
				return [
					{
						label: 'Export as CSV',
						icon: 'download',
						onClick() {
							exportForensicEvents(listResource);
						},
					},
				];
			},
		},
	};
}
