<script setup lang="ts">
import { ref } from 'vue';
import { useScroll } from '@vueuse/core';

import Timeline from './Timeline.vue'
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import Sep from '@/components/App/Sep.vue';
import Popup from '@/components/App/Popup.vue'
import Modal from '@/components/App/Modal.vue';
import ConfirmDialog from '@/components/App/ConfirmDialog.vue';
import useNotify from '@/composables/useNotify'
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore'
import { sendReqCookie } from'@/utils/axiosInstances'
import { XweetResponse } from '@/types/xweets'

const authStore = useAuthStore()

const el = ref<HTMLElement | null>(null)
const { y } = useScroll(el)

const notification = ref({ 
    isNotified: false, 
    category: undefined, 
    msg: '' 
    })

const showNotice = (category: 'success' | 'error', msg: string) => {
    useNotify(notification, category, msg)
}

const showModal = ref(false)
const xweetToDelete = ref<number | null>()

const isLoading = ref(false)
const isError = ref(false)
const isSuccess = ref(false)

const deleteXweet = async (xweet_id?: number | null) => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.delete<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${xweet_id}`
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            showModal.value = false
            
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
    showModal.value = true
    xweetToDelete.value = xweetId
}
</script>

<template>
    <NewXweet 
        v-if="authStore.getIsAuthenticated" 
        @increment-xweet-count="() => { countStore.incrementXweetsCount() }" />
    <Sep title="Timeline" is-sticky class="cursor-pointer" @click="y = 0" />
    <Timeline 
        :y="y"
        :is-filtered="isSuccess"
        :deleted-xweet="xweetToDelete"
        :show-delete-modal="showDeleteModal"
        :show-notice="showNotice" />
    <Modal :show="showModal" @clicked-outside="showModal = false">
        <ConfirmDialog
            title="Delete Xweet"
            confirm-msg="Are you sure you want to delete this xweet?"
            :confirm-fn="deleteXweet"
            :payload="xweetToDelete"
            error-msg="Failed to delete xweet. Please try again"
            :is-loading="isLoading"
            :is-error="isError"
            @close-modal="showModal = false" />
    </Modal>
    <Popup 
        :show="notification.isNotified" 
        :message="(notification.msg as string)" 
        :category="notification.category" />
</template>