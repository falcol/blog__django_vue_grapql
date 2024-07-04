import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './index.css'
import { apolloProvider } from '@/apollo-config'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(apolloProvider)
app.mount('#app')
