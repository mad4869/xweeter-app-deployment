import { User } from "./auth";

type FollowResponse = {
    success: boolean
    data: User[]
}

type FollowDetailResponse = {
    following: FollowResponse
    followers: FollowResponse
}

type WhoToFollow = {
    user_id: number,
    username: string,
    full_name: string,
    body: string,
    profile_pic: string
}

type WhoToFollowResponse = {
    data: WhoToFollow[],
    success: boolean
}

type ToFollowResponse = {
    message: string,
    success: boolean
}

export { 
    type FollowResponse, 
    type FollowDetailResponse, 
    type WhoToFollow, 
    type WhoToFollowResponse, 
    type ToFollowResponse 
}