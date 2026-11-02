<template>
  <div>
    <h2 class="title">Invoices</h2>
    <div class="box">
      <h3>All invoices</h3>
      <table class="tbl">
        <thead>
          <tr><th>Invoice</th><th>Customer</th><th>Issued</th><th>Due</th><th>Amount</th><th>Status</th></tr>
        </thead>
        <tbody>
          <tr v-for="i in invoices" :key="i.id">
            <td>{{ i.id }}</td><td>{{ i.customer }}</td><td>{{ i.issued }}</td>
            <td>{{ i.due }}</td><td>{{ i.amount }}</td>
            <td><span :class="['pill', i.status]">{{ i.status }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Invoices',
  setup() {
    const invoices = [
      { id: 'INV-1040', customer: 'Umbrella', issued: '2026-09-28', due: '2026-10-28', amount: '$1,200', status: 'paid' },
      { id: 'INV-1042', customer: 'Acme Corp', issued: '2026-10-02', due: '2026-11-01', amount: '$2,400', status: 'paid' },
      { id: 'INV-1043', customer: 'Globex', issued: '2026-10-15', due: '2026-11-14', amount: '$980', status: 'due' },
      { id: 'INV-1044', customer: 'Initech', issued: '2026-09-01', due: '2026-10-01', amount: '$5,150', status: 'late' }
    ]
    return { invoices }
  }
}
</script>

<style scoped>
.title { font-size: 24px; margin: 0 0 20px; }
</style>
