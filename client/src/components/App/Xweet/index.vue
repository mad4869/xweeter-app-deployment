<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { RouterLink } from 'vue-router';
import { useDateFormat } from '@vueuse/core';

import ImageViewer from './ImageViewer.vue';
import EditXweet from './EditXweet.vue';
import useRenderXweet from '@/composables/useRenderXweet';
import useTimestamp from '@/composables/useTimestamp';
import useCount, { Features } from '@/composables/useCount';
import useAuthStore from '@/stores/useAuthStore';
import { sendReqCookie } from '@/utils/axiosInstances';
import { RexweetResponse } from '@/types/rexweets';
import { LikeResponse } from '@/types/likes'

const props = defineProps<{
    id: number
    userId: number
    fullname?: string
    username?: string
    body: string
    media?: string
    profilePic?: string
    createdAt: string
    updatedAt?: string
    ogUserId?: number
    ogUsername?: string
    ogFullname?: string
    ogProfilePic?: string
    isOwn: boolean
    isRexweet?: boolean
    isLike?: boolean
    isReply?: boolean
    isReplied?: boolean
    rexweeted: boolean
    liked: boolean
}>()

const emit = defineEmits<{
    (e: 'show-notice', category: 'success' | 'error', msg: string): void,
    (e: 'reply', xweet_id: number | null): void
    (e: 'delete', xweet_id: number): void
}>()

const authStore = useAuthStore()

const isImageEnlarged = ref(false)
const isRexweeted = ref(props.rexweeted)
const isLiked = ref(props.liked)
const isEditable = ref(false)
const isRepliable = ref(false)

const xweet = ref(props.body)
const xweetText = computed(() => useRenderXweet(xweet.value))
const xweetMedia = ref(props.media)
const xweetTimestamp = ref(useTimestamp(props.createdAt))
const xweetUpdatedTimestamp = ref(useTimestamp(props.updatedAt))
const xweetRepliesCount = await useCount('xweets', props.id, Features.Replies)
const xweetRexweetsCount = await useCount('xweets', props.id, Features.Rexweets)
const xweetLikesCount = await useCount('xweets', props.id, Features.Likes)

const rexweet = async () => {
    if (!authStore.getIsAuthenticated || props.isOwn) {
        return
    }

    isRexweeted.value = !isRexweeted.value
    
    if (isRexweeted.value) {
        xweetRexweetsCount.value++
        try {
            const { data } = await sendReqCookie.post<RexweetResponse | undefined>(
                `/api/users/${authStore.getSignedInUserId}/xweets/${props.id}/rexweets`
            )
    
            if (data?.success) {
                emit('show-notice', 'success', `You rexweeted ${props.isRexweet || props.isLike ? props.ogUsername : props.username}'s xweet`)
            }
        } catch (err) {
            isRexweeted.value = false
            xweetRexweetsCount.value--
    
            emit('show-notice', 'error', 'Failed to rexweet: error occured during the process')
        }
    } else {
        xweetRexweetsCount.value--

        try {
            const { data } = await sendReqCookie.delete<RexweetResponse | undefined>(
                `/api/users/${authStore.getSignedInUserId}/xweets/${props.id}/rexweets`
            )

            if (data?.success) {
                emit('show-notice', 'success', `You unrexweeted ${props.isRexweet || props.isLike ? props.ogUsername : props.username}'s xweet`)
            }
        } catch (err) {
            isRexweeted.value = true
            xweetRexweetsCount.value++

            emit('show-notice', 'error', 'Failed to unrexweet: error occured during the process')
        }
    }
}

const switchRepliable = () => {
    if (!authStore.getIsAuthenticated) {
        return
    }
    
    isRepliable.value = !isRepliable.value
    
    if (isRepliable.value) {
        emit('reply', props.id)
    } else {
        emit('reply', null)
    }
}

watch(() => props.isReplied, () => {
    if (props.isReplied) {
        isRepliable.value = false
    }
})

const likeXweet = async () => {
    if (!authStore.getIsAuthenticated) {
        return
    }

    isLiked.value = true
    xweetLikesCount.value++

    try {
        const { data } = await sendReqCookie.post<LikeResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${props.id}/likes`
        )

        if (data?.success) {
            emit('show-notice', 'success', `You liked ${props.isRexweet || props.isLike ? props.ogUsername : props.username}'s xweet`)
        }
    } catch (err) {
        isLiked.value = false
        xweetLikesCount.value--

        emit('show-notice', 'error', 'Failed to like xweet: error occured during the process')
    }
}

const unlikeXweet = async () => {
    if (!authStore.getIsAuthenticated) {
        return
    }

    isLiked.value = false
    xweetLikesCount.value--

    try {
        const { data } = await sendReqCookie.delete<LikeResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${props.id}/likes`
        )

        if (data?.success) {
            emit('show-notice', 'success', `You unliked ${props.isRexweet || props.isLike ? props.ogUsername : props.username}'s xweet`)
        }
    } catch (err) {
        isLiked.value = true
        xweetLikesCount.value++

        emit('show-notice', 'error', 'Failed to unlike xweet: error occured during the process')
    }
} 

const updateXweet = (newBody: string, newMedia?: string, updateDate?: string) => {
    xweet.value = newBody
    xweetMedia.value = newMedia
    xweetUpdatedTimestamp.value = useTimestamp(updateDate)
    isEditable.value = false
}
</script>

<template>
    <section
        class="flex justify-center gap-4 px-4 py-4 border border-solid bg-sky-600/10 backdrop-blur-lg border-sky-800 rounded-xl">
        <router-link
            :to="`/users/${isRexweet || isLike ? ogUserId : userId}`"
            class="flex flex-col items-center flex-1 w-20 gap-2 px-4 border-r border-solid border-sky-600/20 wrap-balance">
            <img 
                :src="isRexweet || isLike ? ogProfilePic : profilePic"
                class="object-cover w-10 h-10 border border-solid rounded-full border-sky-800" 
                loading="lazy" />
            <div class="flex flex-col items-center justify-center text-center">
                <p class="font-semibold text-sky-600">{{ isRexweet || isLike ? ogFullname : fullname }}</p>
                <p class="text-sm text-sky-800">@{{ isRexweet || isLike ? ogUsername : username }}</p>
            </div>
        </router-link>
        <div class="flex flex-col w-4/5 h-full gap-2">
            <div 
                class="flex items-center justify-between text-xs text-sky-900">
                <p class="flex items-center gap-1">
                    <span class="cursor-help" :title="useDateFormat(createdAt, 'D-M-YYYY HH:mm').value">
                        {{ xweetTimestamp }}
                    </span>
                    <em 
                        v-if="xweetUpdatedTimestamp" 
                        class="cursor-help" 
                        :title="useDateFormat(updatedAt, 'D-M-YYYY HH:mm').value">
                        - Updated {{ xweetUpdatedTimestamp }}
                    </em>
                </p>
                <span class="flex items-center justify-center gap-4 text-sm">
                    <span v-if="!isReply" class="flex items-center gap-1">
                        <font-awesome-icon
                            v-if="!isRepliable"
                            icon="fa-regular fa-comment"
                            class="transition-transform"
                            :class="authStore.getIsAuthenticated ? 'cursor-pointer hover:text-sky-600 hover:scale-105' : 'cursor-not-allowed'"
                            :title="authStore.getIsAuthenticated ? 'Reply to this xweet' : 'You need to login to use this feature'"
                            @click="switchRepliable" />
                        <font-awesome-icon
                            v-else
                            icon="fa-solid fa-comment"
                            class="transition-transform scale-105 cursor-pointer text-sky-600"
                            :class="authStore.getIsAuthenticated ? 'cursor-pointer' : 'cursor-not-allowed'"
                            :title="authStore.getIsAuthenticated ? 'Cancel reply' : 'You need to login to use this feature'"
                            @click="switchRepliable" />
                        <router-link 
                            :to="`/xweets/${id}`"
                            v-if="xweetRepliesCount"  
                            class="text-xs" 
                            title="View replies">
                            {{ xweetRepliesCount }}
                        </router-link>
                    </span>
                    <span v-if="!isReply" class="flex items-center gap-1">
                        <font-awesome-icon 
                            icon="fa-solid fa-retweet" 
                            class="transition-transform"
                            :class="{
                                'text-sky-600 scale-105': isRexweeted,
                                'cursor-pointer hover:text-sky-600 hover:scale-105': !isOwn && authStore.getIsAuthenticated,
                                'cursor-not-allowed': isOwn || !authStore.getIsAuthenticated
                                }"
                            :title="authStore.getIsAuthenticated && !isOwn && !isRexweeted ? 'Rexweet' :
                                    authStore.getIsAuthenticated && isOwn ? 'You can\'t rexweet your own xweet' :
                                    authStore.getIsAuthenticated && isRexweeted ? 'Unrexweet' :
                                    'You need to login to use this feature'"
                            @click="rexweet" />
                        <span 
                            v-if="xweetRexweetsCount" 
                            class="text-xs"
                            :class="isRexweeted ? 'text-sky-600' : 'text-sky-800'">
                            {{ xweetRexweetsCount }}
                        </span>
                    </span>
                    <span v-if="!isReply" class="flex items-center gap-1">
                        <font-awesome-icon 
                            v-if="!isLiked"
                            icon="fa-regular fa-heart"
                            class="transition-transform"
                            :class="authStore.getIsAuthenticated ? 'cursor-pointer hover:text-sky-600 hover:scale-105' : 'cursor-not-allowed'"
                            :title="authStore.getIsAuthenticated ? 'Like this xweet' : 'You need to login to use this feature'"
                            @click="likeXweet" />
                        <font-awesome-icon
                            v-else
                            icon="fa-solid fa-heart"
                            class="scale-105 text-sky-600"
                            :class="authStore.getIsAuthenticated ? 'cursor-pointer' : 'cursor-not-allowed'"
                            :title="authStore.getIsAuthenticated ? 'Unlike this xweet' : 'You need to login to use this feature'"
                            @click="unlikeXweet" />
                        <span 
                            v-if="xweetLikesCount" 
                            class="text-xs"
                            :class="isLiked ? 'text-sky-600' : 'text-sky-800'">
                            {{ xweetLikesCount }}
                        </span>
                    </span>
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn && !isEditable"
                        icon="fa-regular fa-pen-to-square"
                        class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                        :title="!isReply ? 'Edit this xweet' : 'Edit this reply'"
                        @click="() => { isEditable = true }"
                        />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn && isEditable"
                        icon="fa-solid fa-pen-to-square"
                        class="scale-105 cursor-pointer text-sky-600"
                        title="Cancel edit"
                        @click="() => { isEditable = false }" />
                    <font-awesome-icon
                        v-if="authStore.getIsAuthenticated && isOwn"
                        icon="fa-regular fa-trash-can"
                        class="transition-transform cursor-pointer hover:text-red-600 hover:scale-105"
                        :title="!isReply ? 'Delete this xweet' : 'Delete this reply'"
                        @click="$emit('delete', id)"
                        />
                </span>
            </div>
            <div 
                class="text-sky-800 dark:text-white">
                <Transition mode="out-in">
                    <div v-if="!isEditable" class="flex flex-col gap-2">
                        <router-link :to="`/xweets/${id}`" class="break-words">
                            <template v-for="(word, index) in xweetText">
                                <component 
                                    :is="word.type" 
                                    :to="word.to"
                                    :title="word.type === RouterLink ? `View ${word.text}` : ''" 
                                    :class="word.type === RouterLink ? 'text-sky-400 dark:text-sky-600 hover:text-sky-900 dark:hover:text-sky-400' : 'text-sky-900 dark:text-white'">
                                    {{ word.text }}
                                </component>
                                <span v-if="index < xweet.length - 1" v-html="`&nbsp;`" />
                            </template>
                        </router-link>
                        <div class="flex-shrink-0">
                            <img 
                                :src="xweetMedia" 
                                v-if="xweetMedia"
                                alt="Media" 
                                class="rounded-md max-h-60 cursor-zoom-in" 
                                loading="lazy"
                                @click="() => { isImageEnlarged = true }">
                        </div>
                    </div>
                    <EditXweet
                        v-else
                        :key="id"
                        :xweet_id="id" 
                        :body="xweet" 
                        :file-url="xweetMedia"
                        :is-reply="isReply" 
                        @update-xweet="updateXweet" />
                </Transition>
            </div>
            <div></div>
        </div>
    </section>
    <ImageViewer 
        :show="isImageEnlarged" 
        :username="username!"
        :fullname="fullname!"
        :body="xweet"
        :profile-pic="profilePic!"
        :file-url="xweetMedia!" 
        :is-own="isOwn"
        :is-rexweeted="isRexweeted"
        :is-liked="isLiked"
        :is-reply="isReply"
        :rexweet-count="xweetRexweetsCount"
        :like-count="xweetLikesCount"
        @clicked-outside="isImageEnlarged = false"
        @rexweet="rexweet"
        @like-xweet="likeXweet"
        @unlike-xweet="unlikeXweet"
        />
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
.wrap-balance {
    overflow-wrap: anywhere;
}
</style>