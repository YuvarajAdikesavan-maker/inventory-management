import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import Customers from './views/Customers.vue'
import Invoices from './views/Invoices.vue'
import Settings from './views/Settings.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/customers', component: Customers },
    { path: '/invoices', component: Invoices },
    { path: '/settings', component: Settings }
  ]
})

createApp(App).use(router).mount('#app')
