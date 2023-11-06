<script setup lang="ts">
defineProps<{
    keywords: string
}>()
defineEmits<{
    (e: 'update:keywords', value: string): void
}>()
</script>

<template>
    <section class="flex items-center pl-2 ml-4 overflow-hidden border border-solid rounded-md text-sky-800 dark:text-white border-sky-800 max-w-fit focus-within:ring-1 focus-within:ring-sky-600">
        <input 
            id="search-bar"
            name="search-bar"
            type="text"
            :value="keywords" 
            @input="$emit('update:keywords', ($event.target as HTMLInputElement).value)"
            class="bg-transparent focus:outline-none" />
        <div class="px-2 py-1 rounded-sm bg-sky-600">
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" class="text-white" />
        </div>
    </section>
</template>