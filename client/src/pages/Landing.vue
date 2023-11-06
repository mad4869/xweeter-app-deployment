<script setup lang="ts">
import Hero from '@/components/Landing/Hero.vue'
import Cta from '@/components/Landing/Cta.vue';
import Footer from '@/components/Landing/Footer.vue';
</script>

<template>
    <main
        class="grid grid-rows-6 grid-cols-2 gap-x-16 w-[100vw] h-[100vh] px-20 pt-12 bg-gradient-to-tl from-slate-900 from-20% to-sky-800">
        <Hero />
        <Cta />
        <Footer />
    </main>
</template>