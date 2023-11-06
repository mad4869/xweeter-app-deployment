<script setup lang="ts">
defineProps<{
    body: string,
    xweetCount: number
}>()
</script>

<template>
    <div class="flex flex-col items-center gap-1 px-4 py-1">
        <div class="w-full text-sm font-bold text-sky-800 dark:text-sky-600">
            <router-link :to="`/trending?tag=${body}`">{{ body }}</router-link>
        </div>
        <div class="w-full text-xs text-slate-600 dark:text-slate-400">
            {{ xweetCount }} {{ xweetCount === 1 ? 'xweet' : 'xweets' }} in the last week
        </div>
    </div>
</template>