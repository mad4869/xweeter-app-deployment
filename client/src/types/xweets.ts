type XweetDetail = {
    xweet_id: number,
    user_id: number,
    full_name: string,
    username: string,
    body: string,
    media?: string,
    profile_pic: string,
    created_at: string,
    updated_at?: string
}

type XweetResponse = {
    data: XweetDetail,
    success: boolean
}

type XweetsResponse = {
    data: XweetDetail[],
    success: boolean
}

enum XweetMode {
    NewXweet,
    EditXweet,
    ReplyXweet
}

export { type XweetDetail, type XweetResponse, type XweetsResponse, XweetMode}
