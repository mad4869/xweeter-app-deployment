<script lang="ts">
export enum Tabs {
    Xweets = 'xweets',
    Following = 'following',
    Followers = 'followers',
    Likes = 'likes'
}
</script>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useScroll } from '@vueuse/core';

import Header from './Header.vue';
import Toggle from './Toggle.vue';
import Timeline from './Timeline.vue';
import UserList from './UserList.vue';
import Likes from './Likes.vue';
import ProfileForm from './ProfileForm.vue';
import Popup from '@/components/App/Popup.vue';
import Modal from '@/components/App/Modal.vue';
import ConfirmDialog from '@/components/App/ConfirmDialog.vue';
import useCount, { Features } from '@/composables/useCount';
import useNotify from '@/composables/useNotify'
import { useFetchList, useFetchObject } from '@/composables/useFetch';
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore'
import { sendReqCookie } from'@/utils/axiosInstances'
import { User } from '@/types/auth';
import { XweetResponse } from '@/types/xweets';

const authStore = useAuthStore()

const timelineRef = ref<HTMLElement | null>(null)
const likeRef = ref<HTMLElement | null>(null)
const scrollTimeline = useScroll(timelineRef)
const scrollLike = useScroll(likeRef)

const route = useRoute()
const router = useRouter()

const activeTab = ref(route.query.tab || Tabs.Xweets)
const setActiveTab = (tab: Tabs) => {
    if (tab === Tabs.Xweets) {
        router.push('')
    } else {
        router.push({ query: { tab } })
    }

    router.afterEach(() => {
        activeTab.value = route.query.tab || Tabs.Xweets
    })
}

const profile = await useFetchObject<User>(`/api/users/${route.params.id}`, false)

if (profile.error.value) {
    router.replace({ name: '404' })
}

const profileXweetsCount = await useCount('users', parseInt(route.params.id as string), Features.Xweets)
const profileFollowing = await useFetchList<User>(`/api/users/${route.params.id}/following`, false)
const profileFollowers = await useFetchList<User>(`/api/users/${route.params.id}/followers`, false)
const profileFollowingCount = profileFollowing.list.value?.length
const profileFollowersCount = profileFollowers.list.value?.length

const userFollowing = await useFetchList<User>(`/api/users/${authStore.getSignedInUserId}/following`, true)
const userFollowed = userFollowing.list.value?.some(following => following.user_id === profile.obj.value?.user_id)

const notification = ref({ 
    isNotified: false, 
    category: undefined, 
    msg: '' 
    })

const showNotice = (category: 'success' | 'error', msg: string) => {
    useNotify(notification, category, msg)
}

const isLoading = ref(false)
const isError = ref(false)
const isSuccess = ref(false)

const formModal = ref(false)
const deleteModal = ref(false)
const xweetToDelete = ref<number | null>()

const deleteXweet = async (xweet_id?: number | null) => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.delete<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${xweet_id}`
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            deleteModal.value = false
            
            countStore.decrementXweetsCount()
            showNotice('error', 'Your xweet has been deleted')

            setTimeout(() => {
                isSuccess.value = false
                xweetToDelete.value = null
            }, 2000)
        }
    } catch (err) {
        isError.value = true

        setTimeout(() => {
            isError.value = false
        }, 2000)
    }
}

const showDeleteModal = (xweetId: number) => {
    deleteModal.value = true
    xweetToDelete.value = xweetId
}
</script>

<template>
    <Header
        :is-own="profile.obj.value?.user_id === authStore.getSignedInUserId"
        :user-id="profile.obj.value?.user_id"
        :fullname="profile.obj.value?.full_name"
        :username="profile.obj.value?.username"
        :bio="profile.obj.value?.bio"
        :profile-pic="profile.obj.value?.profile_pic"
        :header-pic="profile.obj.value?.header_pic"
        :xweets-count="profileXweetsCount"
        :following-count="profileFollowingCount"
        :followers-count="profileFollowersCount"
        :is-followed="userFollowed"
        @show-notice="showNotice"
        @show-edit-profile="formModal = true"
        @set-active-tab="setActiveTab" />
    <Toggle :active-tab="activeTab" @set-active-tab="setActiveTab" />
    <Timeline v-show="activeTab === Tabs.Xweets"
        :y="scrollTimeline.y.value"
        :is-own="profile.obj.value?.user_id === authStore.getSignedInUserId"
        :is-filtered="isSuccess"
        :deleted-xweet="xweetToDelete"
        :show-delete-modal="showDeleteModal"
        :show-notice="showNotice" />
    <UserList v-show="activeTab === Tabs.Following"
        :data="profileFollowing.list.value ?? []" />
    <UserList v-show="activeTab === Tabs.Followers"
        :data="profileFollowers.list.value ?? []" />
    <Likes v-show="activeTab === Tabs.Likes"
        :y="scrollLike.y.value"
        :show-notice="showNotice" />
    <Modal :show="formModal" @clicked-outside="formModal = false">
        <ProfileForm
            :user-id="profile.obj.value?.user_id"
            :username="profile.obj.value?.username"
            :fullname="profile.obj.value?.full_name"
            :email="profile.obj.value?.email"
            :bio="profile.obj.value?.bio"
            :profile-pic="profile.obj.value?.profile_pic"
            :header-pic="profile.obj.value?.header_pic"
            @close-modal="formModal = false"
            @show-notice="showNotice" />
    </Modal>
    <Modal :show="deleteModal" @clicked-outside="deleteModal = false">
        <ConfirmDialog
            title="Delete Xweet"
            confirm-msg="Are you sure you want to delete this xweet?"
            :confirm-fn="deleteXweet"
            :payload="xweetToDelete"
            error-msg="Failed to delete xweet. Please try again"
            :is-loading="isLoading"
            :is-error="isError"
            @close-modal="deleteModal = false" />
    </Modal>
    <Popup
        :show="notification.isNotified"
        :category="notification.category" 
        :message="notification.msg" />
</template>