import { ref } from 'vue'

const warehouse = ref('all')

export function useFilters() {
  return { warehouse }
}
