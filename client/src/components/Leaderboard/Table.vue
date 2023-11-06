<script setup lang="ts">
import { ref, watch } from 'vue';

import { TopDailyUser } from '@/types/users'

const props = defineProps<{
    data: TopDailyUser[] | undefined
    dataLength: number | undefined
    dataTotal: number | undefined
    page: number
    entries: number
}>()

const initialIndex = ref(0)
const lastIndex = ref(0)

watch(() => [props.page, props.entries, props.dataLength], () => {
    initialIndex.value = props.dataLength ? props.page === 1 ? 1 : props.entries + 1 : 0
    lastIndex.value = (props.dataLength as number) >= props.entries ? 
                (props.dataLength as number) * props.page : 
                props.dataLength ?? 0
}, {
    immediate: true
})

</script>

<template>
    <section class="dark:text-sky-600 text-sky-800 h-table">
        <table class="w-full text-center border-separate table-auto text-sky-800 dark:text-white">
            <thead class="text-white bg-sky-800">
                <tr>
                    <th>No.</th>
                    <th>Users</th>
                    <th>Xweets Count</th>
                </tr>
            </thead>
            <tbody class="bg-sky-800/30">
                <tr v-for="(user, index) in data">
                    <td>{{ page === 1 ? index + 1 : index + 1 + entries }}</td>
                    <td class="hover:text-sky-600" :title="`View @${user.username}'s profile'`">
                        <router-link :to="`/users/${user.user_id}`">@{{ user.username }}</router-link>
                    </td>
                    <td>{{ user.xweet_count }}</td>
                </tr>
            </tbody>
        </table>
        <p>
            Showing {{ initialIndex }} {{ initialIndex < lastIndex ? `- ${lastIndex}` : '' }} of 
            {{ dataTotal }} {{ dataTotal === 1 ? 'entry' : 'entries' }}
        </p>
    </section>
</template>

<style scoped>
.h-table {
    min-height: calc(100vh - 20rem);
}
</style>