import { User } from './auth'

type UserResponse = {
    data: User
    success: boolean
}

type TopDailyUser = {
    user_id: number
    username: string
    full_name: string
    xweet_count: number
}

type TopDailyUserData = {
    users: TopDailyUser[],
    total_users: number,
    total_pages: number
}

type TopDailyUserResponse = {
    data: TopDailyUserData
    success: boolean
}

export { type UserResponse, type TopDailyUser, type TopDailyUserData, type TopDailyUserResponse }