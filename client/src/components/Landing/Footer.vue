<template>
    <footer class="row-start-6 col-span-2 flex justify-end items-center">
        <router-link to="/home">
            <button
                class="flex items-center gap-2 w-fit px-2 py-1 text-xs text-sky-900 transition-transform duration-300 ease-in-out hover:text-sky-600 hover:underline hover:decoration-sky-600 group hover:-translate-x-1"
                title="Go to homepage">
                See the others' stories now!
                <font-awesome-icon icon="fa-solid fa-arrow-right" class="hidden group-hover:block" />
            </button>
        </router-link>
    </footer>
</template>