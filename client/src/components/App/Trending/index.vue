<script setup lang="ts">
import Hashtag from './Hashtag.vue';
import Empty from '@/components/App/Empty.vue';
import { Trending } from '@/types/hashtags'
import { useFetchList } from '@/composables/useFetch';

const hashtags = await useFetchList<Trending>('api/trending', false)
</script>

<template>
    <section 
        class="flex flex-col flex-1 gap-4 overflow-hidden border border-solid border-sky-800 rounded-xl">
        <div class="flex items-center justify-between px-4 py-2 bg-sky-600">
            <span class="font-semibold text-white">Trending</span>
            <font-awesome-icon icon="fa-solid fa-globe" class="text-white" />
        </div>
        <div class="px-4 overflow-scroll">
            <Hashtag 
                v-for="hashtag in hashtags.list.value" 
                :key="hashtag.hashtag_id" 
                :body="hashtag.body"
                :xweet-count="hashtag.xweet_count" />
            <Empty v-if="hashtags.list?.value?.length === 0" submsg="There are no trending topics for now" />
        </div>
    </section>
</template>