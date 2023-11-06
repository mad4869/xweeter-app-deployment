<script setup lang="ts">
import { TransitionRoot } from '@headlessui/vue';

defineProps<{
    show: boolean,
    category: 'success' | 'error' | undefined | null
    message: string,
}>()

const colors = {
    success: 'bg-sky-600',
    error: 'bg-red-600',
}

const icons = {
    success: 'fa-solid fa-clipboard-check',
    error: 'fa-solid fa-triangle-exclamation'
}
</script>

<template>
    <TransitionRoot
        :show="show"
        as="div" 
        class="fixed flex items-center gap-4 px-4 py-2 text-white -translate-x-1/2 rounded-md left-1/2 bottom-4" 
        :class="category ? colors[category] : ''"
        enter="transition-all duration-200 ease-out"
        enter-from="opacity-0 translate-y-4"
        enter-to="opacity-100 translate-y-0"
        leave="transition-all duration-150 ease-in"
        leave-from="opacity-100 translate-y-0"
        leave-to="opacity-0 translate-y-4">
        <div>
            <font-awesome-icon 
                :icon="category ? icons[category] : ''" beat-fade 
                class="text-sm" />
        </div>
        <div class="flex-1">
            <p>{{ message }}</p>
        </div>
    </TransitionRoot>
</template>