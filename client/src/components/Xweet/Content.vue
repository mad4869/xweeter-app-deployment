<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import XweetDetails from './XweetDetails.vue';
import Sep from '@/components/App/Sep.vue';
import Modal from '@/components/App/Modal.vue';
import ConfirmDialog from '@/components/App/ConfirmDialog.vue';
import Popup from '@/components/App/Popup.vue'
import { useFetchObject } from '@/composables/useFetch';
import useNotify from '@/composables/useNotify'
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore'
import { sendReqCookie } from'@/utils/axiosInstances'
import { XweetDetail, XweetResponse } from '@/types/xweets';

const authStore = useAuthStore()

const route = useRoute()
const router = useRouter()

const notification = ref({ 
    isNotified: false, 
    category: undefined, 
    msg: '' 
    })

const showNotice = (category: 'success' | 'error', msg: string) => {
    useNotify(notification, category, msg)
}

const xweet = await useFetchObject<XweetDetail>(`/api/xweets/${route.params.id}`, false)

if (xweet.error.value) {
    router.replace({ name: '404' })
}

const isLoading = ref(false)
const isError = ref(false)
const isSuccess = ref(false)

const deleteXweetModal = ref(false)
const deleteReplyModal = ref(false)
const xweetToDelete = ref<number | null>()
const replyToDelete = ref<number | null>()

const deleteXweet = async (xweet_id?: number | null) => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.delete<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${xweet_id}`
        )

        if (data?.success) {
            isLoading.value = false
            deleteXweetModal.value = false
            
            countStore.decrementXweetsCount()
            showNotice('error', 'Your xweet has been deleted')

            router.push('/')
        }
    } catch (err) {
        isError.value = true

        setTimeout(() => {
            isError.value = false
        }, 2000)
    }
}

const deleteReply = async (reply_id?: number | null) => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.delete<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/replies/${reply_id}`
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            deleteReplyModal.value = false
            
            showNotice('error', 'Your reply has been deleted')

            setTimeout(() => {
                isSuccess.value = false
                replyToDelete.value = null
            }, 2000)
        }
    } catch (err) {
        isError.value = true

        setTimeout(() => {
            isError.value = false
        }, 2000)
    }
}

const showDeleteXweetModal = (xweetId: number) => {
    deleteXweetModal.value = true
    xweetToDelete.value = xweetId
}
const showDeleteReplyModal = (xweetId: number) => {
    deleteReplyModal.value = true
    replyToDelete.value = xweetId
}
</script>

<template>
    <Sep title="Xweet from:" :subtitle="`@${xweet.obj.value?.username}`" :is-sticky="false" />
    <XweetDetails 
        :data="xweet.obj.value"
        :replies-filtered="isSuccess"
        :deleted-xweet="xweetToDelete"
        :deleted-reply="replyToDelete"
        :show-delete-xweet-modal="showDeleteXweetModal"
        :show-delete-reply-modal="showDeleteReplyModal"
        :show-notice="showNotice" />
    <Modal :show="deleteXweetModal" @clicked-outside="deleteXweetModal = false">
        <ConfirmDialog
            title="Delete Xweet"
            confirm-msg="Are you sure you want to delete this xweet?"
            :confirm-fn="deleteXweet"
            :payload="xweetToDelete"
            error-msg="Failed to delete xweet. Please try again"
            :is-loading="isLoading"
            :is-error="isError"
            @close-modal="deleteXweetModal = false" />
    </Modal>
    <Modal :show="deleteReplyModal" @clicked-outside="deleteReplyModal = false">
        <ConfirmDialog
            title="Delete Reply"
            confirm-msg="Are you sure you want to delete this reply?"
            :confirm-fn="deleteReply"
            :payload="replyToDelete"
            error-msg="Failed to delete reply. Please try again"
            :is-loading="isLoading"
            :is-error="isError"
            @close-modal="deleteReplyModal = false" />
    </Modal>
    <Popup 
        :show="notification.isNotified" 
        :message="(notification.msg as string)" 
        :category="notification.category" />
</template>