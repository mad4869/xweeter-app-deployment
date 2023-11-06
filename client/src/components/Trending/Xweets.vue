<script setup lang="ts">
import { ref, Ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useScroll } from '@vueuse/core';

import Xweet from '@/components/App/Xweet/index.vue';
import ReplyXweet from '@/components/App/Xweet/ReplyXweet.vue';
import MoreXweet from '@/components/App/Xweet/MoreXweet.vue';
import Empty from '@/components/App/Empty.vue';
import { useFetchList } from '@/composables/useFetch';
import useAuthStore from '@/stores/useAuthStore';
import { XweetDetail } from '@/types/xweets';
import { LikeDetail } from '@/types/likes'
import { RexweetDetail } from '@/types/rexweets'

const props = defineProps<{
    isFiltered: boolean
    deletedXweet?: number | null
    showDeleteModal: (xweetId: number) => void
    showNotice: (category: 'success' | 'error', msg: string) => void
}>()

const authStore = useAuthStore()

const route = useRoute()

const isLoading = ref(false)

const start = ref(0)
const trendingData = await useFetchList<XweetDetail>(`/api/hashtags/${route.query.tag}`, false)
const trending = trendingData.list

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

watch(() => props.isFiltered, () => {
    if (props.isFiltered) {
        const index = trending.value?.findIndex(xweet => xweet.xweet_id === props.deletedXweet)
        if (index !== -1) {
            trending.value?.splice((index as number), 1)
        }
    }
})

watch(() => route.query.tag, async () => {
    const newTrendingData = await useFetchList<XweetDetail>(`/api/hashtags/${route.query.tag}`, false)
    trending.value = newTrendingData.list.value
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

const trendingRef = ref<HTMLElement | null>(null)
const { arrivedState } = useScroll(trendingRef)
const needMoreXweet = ref((trending.value?.length ?? 0) > 4)

watch(() => arrivedState.bottom, async () => {
    if (needMoreXweet) {
        start.value+= 10
        isLoading.value = true
    
        const newTrendingData = await useFetchList<XweetDetail>(
            `/api/hashtags/${route.query.tag}?start=${start.value}`, false
        )
        const newTrending = newTrendingData.list
        isLoading.value = false
    
        if (newTrending.value?.length === 0) {
            needMoreXweet.value = false
        } else {
            trending.value?.push(...newTrending.value as XweetDetail[])
        }
    }
})
</script>

<template>
    <section class="flex flex-col max-h-screen gap-4 overflow-y-scroll scrollbar-hide" ref="trendingRef">
        <div v-for="xweet in trending">
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
                :rexweeted="userRexweets.includes(xweet.xweet_id)"
                :liked="userLikes.includes(xweet.xweet_id)"
                @show-notice="showNotice"
                @reply="(xweetId) => { xweetToReply = xweetId }"
                @delete="showDeleteModal" />
            <ReplyXweet 
                :show="xweetToReply === xweet.xweet_id"
                :xweet-id="xweet.xweet_id"
                @close-reply="closeReply" />
        </div>
        <MoreXweet v-if="needMoreXweet" :is-loading="isLoading" />
        <Empty 
            v-if="trending?.length === 0"
            msg="There are no xweets regarding this topic yet" />
    </section>
</template>