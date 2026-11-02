<template>
  <div>
    <h2 class="title">Dashboard</h2>
    <div class="cards">
      <div class="card" v-for="s in stats" :key="s.label">
        <div class="label">{{ s.label }}</div>
        <div class="value">{{ s.value }}</div>
      </div>
    </div>
    <div class="box">
      <h3>Recent activity</h3>
      <table class="tbl">
        <thead><tr><th>Invoice</th><th>Customer</th><th>Amount</th><th>Status</th></tr></thead>
        <tbody>
          <tr v-for="r in recent" :key="r.id">
            <td>{{ r.id }}</td><td>{{ r.customer }}</td><td>{{ r.amount }}</td>
            <td><span :class="['pill', r.status]">{{ r.status }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  setup() {
    const stats = [
      { label: 'Revenue (30d)', value: '$48,200' },
      { label: 'Open invoices', value: '17' },
      { label: 'Overdue', value: '3' },
      { label: 'Customers', value: '124' }
    ]
    const recent = [
      { id: 'INV-1042', customer: 'Acme Corp', amount: '$2,400', status: 'paid' },
      { id: 'INV-1043', customer: 'Globex', amount: '$980', status: 'due' },
      { id: 'INV-1044', customer: 'Initech', amount: '$5,150', status: 'late' }
    ]
    return { stats, recent }
  }
}
</script>

<style scoped>
.title { font-size: 26px; margin: 0 0 18px; }
.cards { display: flex; gap: 14px; margin-bottom: 25px; flex-wrap: wrap; }
.card { background: white; border: 1px solid #ddd; padding: 16px 20px; width: 210px; border-radius: 4px; }
.label { color: #777; font-size: 13px; }
.value { font-size: 24px; margin-top: 6px; font-weight: bold; }
</style>
