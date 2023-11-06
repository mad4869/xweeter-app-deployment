<script setup lang="ts">
defineProps<{
    msg?: string,
    submsg?: string
}>()
</script>

<template>
    <section
        class="flex flex-col items-center justify-center gap-2 px-4 py-4 border border-solid bg-sky-600/10 backdrop-blur-lg text-sky-600 border-sky-800 rounded-xl">
        <h3 v-if="msg" class="text-xl font-bold">{{ msg }}</h3>
        <h6 v-if="submsg">{{ submsg }}</h6>
    </section>
</template>