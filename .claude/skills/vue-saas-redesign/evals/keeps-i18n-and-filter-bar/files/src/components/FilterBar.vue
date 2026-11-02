<template>
  <div class="filter-bar">
    <label>
      {{ t('filters.warehouse') }}
      <select v-model="warehouse">
        <option value="all">{{ t('filters.all') }}</option>
        <option value="Tokyo">{{ t('filters.tokyo') }}</option>
        <option value="London">{{ t('filters.london') }}</option>
      </select>
    </label>
  </div>
</template>

<script>
import { useI18n } from '../composables/useI18n'
import { useFilters } from '../composables/useFilters'

export default {
  name: 'FilterBar',
  setup() {
    const { t } = useI18n()
    const { warehouse } = useFilters()
    return { t, warehouse }
  }
}
</script>

<style scoped>
.filter-bar { background: #fff; border-bottom: 1px solid #ddd; padding: 10px 24px; font-size: 13px; }
.filter-bar select { margin-left: 8px; padding: 4px 6px; }
</style>
