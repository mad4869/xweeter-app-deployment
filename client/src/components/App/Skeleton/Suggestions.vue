<template>
    <section class="flex flex-col flex-1 gap-4 overflow-hidden border border-solid border-sky-800 rounded-xl">
        <div class="flex items-center justify-between px-4 py-2 bg-sky-600">
            <span class="font-semibold text-white">Who to Follow</span>
            <font-awesome-icon icon="fa-regular fa-user" class="text-white" />
        </div>
        <div v-for="_ in 2" class="flex flex-col justify-center gap-2 overflow-scroll">
            <section class="flex flex-col items-center gap-2 px-8 py-1">
                <div class="grid w-full grid-cols-4 grid-rows-2 gap-y-1">
                    <div class="flex items-center col-span-1 col-start-1 row-span-2 row-start-1">
                        <div alt="Profile Pic"
                            class="w-8 h-8 border border-solid rounded-full bg-slate-600 border-sky-800 animate-pulse">
                        </div>
                    </div>
                    <div class="col-span-3 col-start-2 row-span-1 row-start-1 rounded-sm bg-slate-600 animate-pulse"></div>
                    <div class="col-span-3 col-start-2 row-span-1 row-start-2 rounded-sm bg-slate-600 animate-pulse"></div>
                </div>
                <div class="w-full h-8 rounded-sm bg-slate-600 animate-pulse">
                </div>
            </section>
        </div>
    </section>
</template>