import { defineAsyncComponent } from 'vue';
import { getForensicColumns, getForensicFilterControls, exportForensicEvents } from './common/forensics';
import { icon } from '../utils/components';

export default {
	doctype: 'Forensic Event',
	whitelistedMethods: {},
	list: {
		route: '/forensics',
		title: 'Forensics',
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
		orderBy: 'creation desc',
		searchField: 'summary',
		filterControls: getForensicFilterControls,
		columns: getForensicColumns(),
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
	detail: {
		titleField: 'name',
		route: '/forensics/:name',
		statusBadge({ documentResource }) {
			return {
				label: documentResource.doc?.severity || 'Info',
			};
		},
		tabs: [
			{
				label: 'Overview',
				icon: icon('file-search'),
				route: 'overview',
				type: 'Component',
				component: defineAsyncComponent(
					() => import('../components/forensics/ForensicEventOverview.vue'),
				),
				props: (documentResource) => ({
					document: documentResource.doc,
				}),
			},
		],
		actions() {
			return [];
		},
	},
	routes: [],
};
