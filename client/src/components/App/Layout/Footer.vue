<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<template>
    <footer 
        class="flex items-center justify-center py-8 border-t border-solid text-sky-800 border-sky-800 dark:text-slate-400">
        <section class="flex flex-col justify-center w-3/5 gap-1">
            <p class="text-xl font-semibold">Xweeter</p>
            <p class="text-xs">Copyright {{ year }}</p>
        </section>
    </footer>
</template>