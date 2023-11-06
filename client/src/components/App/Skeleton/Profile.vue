<template>
    <section class="flex-[4] grid grid-rows-4 border border-solid border-sky-800 rounded-xl">
        <div class="flex items-center justify-center w-full row-start-1 gap-4 border-b border-solid border-sky-600/20">
            <div class="w-12 h-12 border border-solid rounded-full bg-slate-600 border-sky-800 animate-pulse"></div>
            <div class="flex flex-col items-center justify-center h-full gap-2">
                <div v-for="_ in 2" class="w-24 h-4 rounded-sm bg-slate-600 animate-pulse"></div>
            </div>
        </div>
        <div
            class="flex flex-col items-center justify-center w-full row-start-2 gap-1 border-b border-solid border-sky-600/20">
            <div v-for="_ in 2" class="w-24 h-4 rounded-sm bg-slate-600 animate-pulse"></div>
        </div>
        <div
            class="flex flex-col items-center justify-center w-full row-start-3 gap-1 border-b border-solid border-sky-600/20">
            <div v-for="_ in 2" class="w-24 h-4 rounded-sm bg-slate-600 animate-pulse"></div>
        </div>
        <div class="flex items-center justify-center row-start-4">
            <div class="h-8 rounded-sm w-36 bg-slate-600 animate-pulse"></div>
        </div>
    </section>
</template>