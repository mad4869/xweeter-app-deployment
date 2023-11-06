import { reactive } from "vue";

export const countStore = reactive({
    xweetsCount: 0,
    incrementXweetsCount() {
        this.xweetsCount++
    },
    decrementXweetsCount() {
        this.xweetsCount--
    },
})