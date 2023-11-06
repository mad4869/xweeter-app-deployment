import axios from 'axios'

const REQ_TOKEN_CONFIG = {
    withCredentials: true,
    xsrfCookieName: 'csrf_access_token'
}

const getCookie = (name: string) => {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop()?.split(';').shift() ?? undefined
}

const GET_TOKEN_CONFIG = {
    credentials: 'same-origin',
    headers: {
        'X-CSRF-TOKEN': getCookie('csrf_access_token')
    }
}

const authService = axios.create(REQ_TOKEN_CONFIG);
const sendReqCookie = axios.create(GET_TOKEN_CONFIG)
const sendReqWoCookie = axios.create()

export { authService, sendReqCookie, sendReqWoCookie }