<script setup lang="ts" generic="T">
defineProps<{
    title: string
    confirmMsg: string
    confirmFn: (payload?: number | null) => Promise<void>
    errorMsg: string
    payload?: number | null
    isLoading: boolean
    isError: boolean
}>()
defineEmits<{
    (e: 'close-modal'): void
}>()
</script>

<template>
    <section class="w-[50vw] h-36 flex flex-col items-center gap-4  bg-sky-800/20 text-white">
        <div class="w-full py-2 font-semibold text-center bg-red-600/60">
                <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
                <p>{{ isLoading ? '' : isError ? errorMsg : title }}</p>
            </div>
            <p>{{ confirmMsg }}</p>
            <div class="flex items-center justify-center gap-4">
                <button 
                    class="w-16 py-1 rounded-md bg-red-600/60 hover:bg-red-600 active:shadow-inner" 
                    title="Confirm delete" 
                    @click="confirmFn(payload)">
                    Yes
                </button>
                <button 
                    class="w-16 py-1 border border-solid rounded-md border-red-600/60 hover:border-red-600" 
                    title="Cancel"
                    @click="$emit('close-modal')">
                    No
                </button>
            </div>
    </section>
</template>