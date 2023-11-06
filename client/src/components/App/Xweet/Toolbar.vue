<script setup lang="ts">
import useFile from '@/composables/useFile';

defineProps<{
    mode: 'new-xweet' | 'modal-new-xweet' | 'edit-xweet' | 'reply-xweet'
    submitFunc: () => Promise<void>
    isLoading: boolean
    isSuccess: boolean
    charCount: number
    maxCharCount: number
    mediaPreview?: string
    errorMsg?: string
}>()
const emit = defineEmits<{
    (e: 'set-media', file: File | null, fileUrl: string): void
}>()

const modeMap = {
    'new-xweet': {
        btn: 'Xweet',
        tooltip: 'Add new xweet',
        successMsg: 'You posted a new xweet!'
    },
    'modal-new-xweet': {
        btn: 'Xweet',
        tooltip: 'Add new xweet',
        successMsg: 'You posted a new xweet!'
    },
    'edit-xweet': {
        btn: 'Fix Xweet',
        tooltip: 'Fix your xweet',
        successMsg: 'You fixed your xweet!'
    },
    'reply-xweet': {
        btn: 'Reply',
        tooltip: 'Send reply to the xweet above',
        successMsg: 'You replied to the xweet!'
    }
}

const addFile = async (e: Event) => {
    const fileData = await useFile(e)
    if (fileData.file) {
        emit('set-media', fileData.file, fileData.fileDataURL ?? '')
    }
}

const removeFile = () => {
    emit('set-media', null, '')
}
</script>

<template>
    <div class="flex items-start justify-between w-full py-4">
        <div class="flex items-center h-full gap-2">
            <label :for="`${mode}-add-image`" title="Add image to your xweet">
                <span
                    class="flex items-center gap-2 px-2 py-1 text-xs text-white transition-colors rounded-md cursor-pointer bg-sky-800/70 hover:bg-sky-800 dark:bg-sky-400/50 dark:hover:bg-sky-400">
                    <font-awesome-icon icon="fa-solid fa-images" />
                    <h6>Image</h6>
                </span>
                <input 
                    type="file" 
                    :id="`${mode}-add-image`" 
                    accept="image/jpeg, image/png" 
                    class="hidden"
                    @change="addFile">
            </label>
            <div v-show="mediaPreview" class="relative group">
                <img :src="mediaPreview" class="object-scale-down w-8 h-8" />
                <font-awesome-icon 
                    icon="fa-regular fa-circle-xmark" 
                    title="Remove the image"
                    class="absolute hidden text-xs cursor-pointer -top-1 -right-1 text-sky-800 dark:text-white group-hover:block"
                    @click="removeFile" />
            </div>
        </div>
        <div class="flex items-center h-full px-2 text-center text-white">
            <Transition mode="out-in">
                <p v-if="charCount > maxCharCount" class="text-red-600 fade-in dark:text-red-400">
                    Your xweet exceeds the maximum number of characters
                </p>
                <p v-else-if="isSuccess" class="font-bold text-sky-800 fade-in dark:text-sky-600">
                    {{ modeMap[mode].successMsg }}
                </p>
                <p v-else-if="errorMsg" class="text-red-600 fade-in dark:text-red-400">
                    {{ errorMsg }}
                </p>
                <p v-else class="text-xs">
                    <span>{{ charCount }}</span>
                    /
                    <span class="font-medium dark:text-sky-600 dark:font-normal">{{ maxCharCount }}</span>
                </p>
            </Transition>
        </div>
        <div class="flex items-center h-full gap-2">
            <font-awesome-icon 
                v-show="isLoading"
                icon="fa-solid fa-spinner" spin-pulse 
                class="text-white" />
            <input 
                type="button" 
                :value="modeMap[mode].btn"
                class="px-4 py-1 font-semibold transition-colors duration-200 bg-white rounded-md cursor-pointer dark:bg-sky-600 text-sky-600 dark:text-white dark:hover:bg-sky-800 active:shadow-inner disabled:bg-sky-700 dark:disabled:bg-slate-800 dark:disabled:text-slate-600 disabled:cursor-not-allowed"
                :disabled="charCount > maxCharCount || (charCount === 0 && !mediaPreview) || isLoading" 
                :title="modeMap[mode].tooltip" 
                @mousedown="submitFunc">
        </div>
    </div>
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
</style>