import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Overview from './views/Overview.vue'
import Orders from './views/Orders.vue'
import Reports from './views/Reports.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Overview },
    { path: '/orders', component: Orders },
    { path: '/reports', component: Reports }
  ]
})

createApp(App).use(router).mount('#app')
