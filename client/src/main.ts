import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { 
    faSun, faMoon, faUser, faHeart, faTrashCan, faCircleXmark, faPenToSquare, faComment, faSquareCaretLeft, faSquareCaretRight
} from '@fortawesome/free-regular-svg-icons'
import { 
    faGear, faFont, faUser as faUserSol, faEnvelope, faLock, faArrowRight, faSpinner, faGlobe, faRetweet, faHeart as faHeartSol, faImages, faFeather, faPenToSquare as faPenToSquareSol, faClipboardCheck, faTriangleExclamation, faCheck, faAddressCard, faImagePortrait, faPanorama, faComment as faCommentSol, faCircleNotch, faDownload, faMagnifyingGlass, faBars
} from '@fortawesome/free-solid-svg-icons'
import './style.css'

import App from './App.vue'
import router from './routes'

library.add(
    faSun, faMoon, faUser, faUserSol, faGear, faFont, faEnvelope, faLock, faArrowRight, faSpinner, faGlobe, faRetweet, faHeart, faHeartSol, faTrashCan, faImages, faCircleXmark, faFeather, faPenToSquare, faPenToSquareSol, faClipboardCheck, faTriangleExclamation, faCheck, faAddressCard, faImagePortrait, faPanorama, faComment, faCommentSol, faSquareCaretLeft, faSquareCaretRight, faCircleNotch, faDownload, faMagnifyingGlass, faBars
)

const pinia = createPinia()

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(pinia)
app.use(router)
app.mount('#app')
