<script setup lang="ts">
defineProps({
    isLoading: {
        type: Boolean,
        default: false
    }
})
</script>

<template>
    <section class="flex justify-center items-center">
        <div class="w-1/2 py-2 bg-sky-800 text-sky-400 text-center rounded-full">
            <font-awesome-icon 
                v-if="isLoading"
                icon="fa-solid fa-circle-notch" spin />
            {{ !isLoading ? 'More Xweets' : '' }}
        </div>
    </section>
</template>