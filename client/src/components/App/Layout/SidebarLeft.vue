<script setup lang="ts">
import { ref } from 'vue';

import Toggle from '@/components/App/Auth/Toggle.vue'
import SigninForm from '../Auth/SigninForm.vue';
import SignupForm from '../Auth/SignupForm.vue';
import Profile from '@/components/App/Profile/index.vue'
import Settings from '@/components/App/Settings/index.vue'
import useAuthStore from '@/stores/useAuthStore';
import { UserAuth } from '@/types/auth';

defineEmits<{
    (e: 'show-new-xweet'): void
}>()

const authStore = useAuthStore()

const activeBtn = ref<UserAuth>(UserAuth.SignUp)
const activateBtn = (btn: UserAuth) => {
    activeBtn.value = btn
}
</script>

<template>
    <section 
        v-if="!authStore.getIsAuthenticated"
        class="flex-[4] flex flex-col items-center px-2 pt-4 bg-sky-800 border border-solid dark:border-sky-800 rounded-xl dark:bg-transparent">
        <Toggle :active-btn="activeBtn" @activate-btn="activateBtn" />
        <Transition mode="out-in">
            <KeepAlive>
                <component :is="activeBtn === UserAuth.SignUp ? SignupForm : SigninForm" />
            </KeepAlive>
        </Transition>
    </section>
    <Profile 
        v-else
        @show-new-xweet="$emit('show-new-xweet')" />
    <Settings />
</template>

<style scoped>
.v-enter-active,
.v-leave-active {
    @apply transition-all duration-300 ease-out
}

.v-enter-from,
.v-leave-to {
    @apply translate-x-4 opacity-0
}
</style>