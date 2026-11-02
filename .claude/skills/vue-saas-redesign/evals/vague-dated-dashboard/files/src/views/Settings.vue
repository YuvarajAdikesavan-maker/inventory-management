<template>
  <div>
    <h2 class="title">Settings</h2>
    <div class="box">
      <h3>Company</h3>
      <label class="field">Company name <input v-model="company" /></label>
      <label class="field">Billing email <input v-model="email" type="email" /></label>
      <label class="field">
        Default payment terms
        <select v-model="terms"><option>Net 15</option><option>Net 30</option><option>Net 60</option></select>
      </label>
      <button class="save" @click="saved = true">Save changes</button>
      <span v-if="saved" class="ok">Saved</span>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Settings',
  setup() {
    const company = ref('Billing Co')
    const email = ref('billing@example.com')
    const terms = ref('Net 30')
    const saved = ref(false)
    return { company, email, terms, saved }
  }
}
</script>

<style scoped>
.title { font-size: 27px; margin: 0 0 16px; }
.field { display: block; margin-bottom: 14px; font-size: 14px; }
.field input, .field select { display: block; margin-top: 5px; padding: 7px; width: 300px; }
.save { background: #1f3a5f; color: white; border: 0; padding: 9px 18px; cursor: pointer; }
.ok { margin-left: 12px; color: green; }
</style>
