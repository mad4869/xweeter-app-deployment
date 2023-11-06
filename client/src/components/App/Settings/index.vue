<script setup lang="ts">
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'
import { useDark } from '@vueuse/core'

const isDark = useDark()
</script>

<template>
    <section 
        class="flex flex-col flex-1 gap-4 overflow-hidden border border-solid border-sky-800 rounded-xl">
        <div class="flex items-center justify-between px-4 py-2 bg-sky-600">
            <span class="font-semibold text-white">Settings</span>
            <font-awesome-icon icon="fa-solid fa-gear" class="text-white" />
        </div>
        <SwitchGroup>
            <div class="flex items-center gap-2 px-4 group">
                <SwitchLabel passive>
                    <font-awesome-icon icon="fa-regular fa-sun" class="text-sky-800 dark:text-white" />
                </SwitchLabel>
                <Switch 
                    v-model="isDark"
                    class="relative inline-flex items-center h-6 transition-colors rounded-full w-11 bg-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-800 focus:ring-offset-2 dark:bg-sky-600">
                    <span 
                        class="inline-block w-4 h-4 transition-transform transform translate-x-1 bg-white rounded-full dark:translate-x-6" />
                </Switch>
                <SwitchLabel passive>
                    <font-awesome-icon icon="fa-regular fa-moon" class="text-sky-800 dark:text-white" />
                </SwitchLabel>
            </div>
        </SwitchGroup>
    </section>
</template>