<template>
  <div>
    <h2>{{ t('orders.title') }}</h2>
    <div class="panel">
      <table>
        <thead><tr><th>{{ t('orders.number') }}</th><th>{{ t('orders.warehouse') }}</th><th>{{ t('orders.status') }}</th></tr></thead>
        <tbody>
          <tr v-for="o in scoped" :key="o.id"><td>{{ o.id }}</td><td>{{ o.warehouse }}</td><td>{{ o.status }}</td></tr>
          <tr v-if="scoped.length === 0"><td colspan="3">{{ t('orders.empty') }}</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useFilters } from '../composables/useFilters'

export default {
  name: 'Orders',
  setup() {
    const { t } = useI18n()
    const { warehouse } = useFilters()
    const orders = [
      { id: 'A-100', warehouse: 'Tokyo', status: 'open' },
      { id: 'A-101', warehouse: 'London', status: 'late' },
      { id: 'A-102', warehouse: 'Tokyo', status: 'open' }
    ]
    const scoped = computed(() => orders.filter(o => warehouse.value === 'all' || o.warehouse === warehouse.value))
    return { t, scoped }
  }
}
</script>

<style scoped>
h2 { margin: 0 0 14px; font-size: 22px; }
</style>
