import { ref } from 'vue'
import en from '../locales/en'
import ja from '../locales/ja'

const messages = { en, ja }
const locale = ref('en')

export function useI18n() {
  const t = (key) => key.split('.').reduce((o, k) => (o ? o[k] : undefined), messages[locale.value]) || key
  const setLocale = (l) => { locale.value = l }
  return { t, locale, setLocale }
}
