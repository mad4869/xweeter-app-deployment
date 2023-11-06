<script setup lang="ts">
import Layout from '@/components/App/Layout/index.vue'
import Header from './Header.vue'
import Content from './Content.vue';
import Settings from './Settings.vue'
import Profile from './Profile.vue'
import Suggestions from './Suggestions.vue';
import Trending from './Trending.vue';
</script>

<template>
    <Layout>
        <template #sidebarLeft>
            <Profile />
            <Settings />
        </template>
        <Header />
        <Content />
        <template #sidebarRight>
            <Suggestions />
            <Trending />
        </template>
    </Layout>
</template>