<script setup lang="ts">
defineProps<{
    id: number,
    fullname: string,
    username: string,
    lastXweet: string,
    profilePic: string
}>()
</script>

<template>
    <section class="flex flex-col items-center gap-1 px-4 py-1">
        <router-link :to="`/users/${id}`" 
            class="grid w-full grid-cols-4 grid-rows-2"
            :title="`View @${username}'s profile`">
            <div class="flex items-center col-span-1 col-start-1 row-span-2 row-start-1">
                <img 
                    :src="profilePic" 
                    alt="Profile Pic"
                    class="object-cover w-8 h-8 border border-solid rounded-full border-sky-800" 
                    loading="lazy">
            </div>
            <div class="col-span-3 col-start-2 row-span-1 row-start-1 text-sm font-bold text-sky-600">
                {{ fullname }}
            </div>
            <div class="col-span-3 col-start-2 row-span-1 row-start-2 text-sm text-sky-600">
                @{{ username }}
            </div>
        </router-link>
        <div 
            class="flex flex-col justify-center w-full gap-1 px-2 py-1 text-xs rounded-sm bg-sky-900 dark:bg-white/5">
            <span class="px-1 rounded bg-sky-800 dark:bg-slate-800 w-fit py text-sky-400 dark:text-slate-600">Last Xweet</span>
            <p class="px-1 italic text-white">{{ lastXweet }}</p>
        </div>
    </section>
</template>