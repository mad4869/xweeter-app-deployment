<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useScroll } from '@vueuse/core';

import Sep from '@/components/App/Sep.vue';
import Xweet from '@/components/App/Xweet/index.vue';
import MoreXweet from '@/components/App/Xweet/MoreXweet.vue';
import { useFetchList } from '@/composables/useFetch';
import useAuthStore from '@/stores/useAuthStore';
import socket from '@/utils/socket';
import { Reply } from '@/types/replies'

const props = defineProps<{
    isFiltered: boolean
    deletedReply?: number | null
    showDeleteReplyModal: (xweetId: number) => void
    showNotice: (category: 'success' | 'error', msg: string) => void
}>()

const authStore = useAuthStore()

const route = useRoute()

const isLoading = ref(false)

const start = ref(0)
const repliesData = await useFetchList<Reply>(`/api/xweets/${route.params.id}/replies?start=${start.value}`, false)
const replies = repliesData.list

socket.on('add_to_replies', (reply) => {
    replies.value?.push(reply)
})

watch(() => props.isFiltered, () => {
    if (props.isFiltered) {
        const index = replies.value?.findIndex(reply => reply.reply_id === props.deletedReply)
        if (index !== -1) {
            replies.value?.splice((index as number), 1)
        }
    }
})

const repliesRef = ref<HTMLElement | null>(null)
const { arrivedState } = useScroll(repliesRef)
const needMoreXweet = ref((replies.value?.length ?? 0) > 4)

watch(() => arrivedState.bottom, async () => {
    if (needMoreXweet) {
        start.value+= 10
        isLoading.value = true
    
        const newRepliesData = await useFetchList<Reply>(
            `/api/xweets/${route.params.id}/replies?start=${start.value}`, false
        )
        const newReplies = newRepliesData.list
        isLoading.value = false
    
        if (newReplies.value?.length === 0) {
            needMoreXweet.value = false
        } else {
            replies.value?.push(...newReplies.value as Reply[])
        }
    }
})
</script>

<template>
    <Sep v-if="(replies?.length ?? 0) > 0" title="Replies" is-sticky />
    <section class="flex flex-col gap-2 max-h-screen overflow-y-scroll scrollbar-hide" ref="repliesRef">
        <Xweet v-for="reply in replies"
            :key="reply.xweet_id"
            :id="reply.reply_id!"
            :userId="reply.user_id!"
            :fullname="reply.full_name!" 
            :username="reply.username!" 
            :body="reply.body!" 
            :media="reply.media"
            :profilePic="reply.profile_pic" 
            :createdAt="reply.created_at!" 
            :updated-at="reply.updated_at" 
            :is-own="reply.user_id === authStore.getSignedInUserId" 
            :is-reply="true"
            :rexweeted="false"
            :liked="false"
            @show-notice="showNotice"
            @delete="showDeleteReplyModal" />
        <MoreXweet v-if="needMoreXweet" :is-loading="isLoading" />
    </section>
</template>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none; 
    scrollbar-width: none;
}
</style>