<script setup lang="ts">
import UserToFollow from './UserToFollow.vue';
import Empty from '@/components/App/Empty.vue';
import { useFetchList } from '@/composables/useFetch';
import useAuthStore from '@/stores/useAuthStore';
import { User } from '@/types/auth';
import { WhoToFollow } from '@/types/follows';

const authStore = useAuthStore()

const mostActiveUsers = await useFetchList<WhoToFollow>('/api/users/most-active', true)
const followingList = await useFetchList<User>(`/api/users/${authStore.getSignedInUserId}/following`, true)

const userToFollow = mostActiveUsers.list?.value?.filter(user => {
    return (
        user.user_id !== authStore.getSignedInUserId &&
        !followingList.list?.value?.some(followed => followed.user_id === user.user_id)
    )
})
</script>

<template>
    <section 
        class="flex flex-col flex-1 gap-2 overflow-hidden border border-solid border-sky-800 rounded-xl">
        <div class="flex items-center justify-between px-4 py-2 bg-sky-600">
            <span class="font-semibold text-white">Who to Follow</span>
            <font-awesome-icon icon="fa-regular fa-user" class="text-white" />
        </div>
        <div class="flex flex-col justify-center gap-2 xl:px-4 overflow-scroll">
            <UserToFollow
                v-for="user in userToFollow" 
                :key="user.user_id"
                :id="user.user_id" 
                :fullname="user.full_name" 
                :username="user.username"
                :last-xweet="user.body"
                :profile-pic="user.profile_pic" />
            <Empty v-if="userToFollow?.length === 0" submsg="There is no user to follow for now" />
        </div>
    </section>
</template>