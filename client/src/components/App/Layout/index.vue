<script setup lang="ts">
import { ref } from 'vue';

import Navbar from './Navbar.vue';
import Footer from './Footer.vue';
import Modal from '@/components/App/Modal.vue';
import ConfirmDialog from '@/components/App/ConfirmDialog.vue';
import router from '@/routes';
import useAuthStore from '@/stores/useAuthStore';

defineProps({
    showSidebar: {
        type: Boolean,
        default: true
    }
})

const authStore = useAuthStore()

const isError = ref(false)
const isLoading = ref(false)
const showModal = ref(false)

const signout = async () => {
    isLoading.value = true

    await authStore.signout()

    isLoading.value = false

    if (!authStore.getIsAuthenticated) {
        router.push('/')
    } else {
        isError.value = true
        setTimeout(() => {
            isError.value = false
        }, 3000)
    }
}
</script>

<template>
    <Navbar @show-signout-modal="showModal = true" />
    <main class="grid w-full grid-cols-4 px-4 py-4 md:grid-cols-6 lg:grid-cols-5 gap-x-4">
        <aside
            v-if="showSidebar" 
            class="sticky flex-col justify-center hidden col-span-1 gap-4 lg:flex top-20 h-side">
            <slot name="sidebarLeft"></slot>
        </aside>
        <article 
            class="flex flex-col gap-4" 
            :class="showSidebar ? 'col-span-4 lg:col-span-3' : 'col-span-5'">
            <slot></slot>
        </article>
        <aside
            v-if="showSidebar" 
            class="sticky flex-col justify-center hidden col-span-1 gap-4 md:flex md:col-span-2 lg:col-span-1 top-20 h-side">
            <slot name="sidebarRight"></slot>
        </aside>
    </main>
    <Modal :show="showModal" @clicked-outside="() => { showModal = false }">
        <ConfirmDialog
            title="Sign Out"
            confirm-msg="Are you sure you want to sign out?"
            :confirm-fn="signout"
            error-msg="Failed to sign out. Please try again"
            :is-loading="isLoading"
            :is-error="isError"
            @close-modal="showModal = false" />
    </Modal>
    <Footer />
</template>

<style scoped>
.h-side {
    height: calc(100vh - 6rem);
}
</style>
