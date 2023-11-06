<script setup lang="ts">
import { computed, ref, watch } from 'vue';

import Sep from '@/components/App/Sep.vue';
import Table from '@/components/Leaderboard/Table.vue';
import Dropdown from '@/components/Leaderboard/Dropdown.vue';
import SearchBar from '@/components/Leaderboard/SearchBar.vue';
import Pagination from '@/components/Leaderboard/Pagination.vue';
import { TopDailyUserData } from '@/types/users'
import { useFetchObject } from '@/composables/useFetch';

const page = ref(1)
const entries = ref(10)
const keywords = ref('')

const topUsersData = await useFetchObject<TopDailyUserData>(
    `/api/users/most-active-daily?page=${page.value}&per_page=${entries.value}`, false
    )
const topUsers = ref(topUsersData.obj.value?.users)
const totalPages = ref(topUsersData.obj.value?.total_pages)

watch(() => [page.value, entries.value], async ([newPage, newEntries], [_, oldEntries]) => {
    if (newEntries !== oldEntries) {
        newPage = 1
        page.value = 1
    }

    const newTopUsersData = await useFetchObject<TopDailyUserData>(
            `/api/users/most-active-daily?page=${newPage}&per_page=${newEntries}`, false
            )
    topUsers.value = newTopUsersData.obj.value?.users
    totalPages.value = newTopUsersData.obj.value?.total_pages
})

const filteredTopUsers = computed(() => {
    if (!keywords.value) {
        return topUsers.value
    }

    const keyword = keywords.value.toLowerCase()
    return topUsers.value?.filter(user => user.username.includes(keyword))
})
</script>

<template>
    <Sep is-sticky title="Top Daily Users" />
    <Dropdown v-model:entries="entries" />
    <SearchBar v-model:keywords="keywords" />
    <Table 
        :data="filteredTopUsers" 
        :data-length="filteredTopUsers?.length" 
        :data-total="topUsersData.obj.value?.total_users"
        :page="page"
        :entries="entries" />
    <Pagination v-model:active-page="page" :pages="totalPages" />
</template>