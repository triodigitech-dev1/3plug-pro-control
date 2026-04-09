<template>
	<div
		class="mx-auto mt-60 w-fit rounded border border-dashed px-12 py-8 text-center text-gray-600"
	>
		<lucide-alert-triangle class="mx-auto mb-4 h-6 w-6 text-red-600" />
		<ErrorMessage
			message="Partner admin tooling is deferred in 3plug v1 while the imported Press surface is being reduced."
		/>
	</div>
</template>

<script setup lang="ts">
defineOptions({ name: 'PartnerAdmin' });
</script>
