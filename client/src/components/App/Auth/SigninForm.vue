<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useVuelidate } from '@vuelidate/core'
import { required, minLength } from '@vuelidate/validators'

import InputField from '@/components/App/InputField.vue';
import useAuthStore from '@/stores/useAuthStore';

const authStore = useAuthStore()

const credentials = reactive({
    username: '',
    password: ''
})
const rules = {
    username: { required },
    password: { required, minLength: minLength(6) }
}

const v$ = useVuelidate(rules, credentials)

const isError = ref(false)
const isLoading = ref(false)

const signin = async () => {
    isLoading.value = true
    
    await authStore.signin(credentials)
    
    isLoading.value = false

    if (!authStore.getIsAuthenticated) {
        isError.value = true
        setTimeout(() => {
            isError.value = false
        }, 3000)
    }
}
</script>

<template>
    <form 
        class="relative flex flex-col items-center justify-center flex-1 w-full gap-6" 
        @submit.prevent="signin">
        <InputField 
            input-id="username" 
            input-name="username" 
            input-type="text" 
            :input-errors="v$.username.$errors"
            v-model="v$.username.$model" 
            label-text="Username" 
            icon="fa-solid fa-user" />
        <InputField 
            input-id="password" 
            input-name="password" 
            input-type="password" 
            :input-errors="v$.password.$errors"
            v-model="v$.password.$model" 
            label-text="Password" 
            icon="fa-solid fa-lock" />
        <div v-if="isError" class="text-xs text-red-400">{{ authStore.getErrorMsg }}</div>
        <button 
            type="submit"
            class="w-24 py-1 text-white uppercase transition-colors duration-200 ease-in rounded-md shadow-sm bg-sky-600 shadow-slate-900/50 hover:bg-sky-800 active:shadow-inner disabled:bg-neutral-800 disabled:text-neutral-600 disabled:shadow-none disabled:cursor-not-allowed"
            title="Sign In"
            :disabled="v$.$invalid">
            <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse v-if="isLoading" />
            {{ !isLoading ? 'Sign In' : '' }}
        </button>
    </form>
</template>