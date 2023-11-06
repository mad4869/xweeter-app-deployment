import { ref } from 'vue'

import { sendReqWoCookie } from "@/utils/axiosInstances"

export enum Features {
    Xweets = 'xweets',
    Replies = 'replies',
    Rexweets = 'rexweets',
    Likes = 'likes',
    Following = 'following',
    Followers = 'followers'
}

const useCount = async (subject: 'users' | 'xweets', id: number | undefined, feature: Features) => {
    const count = ref<number>(0)

    if (!id) {
        return count
    }

    try {
        const { data } = await sendReqWoCookie.get(`/api/${subject}/${id}/${feature}`)
            if (data?.success) {

                count.value = data.data.length
            }
    } catch (err) {
        console.error(err)
    }

    return count
}

export default useCount