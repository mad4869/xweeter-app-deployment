<script setup lang="ts">
import { ref, watch, Ref } from 'vue';
import { useScroll } from '@vueuse/core';

import Xweet from '@/components/App/Xweet/index.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import MoreXweet from '@/components/App/Xweet/MoreXweet.vue';
import Empty from '@/components/App/Empty.vue';
import { useFetchList } from '@/composables/useFetch';
import useAuthStore from '@/stores/useAuthStore';
import { XweetDetail } from '@/types/xweets';
import { LikeDetail } from '@/types/likes';
import { RexweetDetail } from '@/types/rexweets'
import socket from '@/utils/socket';

const props = defineProps<{
    y: number
    isFiltered: boolean
    deletedXweet?: number | null
    showDeleteModal: (xweetId: number) => void
    showNotice: (category: 'success' | 'error', msg: string) => void
}>()

const authStore = useAuthStore()

const isLoading = ref(false)

const start = ref(0)
let timeline: Ref<XweetDetail[] | null | undefined> = ref([])
const likes: Ref<number[]> = ref([])
const rexweets: Ref<number[]> = ref([])

if (authStore.getIsAuthenticated) {
    const timelineData = await useFetchList<XweetDetail>(
        `/api/users/${authStore.getSignedInUserId}/timeline?start=${start.value}`, true
        )
    const likesData = await useFetchList<LikeDetail>(
        `/api/users/${authStore.getSignedInUserId}/likes?start=${start.value}`, true
        )
    const rexweetsData = await useFetchList<RexweetDetail>(
        `/api/users/${authStore.getSignedInUserId}/rexweets`, true
    )

    timeline = timelineData.list

    likesData.list?.value?.forEach(like => {
        likes.value.push(like.xweet_id)
    })
    rexweetsData.list?.value?.forEach(rexweet => {
        rexweets.value.push(rexweet.xweet_id)
    })
} else {
    const timelineData = await useFetchList<XweetDetail>(
        `/api/timeline?start=${start.value}`, false
        )
    timeline = timelineData.list
}

socket.on('add_to_timeline', (xweet) => {
    timeline.value?.unshift(xweet)
})

watch(() => props.isFiltered, () => {
    if (props.isFiltered) {
        const index = timeline.value?.findIndex(xweet => xweet.xweet_id === props.deletedXweet)
        if (index !== -1) {
            timeline.value?.splice((index as number), 1)
        }
    }
})

const xweetToReply = ref<number | null>()
const xweetHasBeenReplied = ref(false)
const closeReply = () => {
    xweetToReply.value = null
    xweetHasBeenReplied.value = true

    setTimeout(() => {
        xweetHasBeenReplied.value = false
    }, 2000)
}

const el = ref<HTMLElement | null>(null)
const { arrivedState } = useScroll(el)
const needMoreXweet = ref((timeline.value?.length ?? 0) > 4)

watch(() => arrivedState.bottom, async () => {
    if (needMoreXweet) {
        start.value+= 10
        isLoading.value = true
        
        let newTimeline: Ref<XweetDetail[] | null | undefined> = ref([])

        if (authStore.getIsAuthenticated) {
            const newTimelineData = await useFetchList<XweetDetail>(
                `/api/users/${authStore.getSignedInUserId}/timeline?start=${start.value}`, true
            )
            newTimeline = newTimelineData.list
        } else {
            const newTimelineData = await useFetchList<XweetDetail>(
                `/api/timeline?start=${start.value}`, true
            )
            newTimeline = newTimelineData.list
        }
    
        isLoading.value = false

        if (newTimeline.value?.length === 0) {
            needMoreXweet.value = false
        } else {
            timeline.value?.push(...newTimeline.value as XweetDetail[])
        }
    }
})
</script>

<template>
    <section class="flex flex-col max-h-screen gap-4 overflow-y-scroll scrollbar-hide" ref="el">
        <div v-for="xweet in timeline">
            <Xweet
                :key="xweet.xweet_id" 
                :id="xweet.xweet_id" 
                :userId="xweet.user_id"
                :fullname="xweet.full_name" 
                :username="xweet.username" 
                :body="xweet.body" 
                :media="xweet.media"
                :profilePic="xweet.profile_pic" 
                :createdAt="xweet.created_at" 
                :updated-at="xweet.updated_at" 
                :is-rexweet="false"
                :is-own="xweet.user_id === authStore.getSignedInUserId" 
                :is-replied="xweetHasBeenReplied"
                :rexweeted="rexweets.includes(xweet.xweet_id)"
                :liked="likes.includes(xweet.xweet_id)"
                @show-notice="showNotice"
                @reply="xweetId => { xweetToReply = xweetId }"
                @delete="showDeleteModal" />
            <ReplyXweet 
                :show="xweetToReply === xweet.xweet_id"
                :xweet-id="xweet.xweet_id"
                @close-reply="closeReply" />
        </div>
        <MoreXweet v-if="needMoreXweet" :is-loading="isLoading" />
        <Empty 
            v-if="timeline?.length === 0"
            msg="This is where your timeline would appear" 
            submsg="Start following some people to get contents to your desire!" />
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