<script setup lang="ts">
const props = defineProps<{
    activePage: number
    pages: number | undefined
}>()
const emit = defineEmits<{
    (e: 'update:active-page', value: number): void
}>()

const changePage = (page: number) => {
    emit('update:active-page', page)
}
const nextPage = () => {
    if (props.activePage < (props.pages ?? 0)) {
        emit('update:active-page', props.activePage + 1)
    }
}
const prevPage = () => {
    if (props.activePage > 1) {
        emit('update:active-page', props.activePage - 1)
    }
}
</script>

<template>
    <section class="flex justify-between items-center px-2 py-2 bg-sky-800/20 backdrop-blur-sm">
        <font-awesome-icon 
            icon="fa-regular fa-square-caret-left" 
            class="text-sky-800 cursor-pointer"
            @click="prevPage" />
        <div class="flex items-center gap-1">
            <div 
                v-for="page in pages"
                class="px-2 text-sky-800 dark:text-white cursor-pointer"
                :class="page === activePage ? 'bg-sky-800 text-white rounded' : ''"
                @click="changePage(page)">
                {{ page }}
            </div>
        </div>
        <font-awesome-icon 
            icon="fa-regular fa-square-caret-right" 
            class="text-sky-800 cursor-pointer"
            @click="nextPage" />
    </section>
</template>