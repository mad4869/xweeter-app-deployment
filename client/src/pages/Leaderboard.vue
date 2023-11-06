<script setup lang="ts">
import { ref } from 'vue';

import Layout from '@/components/App/Layout/index.vue'
import SidebarLeft from '@/components/App/Layout/SidebarLeft.vue';
import SidebarRight from '@/components/App/Layout/SidebarRight.vue';
import Skeleton from '@/components/App/Skeleton/index.vue'
import Modal from '@/components/App/Modal.vue';
import NewXweet from '@/components/App/Xweet/NewXweet.vue';
import Content from '@/components/Leaderboard/Content.vue';
import useAuthStore from '@/stores/useAuthStore';
import { countStore } from '@/stores/useCountStore';

const authStore = useAuthStore()
await authStore.getUser()

const showModal = ref(false)
</script>

<template>
    <Suspense>
        <Layout>
            <template #sidebarLeft>
                <SidebarLeft @show-new-xweet="showModal = true" />
            </template>
            <Content />
            <Modal :show="showModal" @clicked-outside="showModal = false">
                <NewXweet in-modal 
                    @increment-xweet-count="countStore.incrementXweetsCount()"
                    @close-modal="showModal = false" />
            </Modal>
            <template #sidebarRight>
                <SidebarRight />
            </template>
        </Layout>
        <template #fallback>
            <Skeleton />
        </template>
    </Suspense>
</template>