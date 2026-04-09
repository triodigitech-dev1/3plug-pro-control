<template>
	<div class="sticky top-0 z-10 shrink-0">
		<Header>
			<FBreadcrumbs
				:items="[{ label: 'Billing', route: { name: 'Billing' } }]"
			/>
		</Header>
		<div
			class="mx-auto mt-60 w-fit rounded border border-dashed px-12 py-8 text-center text-gray-600"
		>
			<lucide-alert-triangle class="mx-auto mb-4 h-6 w-6 text-red-600" />
			<ErrorMessage
				message="Billing self-service is deferred in 3plug v1 while the Press base is being trimmed."
			/>
		</div>
	</div>
</template>
<script>
import { Breadcrumbs } from 'frappe-ui';
import Header from '../components/Header.vue';

export default {
	name: 'Billing',
	components: {
		Header,
		FBreadcrumbs: Breadcrumbs,
	},
};
</script>
