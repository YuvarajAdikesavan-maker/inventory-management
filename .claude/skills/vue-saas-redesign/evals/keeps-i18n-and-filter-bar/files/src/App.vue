<template>
  <div class="app">
    <header class="top-nav">
      <h1 class="logo">{{ t('nav.company') }}</h1>
      <nav class="links">
        <router-link to="/" :class="{ active: $route.path === '/' }">{{ t('nav.overview') }}</router-link>
        <router-link to="/orders" :class="{ active: $route.path === '/orders' }">{{ t('nav.orders') }}</router-link>
        <router-link to="/reports" :class="{ active: $route.path === '/reports' }">Reports</router-link>
      </nav>
      <LanguageSwitcher />
    </header>
    <FilterBar />
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { useI18n } from './composables/useI18n'
import FilterBar from './components/FilterBar.vue'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

export default {
  name: 'App',
  components: { FilterBar, LanguageSwitcher },
  setup() {
    const { t } = useI18n()
    return { t }
  }
}
</script>

<style>
body { margin: 0; font-family: Helvetica, Arial, sans-serif; background: #f2f3f5; color: #222; }
.top-nav { display: flex; align-items: center; gap: 30px; background: #111827; color: #fff; padding: 12px 24px; }
.logo { font-size: 19px; margin: 0; }
.links { display: flex; gap: 6px; margin-right: auto; }
.links a { color: #9ca3af; text-decoration: none; padding: 6px 12px; border-radius: 4px; }
.links a.active { color: #fff; background: #374151; }
.content { padding: 26px 30px; }
.panel { background: #fff; border: 1px solid #e0e0e0; padding: 16px; border-radius: 4px; margin-bottom: 20px; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 8px; background: #f0f0f0; font-size: 12px; }
td { padding: 8px; border-bottom: 1px solid #eee; font-size: 14px; }
</style>
