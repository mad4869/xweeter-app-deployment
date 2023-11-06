<script setup lang="ts">
import { ref } from 'vue';
import { onClickOutside } from '@vueuse/core';

import useAuthStore from '@/stores/useAuthStore';
import { TransitionRoot } from '@headlessui/vue';

defineProps<{
    show: boolean
    username?: string
    fullname?: string
    profilePic?: string
    body?: string
    fileUrl?: string
    isOwn: boolean
    isRexweeted: boolean
    isLiked: boolean
    isReply?: boolean
    rexweetCount: number
    likeCount: number
}>()

const emit = defineEmits<{
    (e: 'clicked-outside'): void
    (e: 'rexweet'): void
    (e: 'like-xweet'): void
    (e: 'unlike-xweet'): void
}>()

const authStore = useAuthStore()

const imgRef = ref<HTMLDivElement | null>(null)

onClickOutside(imgRef, () => {
    emit('clicked-outside')
})
</script>

<template>
    <TransitionRoot
        :show="show"
        as="div" 
        class="fixed top-0 bottom-0 left-0 right-0 z-40 flex flex-col items-center justify-center gap-4 bg-black/5 backdrop-blur-md"
        enter="transition-opacity ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="transition-opacity ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0">
        <div class="relative group" ref="imgRef">
            <img 
                :src="fileUrl" 
                alt="Image" 
                loading="lazy" 
                class="max-w-[75vw] max-h-[75vh] border-4 border-solid border-white shadow-xl" />
            <div class="absolute items-center hidden w-8 h-8 px-2 py-2 rounded-full -right-4 -top-4 bg-white/50 group-hover:flex hover:bg-white">
                <a :href="fileUrl" class="text-sky-800" title="Download this image" download>
                    <font-awesome-icon 
                        icon="fa-solid fa-download" />
                </a>
            </div>
        </div>
        <div 
            class="flex justify-center items-center gap-4 w-[50vw] px-8 py-2 bg-white/30 dark:bg-slate-900/70 text-sky-900 dark:text-white rounded-lg">
            <aside class="flex items-center justify-center">
                <img 
                    :src="profilePic" 
                    alt="Profile Pic"
                    class="object-cover w-10 h-10 border border-solid rounded-full border-sky-800" 
                    loading="lazy">
            </aside>
            <div class="flex flex-col items-center flex-1">
                <div class="flex items-center justify-between w-full">
                    <div class="flex gap-2 text-sm text-sky-800">
                        <span class="font-bold">{{ fullname }}</span>
                        <span>@{{ username }}</span>
                    </div>
                    <div 
                        v-if="authStore.getIsAuthenticated && !isReply"
                        class="flex items-center justify-center gap-4 text-sky-400 dark:text-sky-900">
                        <span class="flex items-center gap-1">
                            <font-awesome-icon 
                                icon="fa-solid fa-retweet" 
                                class="transition-transform"
                                :class="{
                                    'text-sky-600 scale-105': isRexweeted,
                                    'cursor-pointer hover:text-sky-600 hover:scale-105': !isOwn,
                                    'cursor-not-allowed': isOwn
                                    }"
                                :title="!isOwn && !isRexweeted ? 'Rexweet' :
                                        isOwn ? 'You can\'t rexweet your own xweet' :
                                        'Unrexweet'"
                                @click="$emit('rexweet')" />
                            <span 
                                v-if="rexweetCount" 
                                class="text-xs"
                                :class="isRexweeted ? 'text-sky-600' : 'text-sky-400 dark:text-sky-900'">
                                {{ rexweetCount }}
                            </span>
                        </span>
                        <span class="flex items-center gap-1">
                        <font-awesome-icon 
                            v-if="!isLiked"
                            icon="fa-regular fa-heart"
                            class="transition-transform cursor-pointer hover:text-sky-600 hover:scale-105"
                            title="Like this xweet"
                            @click="$emit('like-xweet')" />
                        <font-awesome-icon
                            v-else
                            icon="fa-solid fa-heart"
                            class="scale-105 cursor-pointer text-sky-600"
                            title="Unlike this xweet"
                            @click="$emit('unlike-xweet')" />
                        <span 
                            v-if="likeCount" 
                            class="text-xs"
                            :class="isLiked ? 'text-sky-600' : 'text-sky-800'">
                            {{ likeCount }}
                        </span>
                        </span>
                    </div>
                </div>
                <span class="w-full">{{ body }}</span>
            </div>
        </div>
    </TransitionRoot>
</template>