<script setup lang="ts">
import { ref } from 'vue';

import Toggle from '@/components/App/Auth/Toggle.vue';
import SignupForm from '@/components/App/Auth/SignupForm.vue';
import SigninForm from '@/components/App/Auth/SigninForm.vue';
import { UserAuth } from '@/types/auth'

const activeBtn = ref<UserAuth>(UserAuth.SignUp)
const activateBtn = (btn: UserAuth) => {
    activeBtn.value = btn
}
</script>

<template>
    <section
        class="flex flex-col items-center justify-center col-start-1 col-span-2 sm:col-start-2 sm:col-span-1 row-span-5 row-start-1 gap-2 px-32 py-8 rounded-lg shadow-lg bg-white/10 backdrop-blur-lg shadow-sky-800">
        <Toggle :active-btn="activeBtn" @activate-btn="activateBtn" />
        <h3 class="text-xl lg:text-2xl font-semibold text-white min-w-max">
            {{ activeBtn === UserAuth.SignUp ? 'Let\'s get you started!' : 'Welcome Back!' }}
        </h3>
        <Transition mode="out-in">
            <KeepAlive>
                <component :is="activeBtn === UserAuth.SignUp ? SignupForm : SigninForm" />
            </KeepAlive>
        </Transition>
    </section>
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