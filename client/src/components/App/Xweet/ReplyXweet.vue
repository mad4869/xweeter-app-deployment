<script setup lang="ts">
import { ref, computed } from 'vue';
import { TransitionRoot } from '@headlessui/vue';
import { AxiosError } from 'axios';

import TextEditor from './TextEditor.vue';
import Toolbar from './Toolbar.vue';
import useAuthStore from '@/stores/useAuthStore';
import { sendReqCookie } from '@/utils/axiosInstances'
import { MAX_CHAR_COUNT } from '@/utils/constants'
import { RepliesResponse } from '@/types/replies';
import socket from '@/utils/socket';

const { xweetId } = defineProps<{
    show: boolean
    xweetId: number
}>()
const emit = defineEmits<{
    (e: 'close-reply'): void
}>()

const authStore = useAuthStore()

const body = ref('')
const media = ref<File | null>(null)
const mediaPreview = ref('')
const charCount = computed(() => body.value.length)

const payload = computed(() => {
    const formData = new FormData()

    formData.append('xweet_id', String(xweetId))
    formData.append('body', body.value)
    formData.append('media', media.value as Blob)

    return formData
})

const isLoading = ref(false)
const isSuccess = ref(false)
const errorMsg = ref('')

const replyXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.post<RepliesResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/replies`, payload.value
        )

        if (data?.success) {
            socket.emit('add_to_replies', xweetId)

            isLoading.value = false
            isSuccess.value = true
            body.value = ''
            media.value = null
            mediaPreview.value = ''

            setTimeout(() => {
                isSuccess.value = false
                
                emit('close-reply')
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
    <TransitionRoot
        as="section"
        :show="show"
        class="px-8 pt-4 flex flex-col justify-center items-center bg-sky-600/10 backdrop-blur-lg border border-solid border-sky-800 rounded-xl before:absolute before:top-0 before:left-16 before:-translate-y-2 before:w-0 before:h-0 before:border-l-8 before:border-r-8 before:border-b-8 before:border-solid before:border-l-transparent before:border-r-transparent before:border-b-sky-800"
        enter="transition-all duration-500 ease-out"
        enter-from="-translate-y-1 opacity-0"
        enter-to="translate-y-0 opacity-100"
        leave="transition-all duration-150 ease-in"
        leave-from="translate-y-0 opacity-100"
        leave-to="-translate-y-1 opacity-0">
        <TextEditor
            input-name="reply-xweet"
            v-model="body"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT" />
        <Toolbar
            mode="reply-xweet"
            :submit-func="replyXweet"
            :is-loading="isLoading"
            :is-success="isSuccess"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT"
            :media-preview="mediaPreview"
            :error-msg="errorMsg"
            @set-media="setMedia" />
    </TransitionRoot>
</template>