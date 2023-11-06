<script setup lang="ts">
import { ref } from 'vue';

import Layout from '@/components/App/Layout/index.vue'
import SidebarLeft from '@/components/App/Layout/SidebarLeft.vue';
import SidebarRight from '@/components/App/Layout/SidebarRight.vue';
import Modal from '@/components/App/Modal.vue';
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore';

const authStore = useAuthStore()
await authStore.getUser()

const showModal = ref(false)
</script>

<template>
    <Layout>
        <template #sidebarLeft>
            <SidebarLeft @show-new-xweet="showModal = true" />
        </template>
        <section class="flex flex-col items-center justify-center min-h-screen gap-8 text-sky-600">
            <div class="flex flex-col items-center justify-center">
                <p class="text-6xl font-bold">404</p>
                <p>There is nothing here</p>
            </div>
            <router-link to="/" title="Back to home" class="dark:text-white hover:underline">Go back</router-link>
        </section>
        <Modal :show="showModal" @clicked-outside="showModal = false">
            <NewXweet in-modal 
                @increment-xweet-count="countStore.incrementXweetsCount()"
                @close-modal="showModal = false" />
        </Modal>
        <template #sidebarRight>
            <SidebarRight />
        </template>
    </Layout>
</template>