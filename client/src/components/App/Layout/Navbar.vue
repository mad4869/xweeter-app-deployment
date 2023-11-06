<script setup lang="ts">
import { ref } from 'vue';
import { onClickOutside } from '@vueuse/core';

import Logo from '@/components/App/Logo.vue';
import useAuthStore from '@/stores/useAuthStore';

const authStore = useAuthStore()

defineEmits<{
    (e: 'show-signout-modal'): void
}>()

const showMenu = ref(false)
const menu = ref<HTMLElement | null>(null)
onClickOutside(menu, () => {
    showMenu.value = false
})
</script>

<template>
    <nav
        class="sticky top-0 z-20 grid grid-cols-4 px-20 py-4 mx-auto text-white border-b border-solid place-items-center bg-sky-600/90 backdrop-blur border-sky-900 dark:bg-slate-900/90 dark:text-white dark:shadow-md dark:shadow-sky-600/50">
        <div class="col-span-1"></div>
        <div class="flex items-center justify-center col-span-2">
            <router-link to="/home" title="Home">
                <Logo size="sm" />
            </router-link>
        </div>
        <div  
            class="items-center justify-end hidden w-full col-span-1 text-sm sm:flex min-w-max md:text-base">
            <button
                v-if="authStore.getIsAuthenticated" 
                class="navbar-menu hover:bg-slate-900/10 dark:hover:bg-sky-600/10">
                <router-link 
                    :to="`/users/${authStore.getSignedInUserId}`" 
                    title="View your profile" 
                    active-class="active">
                    Profile
                </router-link>
            </button>
            <button  
                class="navbar-menu hover:bg-slate-900/10 dark:hover:bg-sky-600/10">
                <router-link 
                    to="/leaderboard" 
                    title="View leaderboard" 
                    active-class="active">
                    Leaderboard
                </router-link>
            </button>
            <button 
                v-if="authStore.getIsAuthenticated && authStore.getSignedInRole === 'admin'" 
                class="navbar-menu hover:bg-slate-900/10 dark:hover:bg-sky-600/10">
                <router-link 
                    to="/admin" 
                    title="View admin dashboard"
                    active-class="active">
                    Admin
                </router-link>
            </button>
            <button 
                v-if="authStore.getIsAuthenticated"
                class="navbar-menu hover:bg-red-600/80 dark:hover:bg-red-600/30 hover:text-white" 
                @click="$emit('show-signout-modal')"
                title="Sign Out">
                Sign Out
            </button>
        </div>
        <div class="flex items-center justify-end w-full col-span-1 sm:hidden">
            <font-awesome-icon icon="fa-solid fa-bars" class="cursor-pointer" @click="showMenu = true" />
        </div>
        <div 
            v-if="showMenu"
            ref="menu" 
            class="absolute flex flex-col border border-solid rounded-md top-12 right-8 bg-white/70 dark:bg-slate-900/70 backdrop-blur-md text-slate-400 border-slate-400/70">
            <button
                v-if="authStore.getIsAuthenticated" 
                class="navbar-menu hover:bg-sky-600/10">
                <router-link 
                    :to="`/users/${authStore.getSignedInUserId}`" 
                    title="View your profile" 
                    active-class="active">
                    Profile
                </router-link>
            </button>
            <button  
                class="navbar-menu hover:bg-sky-600/10">
                <router-link 
                    to="/leaderboard" 
                    title="View leaderboard" 
                    active-class="active">
                    Leaderboard
                </router-link>
            </button>
            <button 
                v-if="authStore.getIsAuthenticated && authStore.getSignedInRole === 'admin'" 
                class="navbar-menu hover:bg-sky-600/10">
                <router-link 
                    to="/admin" 
                    title="View admin dashboard"
                    active-class="active">
                    Admin
                </router-link>
            </button>
            <button
                v-if="authStore.getIsAuthenticated" 
                class="navbar-menu hover:bg-red-600/80 dark:hover:bg-red-600/30 hover:text-white" 
                @click="$emit('show-signout-modal')"
                title="Sign Out">
                Sign Out
            </button>
        </div>
    </nav>
</template>

<style scoped>
.active {
    @apply text-slate-900 dark:text-sky-600
}
.navbar-menu {
    @apply px-2 py-1 rounded-md cursor-pointer transition-colors ease-in hover:backdrop-blur-md
}
</style>