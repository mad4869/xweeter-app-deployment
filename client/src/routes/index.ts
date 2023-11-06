import { createRouter, createWebHashHistory, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'

import Home from '@/pages/Home.vue'
import Landing from '@/pages/Landing.vue'
import Profile from '@/pages/Profile.vue'
import Leaderboard from '@/pages/Leaderboard.vue'
import Trending from '@/pages/Trending.vue'
import Xweet from '@/pages/Xweet.vue'
import Admin from '@/pages/Admin.vue'
import NotFound from '@/pages/404.vue'
import useAuthStore from '@/stores/useAuthStore'

const APP_NAME = 'Xweeter'

const routes = [
    { 
        path: '/',  
        component: Landing, 
        beforeEnter: async (_: RouteLocationNormalized, __: RouteLocationNormalized, next: NavigationGuardNext) => {
        const authStore = useAuthStore()
        await authStore.getUser()

        if (authStore.getIsAuthenticated) {
            next('/home')
        } else {
            next()
        }
    }},
    { path: '/home', name: 'Home', component: Home, meta: { title: `${APP_NAME} - Home` } },
    { path: '/users/:id', name: 'Profile', component: Profile, meta: { title: `${APP_NAME} - Profile` }, children: [
        { path: 'following', component: Profile },
        { path: 'followers', component: Profile },
        { path: 'likes', component: Profile },
    ] },
    { path: '/leaderboard', name: 'Leaderboard', component: Leaderboard, meta: { title: `${APP_NAME} - Leaderboard` } },
    { path: '/trending', name: 'Trending', component: Trending, meta: { title: `${APP_NAME} - Trending` } },
    { path: '/xweets/:id', name: 'Xweet', component: Xweet, meta: { title: `${APP_NAME} - Xweet` } },
    { 
        path: '/admin', 
        name: 'Admin', 
        component: Admin, 
        meta: { title: `${APP_NAME} - Admin` },
        beforeEnter: async (_: RouteLocationNormalized, __: RouteLocationNormalized, next: NavigationGuardNext) => {
            const authStore = useAuthStore()
            await authStore.getUser()

            if (!authStore.getIsAuthenticated || (authStore.getIsAuthenticated && authStore.getSignedInRole !== 'admin')) {
                next('/home')
            } else {
                next()
            }
        }
    },
    { path: '/:pathMatch(.*)*', name: '404', component: NotFound, meta: { title: `${APP_NAME} - 404` } }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

router.beforeEach((to, _, next) => {
    document.title = to.meta.title as string || APP_NAME 
    next()
})

export default router