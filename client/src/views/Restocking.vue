<template>
  <div class="restocking">
    <div class="page-header">
      <h2>{{ t('restocking.title') }}</h2>
      <p>{{ t('restocking.description') }}</p>
    </div>

    <div v-if="loading" class="loading">{{ t('common.loading') }}</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="card budget-card">
        <div class="budget-header">
          <label class="budget-label" for="budget-slider">{{ t('restocking.budget') }}</label>
          <span class="budget-value">{{ currencySymbol }}{{ budget.toLocaleString() }}</span>
        </div>
        <input
          id="budget-slider"
          v-model.number="budget"
          class="budget-slider"
          type="range"
          min="0"
          :max="maxBudget"
          step="500"
        />
        <div class="budget-scale">
          <span>{{ currencySymbol }}0</span>
          <span>{{ currencySymbol }}{{ maxBudget.toLocaleString() }}</span>
        </div>
        <p class="budget-hint">{{ t('restocking.budgetHint') }}</p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">{{ t('restocking.budget') }}</div>
          <div class="stat-value">{{ currencySymbol }}{{ budget.toLocaleString() }}</div>
        </div>
        <div class="stat-card info">
          <div class="stat-label">{{ t('restocking.selectedTotal') }}</div>
          <div class="stat-value">{{ currencySymbol }}{{ selectedTotal.toLocaleString() }}</div>
        </div>
        <div :class="['stat-card', remaining < 0 ? 'danger' : 'success']">
          <div class="stat-label">{{ t('restocking.remaining') }}</div>
          <div class="stat-value">{{ remaining < 0 ? '-' : '' }}{{ currencySymbol }}{{ Math.abs(remaining).toLocaleString() }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">{{ t('restocking.leadTime') }}</div>
          <div class="stat-value">{{ leadTime === null ? '-' : t('restocking.days', { count: leadTime }) }}</div>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ t('restocking.recommendedItems') }} ({{ recommendation.length }})</h3>
        </div>

        <div v-if="recommendation.length === 0" class="empty-state">
          {{ t('restocking.emptyState') }}
        </div>
        <div v-else class="table-container">
          <table class="restock-table">
            <thead>
              <tr>
                <th class="col-check"></th>
                <th>{{ t('restocking.table.sku') }}</th>
                <th>{{ t('restocking.table.trend') }}</th>
                <th class="col-qty">{{ t('restocking.table.quantity') }}</th>
                <th class="col-num">{{ t('restocking.table.unitCost') }}</th>
                <th class="col-num">{{ t('restocking.table.lineCost') }}</th>
                <th class="col-num">{{ t('restocking.table.leadTime') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in recommendation" :key="item.item_sku">
                <td class="col-check">
                  <input
                    v-model="selection[item.item_sku].selected"
                    type="checkbox"
                    :aria-label="t('restocking.selectItem', { sku: item.item_sku })"
                  />
                </td>
                <td>
                  <strong>{{ item.item_sku }}</strong>
                  <div class="item-name">{{ translateProductName(item.item_name) }}</div>
                </td>
                <td>
                  <span :class="['badge', item.trend]">{{ t(`trends.${item.trend}`) }}</span>
                </td>
                <td class="col-qty">
                  <input
                    v-model.number="selection[item.item_sku].quantity"
                    :class="['qty-input', { invalid: !isValidQty(selection[item.item_sku].quantity) }]"
                    type="number"
                    min="1"
                    step="1"
                    :aria-label="t('restocking.table.quantity')"
                  />
                </td>
                <td class="col-num">{{ currencySymbol }}{{ item.unit_cost.toLocaleString() }}</td>
                <td class="col-num">
                  <strong>{{ currencySymbol }}{{ lineCost(item).toLocaleString() }}</strong>
                </td>
                <td class="col-num">{{ item.lead_time_days }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="order-actions">
          <p v-if="overBudget" class="warning-text">{{ t('restocking.overBudget') }}</p>
          <button
            type="button"
            class="btn-primary"
            :disabled="!canSubmit"
            @click="placeOrder"
          >
            {{ submitting ? t('restocking.placing') : t('restocking.placeOrder') }}
          </button>
        </div>

        <div v-if="submitError" class="error">{{ submitError }}</div>
        <div v-if="successOrder" class="success-message">
          {{ t('restocking.orderSuccess', {
            orderNumber: successOrder.order_number,
            days: successOrder.lead_time_days,
            date: formatDate(successOrder.expected_delivery)
          }) }}
          <router-link to="/orders">{{ t('restocking.viewOrders') }}</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { api } from '../api'
import { useI18n } from '../composables/useI18n'

const BUDGET_STEP = 500

export default {
  name: 'Restocking',
  setup() {
    const { t, currentCurrency, currentLocale, translateProductName } = useI18n()

    const currencySymbol = computed(() => {
      return currentCurrency.value === 'JPY' ? '¥' : '$'
    })

    const loading = ref(true)
    const error = ref(null)
    const demand = ref([]) // raw API data; everything else is derived
    const budget = ref(0)
    // Per-SKU { selected, quantity }, re-seeded whenever the recommendation changes
    const selection = ref({})
    const submitting = ref(false)
    const submitError = ref(null)
    const successOrder = ref(null)

    const isValidQty = (q) => Number.isInteger(q) && q >= 1

    const trendRank = (trend) => (trend === 'increasing' ? 0 : 1)

    // Items whose forecast exceeds current demand, ranked: increasing trend first,
    // then by growth percent descending. Zero current demand counts as infinite growth.
    const candidates = computed(() => {
      return demand.value
        .map(item => {
          const shortfall = item.forecasted_demand - item.current_demand
          const growth = item.current_demand > 0 ? shortfall / item.current_demand : Infinity
          return { ...item, shortfall, growth }
        })
        .filter(item => item.shortfall > 0)
        .sort((a, b) => {
          const byTrend = trendRank(a.trend) - trendRank(b.trend)
          if (byTrend !== 0) return byTrend
          if (a.growth !== b.growth) return b.growth - a.growth
          return a.item_sku.localeCompare(b.item_sku)
        })
    })

    // Slider max: cost of restocking every candidate, rounded up to the next step
    const maxBudget = computed(() => {
      const total = candidates.value.reduce((sum, i) => sum + i.shortfall * i.unit_cost, 0)
      return Math.ceil(total / BUDGET_STEP) * BUDGET_STEP
    })

    // Greedy walk of the ranked list: take an item at its full shortfall if it fits
    // the remaining budget, otherwise skip it and try the next (cheaper) one.
    // Money is compared in whole cents so float noise (e.g. 4.2 * 100 = 420.00000000000006)
    // can't skip an item that exactly fits, and the client agrees with the server's rounding.
    const toCents = (amount) => Math.round(amount * 100)

    const recommendation = computed(() => {
      let remainingCents = toCents(budget.value)
      const picked = []
      for (const item of candidates.value) {
        const costCents = toCents(item.shortfall * item.unit_cost)
        if (costCents <= remainingCents) {
          picked.push(item)
          remainingCents -= costCents
        }
      }
      return picked
    })

    // Re-seed selection when the recommendation changes, but keep the user's unchecked
    // items and edited quantities for SKUs that are still recommended.
    watch(
      recommendation,
      (items) => {
        const next = {}
        for (const item of items) {
          next[item.item_sku] = selection.value[item.item_sku] ||
            { selected: true, quantity: item.shortfall }
        }
        selection.value = next
      },
      { immediate: true }
    )

    const lineCost = (item) => {
      const sel = selection.value[item.item_sku]
      if (!sel || !isValidQty(sel.quantity)) return 0
      return sel.quantity * item.unit_cost
    }

    const selectedItems = computed(() => {
      return recommendation.value.filter(item => selection.value[item.item_sku]?.selected)
    })

    const selectedTotal = computed(() => {
      return selectedItems.value.reduce((sum, item) => sum + lineCost(item), 0)
    })

    const remaining = computed(() => budget.value - selectedTotal.value)
    const overBudget = computed(() => toCents(selectedTotal.value) > toCents(budget.value))

    const leadTime = computed(() => {
      if (selectedItems.value.length === 0) return null
      return Math.max(...selectedItems.value.map(i => i.lead_time_days))
    })

    const hasInvalidQty = computed(() => {
      return selectedItems.value.some(item => !isValidQty(selection.value[item.item_sku].quantity))
    })

    const canSubmit = computed(() => {
      return selectedItems.value.length > 0 &&
        !hasInvalidQty.value &&
        !overBudget.value &&
        !submitting.value
    })

    const formatDate = (dateString) => {
      // Date-only strings (YYYY-MM-DD) parse as UTC midnight, which displays a day early
      // in timezones behind UTC, so force them to be read as local dates
      const isDateOnly = /^\d{4}-\d{2}-\d{2}$/.test(dateString || '')
      const date = new Date(isDateOnly ? `${dateString}T00:00:00` : dateString)
      if (isNaN(date.getTime())) return dateString || '-'
      const locale = currentLocale.value === 'ja' ? 'ja-JP' : 'en-US'
      return date.toLocaleDateString(locale, { year: 'numeric', month: 'short', day: 'numeric' })
    }

    const loadDemand = async () => {
      try {
        loading.value = true
        error.value = null
        demand.value = await api.getDemandForecasts()
        // Default to roughly half the full-recommendation cost, snapped to the step
        budget.value = Math.round(maxBudget.value / 2 / BUDGET_STEP) * BUDGET_STEP
      } catch (err) {
        error.value = t('restocking.loadError')
        console.error('Failed to load demand forecasts:', err)
      } finally {
        loading.value = false
      }
    }

    const placeOrder = async () => {
      if (!canSubmit.value) return
      submitting.value = true
      submitError.value = null
      successOrder.value = null
      try {
        const order = await api.createRestockOrder({
          items: selectedItems.value.map(item => ({
            sku: item.item_sku,
            quantity: selection.value[item.item_sku].quantity
          })),
          budget: budget.value
        })
        successOrder.value = order
        // Reset: deselect everything and restore the recommended quantities
        const next = {}
        for (const item of recommendation.value) {
          next[item.item_sku] = { selected: false, quantity: item.shortfall }
        }
        selection.value = next
      } catch (err) {
        submitError.value = err.response?.data?.detail || t('restocking.orderFailed')
        console.error('Failed to place restock order:', err)
      } finally {
        submitting.value = false
      }
    }

    // Moving the slider invalidates any previous result messages
    watch(budget, () => {
      successOrder.value = null
      submitError.value = null
    })

    onMounted(loadDemand)

    return {
      t,
      currencySymbol,
      translateProductName,
      loading,
      error,
      budget,
      maxBudget,
      recommendation,
      selection,
      selectedTotal,
      remaining,
      overBudget,
      leadTime,
      canSubmit,
      submitting,
      submitError,
      successOrder,
      isValidQty,
      lineCost,
      formatDate,
      placeOrder
    }
  }
}
</script>

<style scoped>
.budget-card {
  margin-bottom: 1.5rem;
}

.budget-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1rem;
}

.budget-label {
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.budget-value {
  font-size: 2rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.025em;
}

/* Custom slate range slider */
.budget-slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: #e2e8f0;
  outline: none;
  cursor: pointer;
}

.budget-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #0f172a;
  border: 3px solid white;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.4);
}

.budget-slider::-moz-range-thumb {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #0f172a;
  border: 3px solid white;
  box-shadow: 0 1px 4px rgba(15, 23, 42, 0.4);
}

.budget-slider:focus-visible::-webkit-slider-thumb {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.budget-slider:focus-visible::-moz-range-thumb {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

.budget-scale {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.813rem;
  color: #64748b;
}

.budget-hint {
  margin: 0.75rem 0 0;
  font-size: 0.875rem;
  color: #64748b;
}

.restock-table {
  width: 100%;
}

.col-check {
  width: 48px;
}

.col-qty {
  width: 120px;
}

.col-num {
  text-align: right;
  white-space: nowrap;
}

.item-name {
  font-size: 0.875rem;
  color: #64748b;
}

.qty-input {
  width: 90px;
  padding: 0.375rem 0.5rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #0f172a;
}

.qty-input:focus {
  outline: none;
  border-color: #0f172a;
}

.qty-input.invalid {
  border-color: #ef4444;
  background: #fef2f2;
}

.empty-state {
  padding: 2rem;
  text-align: center;
  color: #64748b;
  font-size: 0.938rem;
}

.order-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1rem 0 0;
}

.warning-text {
  margin: 0;
  color: #92400e;
  font-size: 0.875rem;
}

.btn-primary {
  background: #0f172a;
  color: white;
  border: 1px solid #0f172a;
  border-radius: 8px;
  padding: 0.625rem 1.25rem;
  font-size: 0.938rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.btn-primary:hover:not(:disabled) {
  background: #1e293b;
}

.btn-primary:disabled {
  background: #cbd5e1;
  border-color: #cbd5e1;
  color: #64748b;
  cursor: not-allowed;
}

.success-message {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0 0;
  font-size: 0.938rem;
}

.success-message a {
  margin-left: 0.5rem;
  color: #1e40af;
  font-weight: 600;
}
</style>
