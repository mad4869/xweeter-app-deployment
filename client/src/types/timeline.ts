type ProfileTimeline = {
    xweet_id: number
    user_id: number
    username: string
    full_name: string
    body: string
    media?: string
    profile_pic: string
    created_at: string
    updated_at?: string
    rexweet_id?: number
    og_user_id?: number
    og_username?: string
    og_full_name?: string
    og_profile_pic?: string
    og_created_at?: string,
    og_updated_at?: string
}

type ProfileTimelineResponse = {
    data: ProfileTimeline[]
    success: boolean
}

export { type ProfileTimeline, type ProfileTimelineResponse }