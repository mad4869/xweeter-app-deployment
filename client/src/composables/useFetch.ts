import { ref, Ref, toRef, toValue } from 'vue'
import { AxiosError } from 'axios'

import { sendReqCookie, sendReqWoCookie } from "@/utils/axiosInstances"

const useFetchObject = async<T> (url: string | Ref<string>, authenthicated: boolean) => {
    const obj = ref<T | null>()
    const error = ref<string | null>()

    if (authenthicated) {
        try {
            const { data } = await sendReqCookie.get(toValue(url))
                if (data?.success) {
                    obj.value = data.data as T
                }
        } catch (err) {
            error.value = (err as AxiosError).message
        }
    } else {
        try {
            const { data } = await sendReqWoCookie.get(toValue(url))
                if (data?.success) {
                    obj.value = data.data as T
                }
        } catch (err) {
            error.value = (err as AxiosError).message
        }
    }

    return { obj, error }
}

const useFetchList = async<T> (url: string | Ref<string>, authenthicated: boolean) => {
    const list: Ref<T[] | null | undefined> = toRef(ref())
    const error = ref<string | null>()

    if (authenthicated) {
        try {
            const { data } = await sendReqCookie.get(toValue(url))
                if (data?.success) {
                    list.value = data.data as T[]
                }
        } catch (err) {
            error.value = (err as AxiosError).message
        }
    } else {
        try {
            const { data } = await sendReqWoCookie.get(toValue(url))
                if (data?.success) {
                    list.value = data.data as T[]
                }
        } catch (err) {
            error.value = (err as AxiosError).message
        }
    }

    return { list, error }
}

export { useFetchObject, useFetchList }