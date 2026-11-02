<template>
  <div class="app">
    <header class="top-nav">
      <div class="nav-inner">
        <h1 class="logo">Billing Admin</h1>
        <nav class="links">
          <router-link to="/" :class="{ active: $route.path === '/' }">Dashboard</router-link>
          <router-link to="/customers" :class="{ active: $route.path === '/customers' }">Customers</router-link>
          <router-link to="/invoices" :class="{ active: $route.path === '/invoices' }">Invoices</router-link>
          <router-link to="/settings" :class="{ active: $route.path === '/settings' }">Settings</router-link>
        </nav>
        <button class="user-btn" @click="menuOpen = !menuOpen">
          Jordan Lee
        </button>
        <ul v-if="menuOpen" class="user-menu">
          <li>Profile</li>
          <li @click="menuOpen = false">Sign out</li>
        </ul>
      </div>
    </header>
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'App',
  setup() {
    const menuOpen = ref(false)
    return { menuOpen }
  }
}
</script>

<style>
body { margin: 0; font-family: Arial, sans-serif; background: #f4f4f4; color: #333; }
.top-nav { background: #1f3a5f; color: white; position: relative; }
.nav-inner { display: flex; align-items: center; padding: 14px 22px; }
.logo { font-size: 20px; margin: 0 40px 0 0; }
.links a { color: #cbd5e1; text-decoration: none; margin-right: 18px; padding: 6px 10px; border-radius: 3px; }
.links a.active { background: #2f5a8f; color: white; }
.user-btn { margin-left: auto; background: transparent; border: 1px solid #5b7aa3; color: white; padding: 6px 12px; cursor: pointer; }
.user-menu { position: absolute; right: 22px; top: 52px; background: white; color: #333; list-style: none; margin: 0; padding: 6px 0; box-shadow: 0 2px 8px rgba(0,0,0,.2); width: 140px; }
.user-menu li { padding: 8px 14px; cursor: pointer; }
.content { padding: 28px 34px; max-width: 1200px; margin: 0 auto; }
.box { background: white; border: 1px solid #ddd; border-radius: 4px; padding: 18px; margin-bottom: 22px; }
.box h3 { margin: 0 0 12px 0; font-size: 17px; }
.tbl { width: 100%; border-collapse: collapse; }
.tbl th { text-align: left; background: #eee; padding: 9px; font-size: 13px; }
.tbl td { padding: 9px; border-bottom: 1px solid #eee; font-size: 14px; }
.pill { padding: 3px 9px; border-radius: 10px; font-size: 12px; }
.pill.paid { background: #d4edda; color: #155724; }
.pill.due { background: #fff3cd; color: #856404; }
.pill.late { background: #f8d7da; color: #721c24; }
</style>
