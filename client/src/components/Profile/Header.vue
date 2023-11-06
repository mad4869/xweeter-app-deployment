<script setup lang="ts">
import { ref } from 'vue';

import { Tabs } from './Content.vue'
import useAuthStore from '@/stores/useAuthStore';
import { sendReqCookie } from '@/utils/axiosInstances';
import { UserResponse } from '@/types/users'
import { ToFollowResponse } from '@/types/follows'
import useFile from '@/composables/useFile'

const { userId, profilePic, headerPic, isFollowed } = defineProps<{
    isOwn: boolean,
    userId?: number,
    fullname?: string,
    username?: string,
    bio?: string | null,
    profilePic?: string,
    headerPic?: string,
    xweetsCount?: number,
    followingCount?: number,
    followersCount?: number,
    isFollowed?: boolean
}>()

const emit = defineEmits<{
    (e: 'show-notice', category: 'success' | 'error', msg: string): void,
    (e: 'show-edit-profile'): void
    (e: 'set-active-tab', tab: Tabs): void
}>()

const authStore = useAuthStore()

const pfp = ref<File | null>(null)
const pfpPreview = ref(profilePic)
const header = ref<File | null>(null)
const headerPreview = ref(headerPic)
const userFollowed = ref(isFollowed)
const isLoading = ref(false)
const isEditable = ref(false)

const managePfp = async (e: Event) => {
    isEditable.value = true
    const fileData = await useFile(e)
    if (fileData.file) {
        pfp.value = fileData.file
        pfpPreview.value = fileData.fileDataURL
    }
}

const manageHeader = async (e: Event) => {
    isEditable.value = true
    const fileData = await useFile(e)
    if (fileData.file) {
        header.value = fileData.file
        headerPreview.value = fileData.fileDataURL
    }
}

const changeImage = async () => {
    isLoading.value = true

    const formData = new FormData()

    try {
        if (pfp.value) {
            formData.append('profile_pic', pfp.value)
        }
        if (header.value) {
            formData.append('header_pic', header.value)
        }

        const { data } = await sendReqCookie.put<UserResponse | undefined>(
            `/api/users/${userId}`, formData
        )

        if (data?.success) {
            isLoading.value = false
            isEditable.value = false

            emit('show-notice', 'success', 'Your profile images have been updated')
        }
    } catch (err) {
        isLoading.value = false
        isEditable.value = false
        pfpPreview.value = profilePic
        headerPreview.value = headerPic

        emit('show-notice', 'error', 'Error occured during process. Please try again')
    }
}

const follow = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.post<ToFollowResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/follows/${userId}`
        )

        if (data?.success) {
            isLoading.value = false
            userFollowed.value = true
        }
    } catch (err) {
        isLoading.value = false

        emit('show-notice', 'error', 'Error occured during process. Please try again')
    }
}
</script>

<template>
    <section class="relative grid grid-rows-5 h-[55vh] rounded-lg overflow-hidden">
        <div class="relative row-span-3 group/header">
            <img 
                :src="headerPreview" 
                class="object-cover w-full h-full"
                alt="Header" 
                loading="lazy">
            <label
                v-if="authStore.getIsAuthenticated && isOwn" 
                for="change-header"
                class="absolute items-center hidden px-2 py-1 text-xs font-semibold text-white rounded-md cursor-pointer right-4 top-4 bg-sky-600/50 backdrop-blur-md group-hover/header:flex hover:bg-sky-600"
                title="Change your header">
                Change
                <input 
                    type="file" 
                    id="change-header" 
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="manageHeader">
            </label>
        </div>
        <div class="absolute flex justify-between items-center w-full bottom-[16vh] px-12">
            <label
                for="change-profile-pic" 
                title="Change your profile picture" 
                class="relative w-20 h-20 overflow-hidden border border-solid rounded-full shadow-xl border-sky-600 group/pfp">
                <img 
                    :src="pfpPreview" 
                    class="object-cover w-full h-full"
                    alt="Profile Pic" 
                    loading="lazy">
                <div 
                    v-if="authStore.getIsAuthenticated && isOwn" 
                    class="absolute top-0 left-0 items-center justify-center hidden w-full h-full text-xs font-semibold text-white cursor-pointer bg-slate-600/10 backdrop-blur-sm group-hover/pfp:flex">
                    Change
                </div>
                <input 
                    v-if="authStore.getIsAuthenticated && isOwn" 
                    type="file" 
                    id="change-profile-pic"  
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="managePfp">
            </label>
            <div class="flex items-center gap-2">
                <button
                    v-if="authStore.getIsAuthenticated && isOwn"
                    class="px-4 py-1 font-medium bg-white border-2 border-solid rounded-md dark:text-white text-sky-600 dark:bg-sky-600 dark:border-sky-800 dark:hover:bg-sky-800 dark:hover:border-sky-600 hover:bg-slate-200"
                    title="Edit your profile"
                    @click="$emit('show-edit-profile')">
                    Edit
                </button>
                <button
                    v-else-if="authStore.getIsAuthenticated && !isOwn && !userFollowed"
                    class="px-4 py-1 font-medium bg-white border-2 border-solid rounded-md dark:text-white text-sky-600 dark:bg-sky-600 dark:border-sky-800 dark:hover:bg-sky-800 dark:hover:border-sky-600 hover:bg-slate-200"
                    title="Follow this user"
                    @click="follow">
                    <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
                    {{ !isLoading ? 'Follow' : '' }}
                </button>
                <div
                    v-else-if="authStore.getIsAuthenticated && !isOwn && userFollowed"
                    class="px-4 py-1 font-medium rounded-md cursor-not-allowed bg-slate-600 text-slate-400"
                    title="You already followed this user">
                    Followed
                </div>
                <button
                    v-if="isEditable"
                    class="px-2 py-1 font-medium bg-white border-2 border-solid rounded-full dark:text-white text-sky-600 dark:bg-sky-600 dark:border-sky-800 dark:hover:bg-sky-800 dark:hover:border-sky-600 hover:bg-slate-200"
                    title="Confirm change"
                    @click="changeImage">
                    <font-awesome-icon icon="fa-solid fa-check" class="text-sm" />
                </button>
            </div>
        </div>
        <div class="flex items-center justify-between row-span-2 row-start-4 px-12 pt-8 leading-4 bg-sky-600 dark:bg-white/10">
            <div class="flex flex-col gap-4 max-w-[50%] text-white">
                <div>
                    <p class="text-2xl font-bold dark:text-sky-600">{{ fullname }}</p>
                    <p class="text-sm dark:text-sky-600">@{{ username }}</p>
                </div>
                <p v-if="bio" class="text-xs">{{ bio }}</p>
            </div>
            <div class="flex flex-col items-end justify-center gap-4 text-white cursor-pointer">
                <div @click="$emit('set-active-tab', Tabs.Xweets)" title="View xweets">
                    <p class="text-xl"><strong>{{ xweetsCount }}</strong> <span class="text-white/50">Xweets</span></p>
                </div>
                <div class="flex items-center justify-center gap-4" title="View following">
                    <div @click="$emit('set-active-tab', Tabs.Following)">
                        <strong>{{ followingCount }}</strong> <span class="text-white/50">Following</span>
                    </div>
                    <div @click="$emit('set-active-tab', Tabs.Followers)" title="View followers">
                        <strong>{{ followersCount }}</strong> <span class="text-white/50">Followers</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>