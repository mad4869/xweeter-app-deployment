<script setup lang="ts">
import { UserAuth } from '@/types/auth'

defineProps<{
    activeBtn: UserAuth
}>()
defineEmits<{
    (e: 'activate-btn', btn: UserAuth): void
}>()
</script>

<template>
    <div 
        class="flex items-center w-40 overflow-hidden text-xs border border-solid rounded-lg border-sky-600">
        <button 
            :class="{ active: activeBtn === UserAuth.SignUp }" 
            @click="$emit('activate-btn', UserAuth.SignUp)">
            Sign Up
        </button>
        <button 
            :class="{ active: activeBtn === UserAuth.SignIn }" 
            @click="$emit('activate-btn', UserAuth.SignIn)">
            Sign In
        </button>
    </div>
</template>

<style scoped>
button {
    @apply w-1/2 px-2 py-1 text-sky-600 dark:text-white
}

.active {
    @apply bg-sky-600 font-medium text-white
}
</style>