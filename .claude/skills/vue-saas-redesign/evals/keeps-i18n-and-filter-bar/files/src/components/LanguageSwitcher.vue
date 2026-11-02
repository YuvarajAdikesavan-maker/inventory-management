<template>
  <div class="lang">
    <button :class="{ on: locale === 'en' }" @click="setLocale('en')">EN</button>
    <button :class="{ on: locale === 'ja' }" @click="setLocale('ja')">JA</button>
  </div>
</template>

<script>
import { useI18n } from '../composables/useI18n'

export default {
  name: 'LanguageSwitcher',
  setup() {
    const { locale, setLocale } = useI18n()
    return { locale, setLocale }
  }
}
</script>

<style scoped>
.lang button { background: transparent; border: 1px solid #5b6b7f; color: #cbd5e1; padding: 3px 8px; cursor: pointer; }
.lang button.on { background: #3b82f6; color: #fff; border-color: #3b82f6; }
</style>
