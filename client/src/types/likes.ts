interface Like {
    like_id: number,
    user_id: number,
    xweet_id: number,
    created_at: string,
    updated_at?: string
}

interface LikeDetail extends Like {
    body: string,
    media?: string,
    username: string,
    full_name: string,
    profile_pic: string,
    og_user_id: number,
    og_username: string,
    og_full_name: string,
    og_profile_pic: string,
    og_created_at: string,
    og_updated_at?: string
}

type LikeResponse = {
    data: Like,
    success: boolean
}

type LikeDetailResponse = {
    data: LikeDetail[]
    success: boolean
}

export { type LikeResponse, type LikeDetail, type LikeDetailResponse }