interface Rexweet {
    rexweet_id: number
    user_id: number
    xweet_id: number
    created_at: string
    updated_at?: string
}

interface RexweetDetail extends Rexweet {
    body: string
    media: string
    og_user_id: string
    og_username: string
    og_full_name: string
    og_profile_pic: string
}

type RexweetResponse = {
    data: Rexweet
    success: boolean
}

type RexweetDetailResponse = {
    data: RexweetDetail[]
    success: boolean
}

export { type RexweetResponse, type RexweetDetail, type RexweetDetailResponse }