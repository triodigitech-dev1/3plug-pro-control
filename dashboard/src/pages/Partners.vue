<template>
	<div class="flex h-full flex-col">
		<div class="sticky top-0 z-10 shrink-0">
			<Header>
				<FBreadcrumbs
					:items="[{ label: 'Partnership', route: { name: 'Partnership' } }]"
				/>
			</Header>
		</div>
		<div
			class="mx-auto mt-60 w-fit rounded border border-dashed px-12 py-8 text-center text-gray-600"
		>
			<lucide-alert-triangle class="mx-auto mb-4 h-6 w-6 text-red-600" />
			<ErrorMessage
				message="Partner-program surfaces are deferred in 3plug v1 while the imported Press scope is being reduced."
			/>
		</div>
	</div>
</template>

<script>
import Header from '../components/Header.vue';
import { Breadcrumbs } from 'frappe-ui';

export default {
	name: 'Partner',
	components: {
		Header,
		FBreadcrumbs: Breadcrumbs,
	},
};
</script>
