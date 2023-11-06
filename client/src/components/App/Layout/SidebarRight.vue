<script setup lang="ts">
import Suggestions from '@/components/App/Suggestions/index.vue'
import Trending from '@/components/App/Trending/index.vue'
import useAuthStore from '@/stores/useAuthStore';

const authStore = useAuthStore()
</script>

<template>
    <Suggestions v-if="authStore.getIsAuthenticated" />
    <Trending />
</template>