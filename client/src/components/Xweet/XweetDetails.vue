<script setup lang="ts">
import { ref, Ref } from 'vue';

import Replies from './Replies.vue';
import Xweet from '@/components/App/Xweet/index.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import { useFetchList } from '@/composables/useFetch';
import useAuthStore from '@/stores/useAuthStore';
import { XweetDetail } from '@/types/xweets';
import { LikeDetail } from '@/types/likes'
import { RexweetDetail } from '@/types/rexweets'

defineProps<{
    data: XweetDetail | undefined | null
    repliesFiltered: boolean
    deletedXweet?: number | null
    deletedReply?: number | null
    showDeleteXweetModal: (xweetId: number) => void
    showDeleteReplyModal: (replyId: number) => void
    showNotice: (category: 'success' | 'error', msg: string) => void
}>()

const authStore = useAuthStore()

const userLikes: Ref<number[]> = ref([])
const userRexweets: Ref<number[]> = ref([])

if (authStore.getIsAuthenticated) {
    const userLikesData = await useFetchList<LikeDetail>(
        `/api/users/${authStore.getSignedInUserId}/likes`, true
        )
    const userRexweetsData = await useFetchList<RexweetDetail>(
        `/api/users/${authStore.getSignedInUserId}/rexweets`, true
    )

    userLikesData.list.value?.forEach(like => {
        userLikes.value.push(like.xweet_id)
    })
    userRexweetsData.list.value?.forEach(rexweet => {
        userRexweets.value.push(rexweet.xweet_id)
    })
}

const isRepliable = ref(false)
const showReplyEditor = (xweetId: number | null) => {
    if (!xweetId) {
        isRepliable.value = false
    } else {
        isRepliable.value = true
    }
}

const xweetHasBeenReplied = ref(false)
const closeReply = () => {
    xweetHasBeenReplied.value = true
    isRepliable.value = false

    setTimeout(() => {
        xweetHasBeenReplied.value = false
    }, 2000)
}
</script>

<template>
    <section class="flex flex-col">
        <Xweet
            :key="data?.xweet_id"
            :id="data?.xweet_id!"
            :userId="data?.user_id!"
            :fullname="data?.full_name!" 
            :username="data?.username!" 
            :body="data?.body!" 
            :media="data?.media"
            :profilePic="data?.profile_pic" 
            :createdAt="data?.created_at!" 
            :updated-at="data?.updated_at" 
            :is-own="data?.user_id === authStore.getSignedInUserId" 
            :is-replied="xweetHasBeenReplied"
            :rexweeted="userRexweets.includes(data?.xweet_id as number)"
            :liked="userLikes.includes(data?.xweet_id as number)"
            @show-notice="showNotice"
            @reply="showReplyEditor"
            @delete="showDeleteXweetModal" />
        <ReplyXweet
            class="mt-4" 
            :show="isRepliable"
            :xweet-id="(data?.xweet_id as number)"
            @close-reply="closeReply" />
        <Replies
            :is-filtered="repliesFiltered"
            :deleted-reply="deletedReply"
            :show-delete-reply-modal="showDeleteReplyModal"
            :show-notice="showNotice" />
    </section>
</template>