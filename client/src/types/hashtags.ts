interface Hashtags {
    hashtag_id: number
    body: string
}

interface Trending extends Hashtags {
    xweet_count: number
}

type HashtagResponse = {
    success: boolean
    data: Hashtags[]
}

type TrendingResponse = {
    success: boolean
    data: Trending[]
}

export { type HashtagResponse, type Trending, type TrendingResponse }