<script setup lang="ts">
import Layout from '@/components/App/Layout/index.vue'
</script>

<template>
    <Layout :show-sidebar="false">
        <iframe src="http://127.0.0.1:5000/admin" frameborder="0" width="100%" height="600"></iframe>
    </Layout>
</template>