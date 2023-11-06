import { Ref } from "vue"

type Notification = {
    isNotified: boolean,
    category: 'success' | 'error' | undefined | null
    msg: string
}

const useNotify = (notification: Ref<Notification>, category: 'success' | 'error', msg: string) => {
    notification.value.isNotified = true
    notification.value.category = category
    notification.value.msg = msg

    setTimeout(() => {
        notification.value.isNotified = false
        notification.value.category = null
        notification.value.msg = ''
    }, 3000)
}

export default useNotify