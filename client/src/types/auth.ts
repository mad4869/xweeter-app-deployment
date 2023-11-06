enum UserAuth {
    SignUp,
    SignIn
}

type User = {
    user_id: number,
    username: string,
    full_name: string,
    email: string,
    bio: string | null,
    role: 'admin' | 'user',
    profile_pic: string,
    header_pic: string,
    created_at: string,
    updated_at: string | null
}

type AuthResponse = {
    success: boolean
    message: string,
    user: User
}

type AuthState = {
    isAuthenticated: boolean,
    signedInUserId: number | undefined,
    signedInUsername: string | undefined
    signedInFullname: string | undefined,
    signedInEmail: string | undefined,
    signedInBio: string | undefined | null,
    signedInRole: 'admin' | 'user' | undefined,
    signedInPfp: string | undefined,
    signedInHeader: string | undefined,
    signedInJoindate: string | undefined,
    signedInUpdate: string | undefined | null,
    errorMsg: string | undefined
}

export { UserAuth, type User, type AuthResponse, type AuthState }