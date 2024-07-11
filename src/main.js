import { createApp } from 'vue'
import VueCookies from 'vue-cookies'

import App from './App.vue'
import './index.css'

createApp(App).use(VueCookies).mount('#app')
