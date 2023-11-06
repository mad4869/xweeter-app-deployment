<script setup lang="ts">
import { computed, ref } from 'vue';
import { AxiosError } from 'axios';

import TextEditor from './TextEditor.vue';
import Toolbar from './Toolbar.vue';
import useRenderHashtags from '@/composables/useRenderHashtags';
import useAuthStore from '@/stores/useAuthStore';
import { MAX_CHAR_COUNT } from '@/utils/constants';
import { sendReqCookie } from '@/utils/axiosInstances';
import { XweetResponse } from '@/types/xweets'
import { ReplyResponse } from '@/types/replies';

const { xweet_id, body, fileUrl } = defineProps<{
    xweet_id: number,
    body: string
    fileUrl?: string
    isReply?: boolean
}>()

const emit = defineEmits<{
    (e: 'update-xweet', newBody: string, newMedia?: string, updateDate?: string): void
}>()

const authStore = useAuthStore()

const newBody = ref(body)
const newMedia = ref<File | null>(null)
const newMediaPreview = ref(fileUrl)
const charCount = computed(() => newBody.value.length)
const hashtags = useRenderHashtags(newBody)

const payload = computed(() => {
    const formData = new FormData()

    formData.append('new_body', newBody.value)
    formData.append('new_media', newMedia.value as Blob)
    formData.append('new_media_url', newMediaPreview.value ?? '')

    hashtags.value.forEach(tag => {
        formData.append(`hashtags`, tag)
    })

    return formData
})

const isLoading = ref(false)
const isSuccess = ref(false)
const errorMsg = ref('')

const editXweet = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.put<XweetResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/xweets/${xweet_id}`, payload.value
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            newBody.value = ''
            newMedia.value = null
            newMediaPreview.value = ''
            
            setTimeout(() => {
                isSuccess.value = false

                emit('update-xweet', data.data.body, data.data.media, data.data.updated_at)
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

const editReply = async () => {
    isLoading.value = true

    try {
        const { data } = await sendReqCookie.put<ReplyResponse | undefined>(
            `/api/users/${authStore.getSignedInUserId}/replies/${xweet_id}`, payload.value
        )

        if (data?.success) {
            isLoading.value = false
            isSuccess.value = true
            newBody.value = ''
            newMedia.value = null
            newMediaPreview.value = ''
            
            setTimeout(() => {
                isSuccess.value = false

                emit('update-xweet', data.data.body, data.data.media, data.data.updated_at)
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
    newMedia.value = file
    newMediaPreview.value = fileUrl 
}
</script>

<template>
    <section class="flex flex-col justify-between items-center h-full">
        <TextEditor
            input-name="edit-xweet"
            v-model="newBody"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT" />
        <Toolbar
            mode="edit-xweet"
            :submit-func="!isReply ? editXweet : editReply"
            :is-loading="isLoading"
            :is-success="isSuccess"
            :char-count="charCount"
            :max-char-count="MAX_CHAR_COUNT"
            :media-preview="newMediaPreview"
            :error-msg="errorMsg"
            @set-media="setMedia" />
    </section>
</template>