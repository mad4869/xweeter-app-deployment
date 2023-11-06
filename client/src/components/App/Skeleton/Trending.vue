<template>
    <section class="flex flex-col flex-1 gap-3 overflow-hidden border border-solid border-sky-800 rounded-xl">
        <div class="flex items-center justify-between px-4 py-2 bg-sky-600">
            <span class="font-semibold text-white">Trending</span>
        </div>
        <div v-for="_ in 3" class="flex flex-col w-3/4 gap-2 mx-auto">
            <div class="w-full h-8 rounded-sm bg-slate-600 animate-pulse"></div>
            <div class="w-full h-4 rounded-sm bg-slate-600 animate-pulse"></div>
        </div>
    </section>
</template>