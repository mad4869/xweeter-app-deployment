<template>
    <section class="flex flex-col gap-4">
        <div v-for="_ in 3"
            class="flex items-center justify-center gap-4 px-4 py-4 border border-solid bg-sky-600/10 backdrop-blur-lg border-sky-800 rounded-xl">
            <div class="flex flex-col items-center flex-1 h-full gap-2 px-4 border-r border-solid border-sky-600/20">
                <div class="w-10 h-10 border border-solid rounded-full bg-slate-600 border-sky-800 animate-pulse"></div>
                <div class="flex flex-col items-center justify-center w-full gap-2 text-center">
                    <div v-for="_ in 2" class="w-full h-4 rounded-sm bg-slate-600 animate-pulse"></div>
                </div>
            </div>
            <div class="flex flex-col items-center justify-center w-4/5 h-full gap-2">
                <div v-for="_ in 3" class="w-full h-4 rounded-sm bg-slate-600 animate-pulse"></div>
            </div>
        </div>
    </section>
</template>