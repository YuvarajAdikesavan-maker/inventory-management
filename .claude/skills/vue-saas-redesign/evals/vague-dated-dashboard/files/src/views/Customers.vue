<template>
  <div>
    <h2 class="title">Customers</h2>
    <div class="box">
      <input v-model="query" class="search" placeholder="Search customers" />
      <table class="tbl">
        <thead><tr><th>Name</th><th>Plan</th><th>MRR</th><th>Since</th></tr></thead>
        <tbody>
          <tr v-for="c in filtered" :key="c.id">
            <td>{{ c.name }}</td><td>{{ c.plan }}</td><td>{{ c.mrr }}</td><td>{{ c.since }}</td>
          </tr>
          <tr v-if="filtered.length === 0"><td colspan="4">No customers match.</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'Customers',
  setup() {
    const query = ref('')
    const customers = [
      { id: 1, name: 'Acme Corp', plan: 'Business', mrr: '$400', since: '2023-02-11' },
      { id: 2, name: 'Globex', plan: 'Starter', mrr: '$49', since: '2024-06-03' },
      { id: 3, name: 'Initech', plan: 'Business', mrr: '$400', since: '2022-09-19' },
      { id: 4, name: 'Umbrella', plan: 'Enterprise', mrr: '$1,200', since: '2021-01-28' }
    ]
    const filtered = computed(() =>
      customers.filter(c => c.name.toLowerCase().includes(query.value.toLowerCase()))
    )
    return { query, filtered }
  }
}
</script>

<style scoped>
.title { font-size: 28px; margin: 0 0 14px; }
.search { padding: 7px 10px; margin-bottom: 14px; width: 260px; border: 1px solid #bbb; }
</style>
