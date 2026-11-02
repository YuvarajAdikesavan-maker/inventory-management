<template>
  <div>
    <h2>{{ t('overview.title') }}</h2>
    <div class="row">
      <div class="panel stat"><span>{{ t('overview.open') }}</span><strong>{{ open }}</strong></div>
      <div class="panel stat"><span>{{ t('overview.late') }}</span><strong>{{ late }}</strong></div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useFilters } from '../composables/useFilters'

export default {
  name: 'Overview',
  setup() {
    const { t } = useI18n()
    const { warehouse } = useFilters()
    const orders = [
      { id: 'A-100', warehouse: 'Tokyo', status: 'open' },
      { id: 'A-101', warehouse: 'London', status: 'late' },
      { id: 'A-102', warehouse: 'Tokyo', status: 'open' }
    ]
    const scoped = computed(() => orders.filter(o => warehouse.value === 'all' || o.warehouse === warehouse.value))
    const open = computed(() => scoped.value.filter(o => o.status === 'open').length)
    const late = computed(() => scoped.value.filter(o => o.status === 'late').length)
    return { t, open, late }
  }
}
</script>

<style scoped>
h2 { margin: 0 0 12px; font-size: 25px; }
.row { display: flex; gap: 12px; }
.stat { width: 200px; display: flex; flex-direction: column; gap: 6px; }
.stat strong { font-size: 26px; }
</style>
