<script setup lang="ts">
import { computed, ref } from 'vue'
import { AxiosError } from 'axios'

import Toolbar from './Toolbar.vue'
import TextEditor from './TextEditor.vue'
import useRenderHashtags from '@/composables/useRenderHashtags'
import useAuthStore from '@/stores/useAuthStore'
import socket from '@/utils/socket'
import { sendReqCookie } from '@/utils/axiosInstances'
import { MAX_CHAR_COUNT } from '@/utils/constants'
import { XweetResponse } from '@/types/xweets'

const { inModal } = defineProps({
    inModal: {
        type: Boolean,
        default: false
    }
})
const emit = defineEmits<{
    (e: 'increment-xweet-count'): void
    (e: 'close-modal'): void
}>()

const authStore = useAuthStore()

const body = ref('')
const media = ref<File | null>(null)
const mediaPreview = ref('')
const charCount = computed(() => body.value.length)
const hashtags = useRenderHashtags(body)

const payload = computed(() => {
    const formData = new FormData()

    formData.append('body', body.value)
    formData.append('media', media.value as Blob)

    hashtags.value.forEach(tag => {
        formData.append(`hashtags`, tag)
    })

    return formData
})

const isLoading = ref(false)
const isSuccess = ref(false)
const errorMsg = ref('')

const addXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.post<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets`, 
            payload.value, 
            { headers: { "Content-Type": 'multipart/form-data' } }
        )

        if (data?.success) {
            socket.emit('add_to_timeline', authStore.getSignedInUserId)
            emit('increment-xweet-count')

            isLoading.value = false
            isSuccess.value = true
            body.value = ''
            media.value = null
            mediaPreview.value = ''

            setTimeout(() => {
                isSuccess.value = false
                if (inModal) {
                    emit('close-modal')
                }
            }, 1000)
        }
    } catch (error) {
        const err = error as AxiosError

        if (err.response?.status === 400) {
            isLoading.value = false

            const data = err.response.data as { success: boolean, message: string }
            errorMsg.value = data.message

            setTimeout(() => {
                errorMsg.value = ''
            }, 1000)
        }
    }
}

const setMedia = (file: File | null, fileUrl: string) => { 
    media.value = file
    mediaPreview.value = fileUrl 
}
</script>

<template>
    <section 
        class="bg-sky-600 relative flex flex-col justify-between items-center min-w-[50vw] px-12 border border-solid border-sky-800 rounded-xl dark:bg-transparent">
        <span class="w-full py-4 text-2xl text-white">New Xweet</span>
        <TextEditor
            :input-name="!inModal ? 'new-xweet' : 'modal-new-xweet'"
            v-model="body"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT" />
        <Toolbar
            :mode="!inModal ? 'new-xweet' : 'modal-new-xweet'"
            :submit-func="addXweet"
            :is-loading="isLoading"
            :is-success="isSuccess"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT"
            :media-preview="mediaPreview"
            :error-msg="errorMsg"
            @set-media="setMedia" />
    </section>
</template>