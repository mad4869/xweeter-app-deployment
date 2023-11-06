<script setup lang="ts">
defineProps<{ size: 'sm' | 'md' | 'lg' }>()

const sizes = {
    sm: 'w-8',
    md: 'w-16',
    lg: 'w-32'
}
</script>

<template>
    <img :class="sizes[size]" src="../../assets/logo.png" loading="lazy">
</template>